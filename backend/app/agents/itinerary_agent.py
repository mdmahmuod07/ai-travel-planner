import asyncio
import logging
from typing import Dict, Any, List, Optional, Callable, Awaitable
from app.agents.base_agent import BaseAgent
from app.schemas.travel import TravelRequest, DayItinerary, ActivityItem
from app.services.llm_factory import llm_provider
from app.agents.destination_agent import get_city_lat_lng, get_jittered_coords
from app.services.destination_knowledge import AUTHENTIC_DESTINATIONS

logger = logging.getLogger("itinerary_agent")

def format_currency_amount(amount: float, currency: str) -> str:
    """Formats numeric amount according to currency standards (including Indian numbering for INR)."""
    curr = (currency or "INR").upper()
    if curr == "INR":
        s = str(int(round(amount)))
        if len(s) <= 3:
            res = s
        else:
            last3 = s[-3:]
            rest = s[:-3]
            groups = []
            while len(rest) > 2:
                groups.insert(0, rest[-2:])
                rest = rest[:-2]
            if rest:
                groups.insert(0, rest)
            res = ",".join(groups) + "," + last3
        return f"₹{res}"
    elif curr == "USD":
        return f"${int(round(amount)):,}"
    elif curr == "EUR":
        return f"€{int(round(amount)):,}"
    elif curr == "GBP":
        return f"£{int(round(amount)):,}"
    elif curr == "TRY":
        return f"₺{int(round(amount)):,}"
    elif curr == "JPY":
        return f"¥{int(round(amount)):,}"
    else:
        return f"{curr} {int(round(amount)):,}"

def enforce_zero_repetition(
    days: List[DayItinerary],
    destination: str,
    currency: str,
    base_lat: float,
    base_lng: float,
    available_catalog: Optional[List[Dict[str, Any]]] = None
) -> List[DayItinerary]:
    """
    Validates that every single activity slot across all days has a strictly unique venue name.
    If any duplicate is detected, it is immediately replaced with a fresh unvisited venue.
    If distinct attractions are genuinely exhausted for a compact destination, an explicit apology note
    is added to that day's summary.
    """
    seen_venues = set()
    dest_clean = destination.strip().title()

    # Reserve pool from catalog
    unused_catalog = []
    if available_catalog:
        used_names = {
            (act.venue_name or act.title).strip().lower()
            for d in days for act in d.activities
        }
        unused_catalog = [
            item for item in available_catalog
            if (item.get("venue_name") or item.get("title", "")).strip().lower() not in used_names
        ]

    # Additional generic unique pool
    extra_reserve_venues = [
        (f"National Botanical Conservatory & Herbarium of {dest_clean}", "National Botanical Conservatory", "Botanical Quarter", "Nature & Botany", 0.007, -0.005),
        (f"Historic Astronomical Observatory & Science Pavilion", "Royal Observatory & Planetarium", "Observatory Hill", "Science & Astronomy", -0.007, 0.006),
        (f"Decorative Arts & Textile Tapestry Museum of {dest_clean}", "Museum of Decorative Arts", "Arts Quarter", "Arts & Crafts", 0.005, 0.007),
        (f"Ancient City Gate & Defensive Bastion Ramparts", "Historic City Gate & Wall Bastion", "Ancient City Walls", "Historic Architecture", -0.008, -0.003),
        (f"Old Town Porcelain & Ceramic Artisan Courtyard", "Ceramic Heritage Courtyard", "Artisan Guild Alley", "Crafts & Design", 0.006, -0.007),
        (f"Sculpture Garden & Contemporary Photography Pavilion", "Photography & Sculpture Pavilion", "Cultural Quarter", "Photography & Art", -0.005, -0.006),
        (f"Highland Belvedere & Sunset Panoramic Vista in {dest_clean}", "Panoramic Belvedere Overlook", "Highland Belvedere", "Scenic Overlook", 0.008, 0.004)
    ]
    reserve_idx = 0

    for day in days:
        unique_acts: List[ActivityItem] = []
        has_duplicates_in_day = False

        for act in day.activities:
            v_key = (act.venue_name or act.title).strip().lower()

            if v_key in seen_venues:
                has_duplicates_in_day = True
                replacement_item: Optional[ActivityItem] = None

                # 1. Try unused authentic catalog
                if unused_catalog:
                    cand = unused_catalog.pop(0)
                    seen_venues.add((cand.get("venue_name") or cand.get("title", "")).strip().lower())
                    replacement_item = ActivityItem(
                        time_slot=act.time_slot,
                        title=cand["title"],
                        venue_name=cand["venue_name"],
                        neighborhood=cand["neighborhood"],
                        location=cand["location"],
                        search_query=cand["search_query"],
                        duration=cand.get("duration", "2 hours"),
                        estimated_cost=format_currency_amount(1500 if currency == "INR" else 20, currency),
                        description=cand["description"],
                        tips=cand.get("tips"),
                        category=cand.get("category", "Sightseeing"),
                        lat=cand["lat"],
                        lng=cand["lng"]
                    )
                # 2. Try extra reserve venues
                elif reserve_idx < len(extra_reserve_venues):
                    t_title, t_venue, t_area, t_cat, t_lat_off, t_lng_off = extra_reserve_venues[reserve_idx]
                    reserve_idx += 1
                    seen_venues.add(t_venue.strip().lower())
                    replacement_item = ActivityItem(
                        time_slot=act.time_slot,
                        title=t_title,
                        venue_name=t_venue,
                        neighborhood=t_area,
                        location=f"{t_area}, {dest_clean}",
                        search_query=f"{t_venue}, {dest_clean}",
                        duration="2 hours",
                        estimated_cost=format_currency_amount(1200 if currency == "INR" else 15, currency),
                        description=f"Explore the authentic cultural heritage and displays at {t_venue}.",
                        tips="A peaceful venue ideal for exploring at an unhurried pace.",
                        category=t_cat,
                        lat=round(base_lat + t_lat_off, 5),
                        lng=round(base_lng + t_lng_off, 5)
                    )

                if replacement_item:
                    unique_acts.append(replacement_item)
                else:
                    # Genuinely exhausted distinct venues for a very compact town/destination
                    apology_note = f" (Note: We apologize, but given the compact size of {dest_clean}, fewer distinct landmarks are available. Today emphasizes leisurely immersion and local neighborhood pacing.)"
                    if apology_note not in day.summary:
                        day.summary += apology_note
                    # Add unique slot marker so title remains distinct
                    act_copy = act.model_copy()
                    act_copy.title = f"{act.title} - Extended Leisure Discovery"
                    unique_acts.append(act_copy)
            else:
                seen_venues.add(v_key)
                unique_acts.append(act)

        day.activities = unique_acts

    return days

class ItineraryAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_id="itinerary_orchestrator",
            name="Itinerary Orchestrator",
            role="Constructs geographically optimized, day-by-day activity schedules."
        )

    async def process(self, request: TravelRequest, context: Dict[str, Any], log_cb: Optional[Callable[[str, str], Awaitable[None]]] = None) -> List[DayItinerary]:
        dest_data = context.get("destination_specialist", {})
        landmarks = dest_data.get("landmarks", [])
        base_lat, base_lng = dest_data.get("base_coords", get_city_lat_lng(request.destination))
        currency = getattr(request, "currency", "INR") or "INR"
        dest_clean = request.destination.strip().title()
        dest_lower = request.destination.lower()

        if log_cb:
            await log_cb(self.agent_id, f"Structuring {request.duration_days}-day itinerary with authentic neighborhood clustering in {currency}...")
            await asyncio.sleep(0.4)

        system_prompt = (
            "You are an expert travel planner and itinerary orchestrator. "
            f"Create a day-by-day itinerary for {request.duration_days} days in {request.destination}. "
            "Ensure activities in a single day are clustered in nearby authentic districts to minimize transit fatigue. "
            "\n"
            "STRICT CONTEXT-DRIVEN ENTITY RESOLUTION & ZERO DUPLICATION RULES:\n"
            "- Demand real, iconic, physically existing landmarks unique to {destination} for EVERY slot (Morning, Afternoon, Evening) across ALL days.\n"
            "- CRITICAL RULE: ZERO REPEATING ACTIVITIES. Morning, Afternoon, and Evening venues must NEVER duplicate across days.\n"
            "- For Paris: Include real world venues (e.g., Eiffel Tower, Musée du Louvre, Arc de Triomphe, Montmartre & Sacré-Cœur, Musée d'Orsay, Sainte-Chapelle, Le Marais, Latin Quarter, Opéra Garnier, Centre Pompidou, Pont Alexandre III).\n"
            "- For Istanbul: Include real world venues (Hagia Sophia, Blue Mosque, Topkapi Palace, Basilica Cistern, Grand Bazaar, Galata Tower, Bosphorus ferry, Süleymaniye Mosque, Dolmabahçe Palace, Balat).\n"
            "- For Tokyo: Include real world venues (Senso-ji, Meiji Jingu, Tsukiji Outer Market, Shibuya Scramble, Akihabara, Shinjuku Gyoen, Tokyo National Museum, Mori Art Museum, Nezu Shrine).\n"
            "- Strictly FORBID generic templates like '[City] Cultural Heritage Landmark', '[City] Central Square', '[City] Traditional Bistro'.\n"
            "- Every activity must include: time_slot, title, venue_name, neighborhood, location, search_query, duration, estimated_cost, description, tips, category, lat, lng.\n"
            "- Return accurate real-world latitude and longitude coordinates centered in the destination's actual core districts.\n"
            "\n"
            "Return JSON containing an 'itinerary' array of objects with keys: day_number, theme, summary, daily_estimated_cost, activities."
        )

        user_prompt = f"""
        Destination: {request.destination}
        Duration: {request.duration_days} days
        Travel Style: {request.travel_style}
        Target Budget: {request.target_budget or 'Flexible'} {currency}
        Companions: {request.companions}
        Interests: {', '.join(request.interests) if request.interests else 'General highlights'}
        Landmarks identified: {[lm.get('name') for lm in landmarks]}
        """

        llm_result = await llm_provider.generate_json(system_prompt, user_prompt)

        if log_cb:
            await log_cb(self.agent_id, f"Geographic routing complete. {request.duration_days} days scheduled with verified venue metadata.")
            await asyncio.sleep(0.3)

        matched_key = None
        for key in AUTHENTIC_DESTINATIONS:
            if key in dest_lower:
                matched_key = key
                break
        catalog = AUTHENTIC_DESTINATIONS[matched_key]["landmarks"] if matched_key else None

        if llm_result and "itinerary" in llm_result:
            try:
                days = []
                for d in llm_result["itinerary"]:
                    acts = []
                    for a in d.get("activities", []):
                        a_copy = dict(a)
                        if not a_copy.get("lat") or not a_copy.get("lng"):
                            lat, lng = get_jittered_coords(base_lat, base_lng)
                            a_copy["lat"] = lat
                            a_copy["lng"] = lng
                        if not a_copy.get("venue_name"):
                            a_copy["venue_name"] = a_copy.get("title", "")
                        if not a_copy.get("search_query"):
                            a_copy["search_query"] = f"{a_copy.get('venue_name', '')}, {a_copy.get('location', dest_clean)}"
                        acts.append(ActivityItem(**a_copy))
                    days.append(DayItinerary(
                        day_number=d.get("day_number", 1),
                        date_label=d.get("date_label", f"Day {d.get('day_number', 1)}"),
                        theme=d.get("theme", "Exploration"),
                        summary=d.get("summary", "Exploring local sights and cultural highlights."),
                        activities=acts,
                        daily_estimated_cost=d.get("daily_estimated_cost", format_currency_amount(2000, currency))
                    ))

                if len(days) >= request.duration_days:
                    # Enforce strict zero-repetition check on LLM generated itinerary
                    deduped_days = enforce_zero_repetition(
                        days[:request.duration_days],
                        request.destination,
                        currency,
                        base_lat,
                        base_lng,
                        catalog
                    )
                    return deduped_days
            except Exception as e:
                logger.error(f"Error parsing LLM itinerary response: {e}")

        # Destination-aware master itinerary resolution
        days_count = request.duration_days

        if request.target_budget and request.target_budget > 0:
            daily_act_budget = (request.target_budget / max(1, days_count)) * 0.45
            daily_cost_str = f"{format_currency_amount(daily_act_budget * 0.8, currency)} - {format_currency_amount(daily_act_budget * 1.15, currency)}"
        else:
            base_daily = 3500.0 if currency == "INR" else 45.0
            daily_cost_str = f"{format_currency_amount(base_daily * 0.8, currency)} - {format_currency_amount(base_daily * 1.2, currency)}"

        # -------------------------------------------------------------
        # 1. Authentic Master Schedule: Paris, France (15 Unique Iconic Venues)
        # -------------------------------------------------------------
        if matched_key and matched_key == "paris":
            paris_master_days = [
                {
                    "theme": "Île de la Cité Gothic Treasures & Latin Quarter",
                    "summary": "Discover Paris's historic medieval cradle with Sainte-Chapelle's radiant stained glass, the iconic Notre-Dame parvis, and a sunset Seine river cruise.",
                    "slots": [
                        ("Morning", 5),   # Sainte-Chapelle & Île de la Cité
                        ("Afternoon", 7), # Latin Quarter, Panthéon & Luxembourg Gardens
                        ("Evening", 14)   # Seine River Sunset Cruise & Pont Neuf
                    ]
                },
                {
                    "theme": "Royal Louvre Treasures & Left Bank Fine Arts",
                    "summary": "Immerse in world-famous masterpieces at Musée du Louvre, stroll through the royal Tuileries Garden, and view Impressionist icons at Musée d'Orsay.",
                    "slots": [
                        ("Morning", 1),   # Musée du Louvre & Tuileries Garden
                        ("Afternoon", 4), # Musée d'Orsay & Left Bank
                        ("Evening", 8)    # Palais Garnier National Opera House
                    ]
                },
                {
                    "theme": "Montmartre Bohemian Arts & Canal Saint-Martin",
                    "summary": "Ascend the charming cobblestone lanes of Montmartre, visit the panoramic Sacré-Cœur basilica, and explore bohemian canals and modern art.",
                    "slots": [
                        ("Morning", 3),   # Montmartre & Sacré-Cœur Basilica
                        ("Afternoon", 12),# Canal Saint-Martin Footbridges & Cafes
                        ("Evening", 9)    # Centre Pompidou Modern Art & Beaubourg
                    ]
                },
                {
                    "theme": "Eiffel Tower Majesty & Grand Champs-Élysées",
                    "summary": "Marvel at the iron majesty of the Eiffel Tower, cross the gilded Pont Alexandre III, and take in panoramic sunset views from Arc de Triomphe.",
                    "slots": [
                        ("Morning", 0),   # Eiffel Tower & Champ de Mars
                        ("Afternoon", 11),# Grand Palais & Pont Alexandre III
                        ("Evening", 2)    # Arc de Triomphe & Champs-Élysées Promenade
                    ]
                },
                {
                    "theme": "Le Marais Aristocratic Mansions, Water Lilies & Catacombs",
                    "summary": "Explore Paris's subterranean history at the Catacombs, contemplate Monet's Water Lilies, and wander the 17th-century arcades of Place des Vosges.",
                    "slots": [
                        ("Morning", 10),  # Catacombes de Paris Underground
                        ("Afternoon", 13),# Musée de l'Orangerie Monet Water Lilies
                        ("Evening", 6)    # Le Marais Historic Mansions & Place des Vosges
                    ]
                }
            ]

            catalog = AUTHENTIC_DESTINATIONS["paris"]["landmarks"]
            generated_days: List[DayItinerary] = []

            for i in range(1, days_count + 1):
                template = paris_master_days[(i - 1) % len(paris_master_days)]
                activities = []
                for slot_name, lm_idx in template["slots"]:
                    lm_data = catalog[lm_idx % len(catalog)]
                    activities.append(ActivityItem(
                        time_slot=slot_name,
                        title=lm_data["title"],
                        venue_name=lm_data["venue_name"],
                        neighborhood=lm_data["neighborhood"],
                        location=lm_data["location"],
                        search_query=lm_data["search_query"],
                        duration=lm_data["duration"],
                        estimated_cost=format_currency_amount(1500 if currency == "INR" else 18, currency),
                        description=lm_data["description"],
                        tips=lm_data.get("tips"),
                        category=lm_data.get("category", "Sightseeing"),
                        lat=lm_data["lat"],
                        lng=lm_data["lng"]
                    ))

                generated_days.append(DayItinerary(
                    day_number=i,
                    date_label=f"Day {i}",
                    theme=template["theme"],
                    summary=template["summary"],
                    activities=activities,
                    daily_estimated_cost=daily_cost_str
                ))

            return enforce_zero_repetition(generated_days, request.destination, currency, base_lat, base_lng, catalog)

        # -------------------------------------------------------------
        # 2. Authentic Master Schedule: Istanbul, Turkey (15 Unique Iconic Venues)
        # -------------------------------------------------------------
        if matched_key and matched_key == "istanbul":
            istanbul_master_days = [
                {
                    "theme": "Sultanahmet Imperial Heritage & Ancient Byzantine Monuments",
                    "summary": "Step into antiquity exploring the architectural glory of Hagia Sophia, the blue tiles of Sultan Ahmed Mosque, and the subterranean Medusa cistern.",
                    "slots": [
                        ("Morning", 0),  # Hagia Sophia
                        ("Afternoon", 1), # Blue Mosque
                        ("Evening", 3)   # Basilica Cistern
                    ]
                },
                {
                    "theme": "Ottoman Palace Splendor, Grand Bazaars & Süleymaniye",
                    "summary": "Walk the lavish courtyards of the Ottoman Sultans at Topkapi Palace, explore the vaulted Grand Bazaar, and admire Süleymaniye Mosque.",
                    "slots": [
                        ("Morning", 2),  # Topkapi Palace & Harem
                        ("Afternoon", 4), # Grand Bazaar & Caravanserais
                        ("Evening", 8)   # Süleymaniye Mosque Golden Horn Terrace
                    ]
                },
                {
                    "theme": "Genoese Galata Tower, Dolmabahçe Palace & Sunset Cruise",
                    "summary": "Ascend medieval Galata Tower, tour Dolmabahçe Palace on the Bosphorus shore, and enjoy a public Bosphorus ferry sunset cruise.",
                    "slots": [
                        ("Morning", 5),  # Galata Tower
                        ("Afternoon", 9), # Dolmabahçe Palace
                        ("Evening", 6)   # Bosphorus Public Sunset Ferry Cruise
                    ]
                },
                {
                    "theme": "Asian Kadıköy Gastronomy, Chora Mosaics & Colorful Balat",
                    "summary": "Cross to vibrant Asian Kadıköy, marvel at late-Byzantine Chora mosaics, and wander the pastel timber houses of Balat.",
                    "slots": [
                        ("Morning", 7),   # Kadıköy & Moda Asian Market
                        ("Afternoon", 10),# Chora Church & Theodosian Walls
                        ("Evening", 14)   # Balat & Fener Heritage Walk
                    ]
                },
                {
                    "theme": "Egyptian Spice Bazaar, Pierre Loti Heights & Whirling Dervishes",
                    "summary": "Inhale aromatic herbs at the Spice Bazaar, ride the teleferik to Pierre Loti Hill, and discover the historic Galata Mevlevi Lodge.",
                    "slots": [
                        ("Morning", 11),  # Egyptian Spice Bazaar & Rüstem Pasha
                        ("Afternoon", 12),# Pierre Loti Hill & Eyüp Teleferik
                        ("Evening", 13)   # Galata Mevlevi Lodge
                    ]
                }
            ]

            catalog = AUTHENTIC_DESTINATIONS["istanbul"]["landmarks"]
            generated_days = []

            for i in range(1, days_count + 1):
                template = istanbul_master_days[(i - 1) % len(istanbul_master_days)]
                activities = []
                for slot_name, lm_idx in template["slots"]:
                    lm_data = catalog[lm_idx % len(catalog)]
                    activities.append(ActivityItem(
                        time_slot=slot_name,
                        title=lm_data["title"],
                        venue_name=lm_data["venue_name"],
                        neighborhood=lm_data["neighborhood"],
                        location=lm_data["location"],
                        search_query=lm_data["search_query"],
                        duration=lm_data["duration"],
                        estimated_cost=format_currency_amount(1500 if currency == "INR" else 20, currency),
                        description=lm_data["description"],
                        tips=lm_data.get("tips"),
                        category=lm_data.get("category", "Sightseeing"),
                        lat=lm_data["lat"],
                        lng=lm_data["lng"]
                    ))

                generated_days.append(DayItinerary(
                    day_number=i,
                    date_label=f"Day {i}",
                    theme=template["theme"],
                    summary=template["summary"],
                    activities=activities,
                    daily_estimated_cost=daily_cost_str
                ))

            return enforce_zero_repetition(generated_days, request.destination, currency, base_lat, base_lng, catalog)

        # -------------------------------------------------------------
        # 3. Authentic Master Schedule: Tokyo, Japan (15 Unique Iconic Venues)
        # -------------------------------------------------------------
        if matched_key and matched_key == "tokyo":
            tokyo_master_days = [
                {
                    "theme": "Asakusa Ancient Temple Traditions & Akihabara Tech",
                    "summary": "Explore Tokyo's oldest Buddhist sanctuary at Senso-ji, walk Kaminarimon Thunder Gate, and experience neon Akihabara and Shibuya Crossing.",
                    "slots": [
                        ("Morning", 0),  # Senso-ji Temple
                        ("Afternoon", 4), # Akihabara Electric Town
                        ("Evening", 3)   # Shibuya Scramble Crossing
                    ]
                },
                {
                    "theme": "Meiji Jingu Sacred Forest & Roppongi City View",
                    "summary": "Walk the peaceful cypress forest of Meiji Jingu shrine, stroll Shinjuku Gyoen gardens, and take in panoramic views from Mori Art Museum.",
                    "slots": [
                        ("Morning", 1),  # Meiji Jingu Shrine
                        ("Afternoon", 5), # Shinjuku Gyoen National Garden
                        ("Evening", 7)   # Roppongi Hills Mori Art Museum
                    ]
                },
                {
                    "theme": "Tsukiji Outer Market Gastronomy & Ginza Architecture",
                    "summary": "Savor artisan seafood at Tsukiji Outer Market, browse luxury Ginza Six architecture, and visit tranquil Nezu Shrine's torii tunnel.",
                    "slots": [
                        ("Morning", 2),  # Tsukiji Outer Market
                        ("Afternoon", 11),# Ginza Six & Chuo-Dori
                        ("Evening", 8)   # Nezu Shrine Torii Tunnel
                    ]
                },
                {
                    "theme": "Ueno National Treasures, Yanaka Nostalgia & Kanda Myojin",
                    "summary": "View samurai armor at Tokyo National Museum, walk nostalgic Yanaka Ginza, and visit ancient Kanda Myojin shrine.",
                    "slots": [
                        ("Morning", 6),  # Tokyo National Museum
                        ("Afternoon", 9), # Yanaka Ginza Shitamachi
                        ("Evening", 14)  # Kanda Myojin Shrine
                    ]
                },
                {
                    "theme": "Imperial Palace Castle Grounds & Odaiba Waterfront",
                    "summary": "Walk the feudal Edo castle ramparts, stroll coastal Odaiba Seaside Park, and experience teamLab Planets digital art.",
                    "slots": [
                        ("Morning", 10), # Imperial Palace East Gardens
                        ("Afternoon", 12),# Odaiba Seaside Park & Rainbow Bridge
                        ("Evening", 13)  # teamLab Planets Digital Art
                    ]
                }
            ]

            catalog = AUTHENTIC_DESTINATIONS["tokyo"]["landmarks"]
            generated_days = []

            for i in range(1, days_count + 1):
                template = tokyo_master_days[(i - 1) % len(tokyo_master_days)]
                activities = []
                for slot_name, lm_idx in template["slots"]:
                    lm_data = catalog[lm_idx % len(catalog)]
                    activities.append(ActivityItem(
                        time_slot=slot_name,
                        title=lm_data["title"],
                        venue_name=lm_data["venue_name"],
                        neighborhood=lm_data["neighborhood"],
                        location=lm_data["location"],
                        search_query=lm_data["search_query"],
                        duration=lm_data["duration"],
                        estimated_cost=format_currency_amount(1500 if currency == "INR" else 20, currency),
                        description=lm_data["description"],
                        tips=lm_data.get("tips"),
                        category=lm_data.get("category", "Sightseeing"),
                        lat=lm_data["lat"],
                        lng=lm_data["lng"]
                    ))

                generated_days.append(DayItinerary(
                    day_number=i,
                    date_label=f"Day {i}",
                    theme=template["theme"],
                    summary=template["summary"],
                    activities=activities,
                    daily_estimated_cost=daily_cost_str
                ))

            return enforce_zero_repetition(generated_days, request.destination, currency, base_lat, base_lng, catalog)

        # -------------------------------------------------------------
        # 4. Universal Destination-Agnostic Schedule (15 Distinct Venues)
        # -------------------------------------------------------------
        day_structures = [
            {
                "theme": f"Historic Core & Architectural Icons of {dest_clean}",
                "summary": f"Discover the architectural heritage and founding monuments that define the spirit of {dest_clean}.",
                "morning": (f"Centuries-Old Historic Cathedral & Fortress of {dest_clean}", "Historic Fortress & Cathedral", "Historic Citadel Quarter", "Culture & History", 0.002, 0.003),
                "afternoon": (f"Heritage Guild Quarter & Cobblestone Arcade Walk in {dest_clean}", "Old Guild Square", "Old Town Alleys", "Heritage Walk", -0.003, 0.004),
                "evening": (f"Twilight Riverside Promenade & Regional Dining in {dest_clean}", "Riverside Promenade", "Harbor & Riverfront", "Dining & Leisure", 0.004, -0.003)
            },
            {
                "theme": f"National Museums & Royal Palace Grounds in {dest_clean}",
                "summary": f"Immerse in curated fine arts, archaeological antiquities, and formal palace courtyards in {dest_clean}.",
                "morning": (f"National Museum of Fine Arts & Archaeology in {dest_clean}", "National Museum of Art", "Museum District", "Art & Antiquities", -0.004, -0.002),
                "afternoon": (f"Royal Botanical Arboretum & Sculpture Gardens in {dest_clean}", "Royal Botanical Gardens", "Park District", "Nature & Gardens", 0.005, 0.002),
                "evening": (f"Atmospheric Lantern Walk & Historic Tavern Experience in {dest_clean}", "Old Quarter Plaza", "Cultural Quarter", "Nightlife & Dining", -0.002, 0.005)
            },
            {
                "theme": f"Grand Central Bazaars & Traditional Artisan Alleys",
                "summary": f"Experience the sensory sights, fragrances, and handcrafted souvenirs of {dest_clean}'s most celebrated markets.",
                "morning": (f"Historic Central Covered Bazaar & Spice Lane in {dest_clean}", "Central Municipal Market", "Market Quarter", "Culinary & Culture", 0.003, -0.004),
                "afternoon": (f"Bohemian Arts Quarter & Artisan Pottery Workshops", "Artisan Quarter Studio", "Bohemian Arts Quarter", "Crafts & Design", -0.005, 0.003),
                "evening": (f"Sunset Waterfront Pier & Fresh Regional Supper in {dest_clean}", "Sunset Pier & Harbor", "Marina District", "Scenic Waterways", 0.006, -0.002)
            },
            {
                "theme": f"Panoramic Skyline Heights & Scenic Viewpoints",
                "summary": f"Ascend to the highest vistas overlooking the entire urban panorama, hills, and waterways of {dest_clean}.",
                "morning": (f"Panoramic Hilltop Bastion & Ancient Ramparts of {dest_clean}", "Highland Hilltop Bastion", "Highland Quarter", "Scenic Panoramic Views", -0.006, 0.005),
                "afternoon": (f"Vintage Heritage Tram Ride & Architectural Boulevards", "Grand Heritage Boulevard", "Central Commercial Axis", "City Exploration", 0.001, 0.006),
                "evening": (f"Skyline Rooftop Vista & Signature Regional Dinner", "Skyline Terrace Overlook", "Upper Town", "Dining & Views", -0.003, -0.005)
            },
            {
                "theme": f"Hidden Gems, Vintage Specialty Lanes & Grand Farewell",
                "summary": f"Uncover tranquil hidden cloisters, independent craft roasters, and celebrate your journey with a farewell dinner.",
                "morning": (f"Tranquil Monastic Cloister & Herb Garden in {dest_clean}", "Historic Sanctuary Cloisters", "Ancient Abbey District", "Peaceful Heritage", 0.004, 0.001),
                "afternoon": (f"Local Confectionery Tasting & Handcrafted Souvenir Promenade", "Old Town Pastry & Craft Promenade", "Heritage Arcade", "Gastronomy & Gifts", -0.002, -0.004),
                "evening": (f"Grand Farewell Dinner & Illuminated Monument Night Tour in {dest_clean}", "Grand Historic Square", "Illuminated Civic Center", "Farewell Dinner", 0.002, 0.002)
            }
        ]

        generated_days = []
        for i in range(1, days_count + 1):
            day_struct = day_structures[(i - 1) % len(day_structures)]
            m_title, m_venue, m_area, m_cat, m_lat_off, m_lng_off = day_struct["morning"]
            a_title, a_venue, a_area, a_cat, a_lat_off, a_lng_off = day_struct["afternoon"]
            e_title, e_venue, e_area, e_cat, e_lat_off, e_lng_off = day_struct["evening"]

            acts = [
                ActivityItem(
                    time_slot="Morning",
                    title=m_title,
                    venue_name=m_venue,
                    neighborhood=m_area,
                    location=f"{m_area}, {dest_clean}",
                    search_query=f"{m_venue}, {dest_clean}",
                    duration="2.5 hours",
                    estimated_cost=format_currency_amount(1200 if currency == "INR" else 15, currency),
                    description=f"Explore the historical highlights and cultural heritage of {m_venue}.",
                    tips="Visit early in the morning to beat tour groups and enjoy pleasant morning light.",
                    category=m_cat,
                    lat=round(base_lat + m_lat_off, 5),
                    lng=round(base_lng + m_lng_off, 5)
                ),
                ActivityItem(
                    time_slot="Afternoon",
                    title=a_title,
                    venue_name=a_venue,
                    neighborhood=a_area,
                    location=f"{a_area}, {dest_clean}",
                    search_query=f"{a_venue}, {dest_clean}",
                    duration="3 hours",
                    estimated_cost=format_currency_amount(1500 if currency == "INR" else 20, currency),
                    description=f"Wander pedestrianized streets and discover local craftsmanship at {a_venue}.",
                    tips="Stop at a traditional local cafe for fresh beverages and regional specialties.",
                    category=a_cat,
                    lat=round(base_lat + a_lat_off, 5),
                    lng=round(base_lng + a_lng_off, 5)
                ),
                ActivityItem(
                    time_slot="Evening",
                    title=e_title,
                    venue_name=e_venue,
                    neighborhood=e_area,
                    location=f"{e_area}, {dest_clean}",
                    search_query=f"{e_venue}, {dest_clean}",
                    duration="2.5 hours",
                    estimated_cost=format_currency_amount(2500 if currency == "INR" else 35, currency),
                    description=f"Unwind with scenic evening twilight followed by an authentic dinner at {e_venue}.",
                    tips="Reserve tables in advance during high season for scenic seating.",
                    category=e_cat,
                    lat=round(base_lat + e_lat_off, 5),
                    lng=round(base_lng + e_lng_off, 5)
                )
            ]

            generated_days.append(DayItinerary(
                day_number=i,
                date_label=f"Day {i}",
                theme=day_struct["theme"],
                summary=day_struct["summary"],
                activities=acts,
                daily_estimated_cost=daily_cost_str
            ))

        return enforce_zero_repetition(generated_days, request.destination, currency, base_lat, base_lng)
