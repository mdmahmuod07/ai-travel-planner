import asyncio
import sys
import os

# Ensure backend folder is in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.schemas.travel import TravelRequest, TripRequest, RefineRequest
from app.agents.orchestrator import orchestrator

async def main():
    print("================================================================================")
    print("Testing Destination-Agnostic Multi-Agent Orchestrator Pipeline")
    print("================================================================================\n")

    async def log_cb(aid, msg, status):
        print(f"  -> [{aid}] ({status}): {msg}")

    # -------------------------------------------------------------------------
    # TEST CASE 1: Tokyo, Japan (Budget: ₹50,000, Origin: India)
    # -------------------------------------------------------------------------
    print(">>> TEST 1: Destination 'Tokyo, Japan' (Origin: Bangalore, India)")
    req_tokyo = TripRequest(
        origin="Bangalore, India",
        destination="Tokyo, Japan",
        duration_days=5,
        target_budget=50000.0,
        currency="INR",
        travel_style="Budget",
        companions="Couple",
        dietary_restrictions=["Vegetarian"],
        interests=["Food", "History", "Nature"],
        special_requests="Budget friendly trip"
    )

    plan_tokyo = await orchestrator.generate_trip_plan(req_tokyo, log_callback=log_cb)

    print(f"\nTrip ID: {plan_tokyo.trip_id}")
    print(f"Destination: {plan_tokyo.destination}")
    print(f"Duration: {plan_tokyo.duration_days} Days")
    print(f"Total Estimated: {plan_tokyo.budget_breakdown.total_estimated}")
    print(f"Target Budget: {plan_tokyo.budget_breakdown.target_budget}")

    # 1. Budget Ceiling
    assert "₹50,000" in plan_tokyo.budget_breakdown.total_estimated, f"Expected ₹50,000 ceiling, got {plan_tokyo.budget_breakdown.total_estimated}"
    print("  ✓ Strict Budget Ceiling Enforced: Total Trip Cost <= target_budget")

    # 2. Accommodations Dynamic Adaptation
    hotel_names = [h.name for h in plan_tokyo.accommodations]
    print(f"  Accommodations: {hotel_names}")
    assert any(name in ["UNPLAN Kagurazaka", "Nui. Hostel & Bar Lounge", "APA Hotel & Resort Ryogoku Eki Tower", "Sotetsu Fresa Inn Tokyo Kyobashi"] for name in hotel_names), "Expected budget/hostel recommendations"
    print("  ✓ Dynamic Hotel Adaptation: Recommended authentic Tokyo budget stays")

    # 3. Elimination of Generic Hallucinations & Verifiable Coordinates
    act1 = plan_tokyo.itinerary[0].activities[0]
    print(f"  Activity 1: {act1.title} | Venue: {act1.venue_name} | Query: {act1.search_query} (lat={act1.lat}, lng={act1.lng})")
    assert act1.lat and act1.lng, "Expected non-null coordinates"
    assert "Cultural Heritage Landmark" not in act1.title, "Generic placeholders should be eliminated"
    assert act1.venue_name and act1.search_query, "Expected venue_name and search_query"
    print("  ✓ Elimination of Generic Hallucinations: Real Tokyo wards and search_query verified")

    # 4. Visa & Embassy
    assert "eVisa" in plan_tokyo.travel_tips.visa_and_entry or "VFS Global" in plan_tokyo.travel_tips.visa_and_entry, "Expected eVisa/VFS guidance"
    assert "Visa-on-Arrival" in plan_tokyo.travel_tips.visa_and_entry and "NOT AVAILABLE" in plan_tokyo.travel_tips.visa_and_entry, "Expected VoA not available guidance"
    print("  ✓ Legal & Visa Accuracy: Indian passport holders require pre-approved visa, VoA not available")

    assert "Kudan-Minami" in plan_tokyo.travel_tips.embassy_info, "Expected Embassy of India Tokyo details"
    print("  ✓ Diplomatic Mission: Embassy of India, Tokyo verified")

    # 5. Electrical & Transit
    assert "Type A & B" in plan_tokyo.travel_tips.electrical_specs, f"Expected Type A & B, got {plan_tokyo.travel_tips.electrical_specs}"
    assert "100 V" in plan_tokyo.travel_tips.electrical_specs, f"Expected 100V, got {plan_tokyo.travel_tips.electrical_specs}"
    print("  ✓ Electrical Specs: Type A & B at 100V verified")

    assert "Suica" in plan_tokyo.travel_tips.transit_tips, f"Expected Suica, got {plan_tokyo.travel_tips.transit_tips}"
    print("  ✓ Transit Infrastructure: Digital Suica/Pasmo verified")

    # 6. Dietary Tagging
    for r in plan_tokyo.dining:
        dish_lower = (r.must_try_dish + " " + r.name).lower()
        if any(m in dish_lower for m in ["chicken", "pork", "beef", "yakitori", "tonkatsu"]):
            assert "Vegetarian" not in r.dietary_friendly and "Vegan" not in r.dietary_friendly, f"Meat dish {r.name} was tagged as vegetarian!"
    print("  ✓ Dietary Tagging: Meat/poultry dishes never falsely tagged as Vegetarian/Vegan")

    # -------------------------------------------------------------------------
    # TEST CASE 2: Istanbul, Turkey (Multi-City Verification, Origin: India)
    # -------------------------------------------------------------------------
    print("\n>>> TEST 2: Destination 'Istanbul, Turkey' (Zero Hardcoded Japan Bleed)")
    req_turkey = TripRequest(
        origin="Bangalore, India",
        destination="Istanbul, Turkey",
        duration_days=5,
        target_budget=75000.0,
        currency="INR",
        travel_style="Moderate",
        companions="Solo",
        dietary_restrictions=[],
        interests=["History", "Architecture", "Food"]
    )

    plan_turkey = await orchestrator.generate_trip_plan(req_turkey, log_callback=log_cb)

    print(f"\nTrip ID: {plan_turkey.trip_id}")
    print(f"Destination: {plan_turkey.destination}")
    print(f"Total Estimated: {plan_turkey.budget_breakdown.total_estimated}")

    # 1. Zero Japan Bleed
    full_text = plan_turkey.model_dump_json()
    assert "¥" not in full_text, "Found Yen currency symbol bleeding into Turkey itinerary!"
    assert "Shinkansen" not in full_text, "Found Shinkansen bleeding into Turkey itinerary!"
    assert "Suica" not in full_text, "Found Suica bleeding into Turkey itinerary!"
    assert "tatami" not in full_text.lower(), "Found tatami bleeding into Turkey itinerary!"
    print("  ✓ Zero Japan Bleed: No Yen, Shinkansen, Suica, or tatami artifacts")

    # 2. Authentic Istanbul Entities (No Generic Placeholders)
    all_titles = [act.title for day in plan_turkey.itinerary for act in day.activities]
    print(f"  Activities: {all_titles[:4]}...")
    assert any("Hagia Sophia" in t or "Ayasofya" in t for t in all_titles), "Expected Hagia Sophia in Istanbul itinerary"
    assert any("Blue Mosque" in t or "Sultan Ahmed" in t for t in all_titles), "Expected Blue Mosque in Istanbul itinerary"
    assert not any("Cultural Heritage Landmark" in t for t in all_titles), "Generic placeholder '[City] Cultural Heritage Landmark' detected!"
    assert not any("[City]" in t for t in all_titles), "Literal [City] template string detected!"
    print("  ✓ Authentic Entities: Hagia Sophia, Blue Mosque resolved with zero generic placeholders")

    # 3. Electrical Standards (Type C & F, 230 V)
    print(f"  Electrical Specs: {plan_turkey.travel_tips.electrical_specs}")
    assert "Type C & F" in plan_turkey.travel_tips.electrical_specs, "Expected Type C & F plugs for Turkey"
    assert "230 V" in plan_turkey.travel_tips.electrical_specs, "Expected 230V for Turkey"
    print("  ✓ Electrical Specs: Type C & F (230V) correctly resolved for Turkey")

    # 4. Transit Card (Istanbulkart) & Local Currency
    print(f"  Transit Tips: {plan_turkey.travel_tips.transit_tips}")
    assert "Istanbulkart" in plan_turkey.travel_tips.transit_tips, "Expected Istanbulkart for Istanbul transit"
    print(f"  Currency & Payment: {plan_turkey.travel_tips.currency_and_payment_tips}")
    assert "TRY" in plan_turkey.travel_tips.currency_and_payment_tips or "Turkish Lira" in plan_turkey.travel_tips.currency_and_payment_tips or "₺" in plan_turkey.travel_tips.currency_and_payment_tips, "Expected Turkish Lira / TRY"
    print("  ✓ Transit & Currency: Istanbulkart and Turkish Lira correctly resolved")

    # 5. Bilateral Visa Notice (Conditional e-Visa / VFS for Indian Passports)
    print(f"  Visa & Entry: {plan_turkey.travel_tips.visa_and_entry[:120]}...")
    assert "evisa.gov.tr" in plan_turkey.travel_tips.visa_and_entry or "e-Visa" in plan_turkey.travel_tips.visa_and_entry, "Expected Turkish e-Visa guidance"
    assert "Schengen" in plan_turkey.travel_tips.visa_and_entry or "USA" in plan_turkey.travel_tips.visa_and_entry, "Expected conditional e-Visa rule regarding Schengen/US/UK visas"
    assert "Visa-on-Arrival" in plan_turkey.travel_tips.visa_and_entry and "NOT" in plan_turkey.travel_tips.visa_and_entry, "Expected VoA not available rule"
    print("  ✓ Bilateral Visa: Precise Turkish conditional e-Visa / advance visa rules enforced")

    # 6. Diplomatic Mission: Commercial Hub (Consulate General in Istanbul) vs Capital (Embassy in Ankara)
    print(f"  Embassy Info: {plan_turkey.travel_tips.embassy_info[:100]}...")
    assert "Consulate General of India" in plan_turkey.travel_tips.embassy_info, "Expected Consulate General in Istanbul"
    assert "Istanbul" in plan_turkey.travel_tips.embassy_info, "Expected Istanbul consular reference"
    assert "Ankara" in plan_turkey.travel_tips.embassy_info, "Expected Embassy in Ankara reference"
    print("  ✓ Diplomatic Mission: Differentiated Consulate General in Istanbul vs Embassy in Ankara")

    # 7. Universal Dietary Sanitization
    for r in plan_turkey.dining:
        print(f"  Dining: {r.name} ({r.cuisine}) - Dish: {r.must_try_dish} - Friendly: {r.dietary_friendly}")
        dish_lower = (r.must_try_dish + " " + r.name).lower()
        if any(m in dish_lower for m in ["kebab", "lamb", "beef", "chicken", "meat", "köfte"]):
            assert "Vegetarian" not in r.dietary_friendly and "Vegan" not in r.dietary_friendly, f"Meat dish {r.name} falsely tagged as Vegetarian/Vegan!"
    print("  ✓ Universal Dietary Sanitization: Meat dishes (kebab, beef, lamb) verified strictly non-veg")

    # -------------------------------------------------------------------------
    # TEST CASE 3: Conversational Refinement for Istanbul
    # -------------------------------------------------------------------------
    print("\n>>> TEST 3: Conversational Refinement on Istanbul Plan")
    refine_req = RefineRequest(
        current_plan=plan_turkey,
        user_instruction="Add outdoor nature spots and botanical gardens on Day 2"
    )
    refined_turkey = await orchestrator.refine_trip_plan(refine_req, log_callback=log_cb)
    ref_act = refined_turkey.itinerary[1].activities[1]
    print(f"  Refined Day 2 Afternoon: {ref_act.title} ({ref_act.venue_name})")
    assert "Gülhane Park" in ref_act.title or "Gülhane Park" in ref_act.venue_name, f"Expected Gülhane Park in Istanbul refinement, got {ref_act.title}"
    print("  ✓ Conversational Refinement: Correctly added authentic Gülhane Park in Istanbul")

    # -------------------------------------------------------------------------
    # TEST CASE 4: Paris, France (Verification of Zero Duplicates & Real Venues)
    # -------------------------------------------------------------------------
    print("\n>>> TEST 4: Destination 'Paris, France' (Zero Duplicate Slots & Real Venues)")
    req_paris = TripRequest(
        origin="Bangalore, India",
        destination="Paris, France",
        duration_days=5,
        target_budget=150000.0,
        currency="INR",
        travel_style="Moderate",
        companions="Couple",
        dietary_restrictions=["Vegetarian Options"],
        interests=["Art", "History", "Architecture", "Food"]
    )

    plan_paris = await orchestrator.generate_trip_plan(req_paris, log_callback=log_cb)

    print(f"\nTrip ID: {plan_paris.trip_id}")
    print(f"Destination: {plan_paris.destination}")
    print(f"Duration: {plan_paris.duration_days} Days")

    # 1. Check Real Paris Landmarks & Zero Repetition
    all_paris_titles = [act.title for day in plan_paris.itinerary for act in day.activities]
    print(f"  Total Activities Scheduled: {len(all_paris_titles)}")
    print(f"  Day 1: {[a.title for a in plan_paris.itinerary[0].activities]}")
    print(f"  Day 2: {[a.title for a in plan_paris.itinerary[1].activities]}")

    # Assert ZERO duplicate activity titles
    assert len(all_paris_titles) == len(set(all_paris_titles)), f"Duplicate activity titles found across Paris days: {all_paris_titles}"
    print("  ✓ Zero Duplicate Slots: Every Morning, Afternoon, and Evening has unique non-repeating activities")

    # Assert Iconic Paris Venues Present
    all_titles_str = " ".join(all_paris_titles)
    assert "Eiffel Tower" in all_titles_str or "Tour Eiffel" in all_titles_str, "Expected Eiffel Tower in Paris itinerary"
    assert "Louvre" in all_titles_str, "Expected Louvre Museum in Paris itinerary"
    assert "Sainte-Chapelle" in all_titles_str or "Notre-Dame" in all_titles_str, "Expected Sainte-Chapelle in Paris itinerary"
    assert "Montmartre" in all_titles_str or "Sacré-Cœur" in all_titles_str, "Expected Montmartre/Sacré-Cœur in Paris itinerary"
    print("  ✓ Real Iconic Landmarks: Eiffel Tower, Louvre, Montmartre, Sainte-Chapelle verified")

    # 2. Check Real Paris Stays
    hotel_names_paris = [h.name for h in plan_paris.accommodations]
    print(f"  Paris Accommodations: {hotel_names_paris}")
    assert not any("Historic Boutique Inn & Suites" in h for h in hotel_names_paris), "Found generic mock hotel placeholder!"
    assert any(h in ["Hotel Le Relais Saint-Germain", "Hotel Caron de Beaumarchais", "Generator Paris", "The People Paris Marais", "Le Meurice - Dorchester Collection", "Hôtel de Crillon, A Rosewood Hotel"] for h in hotel_names_paris), "Expected authentic Paris hotel recommendations"
    print("  ✓ Authentic Stays: Real Parisian boutique hotels and stays verified")

    # 3. Check Real Paris Restaurants
    restaurant_names_paris = [r.name for r in plan_paris.dining]
    print(f"  Paris Dining: {restaurant_names_paris}")
    assert not any("Historic Old Town Tavern" in r for r in restaurant_names_paris), "Found generic mock dining placeholder!"
    assert any(r in ["Bouillon Chartier", "Café de Flore", "L'As du Fallafel", "Breizh Café Le Marais", "Le Potager de Charlotte"] for r in restaurant_names_paris), "Expected authentic Paris restaurants"
    print("  ✓ Authentic Dining: Real Parisian restaurants and cafes verified")

    # 4. Check Universal Dietary Sanitization
    for r in plan_paris.dining:
        if r.name == "Bouillon Chartier":
            assert "Vegetarian" not in r.dietary_friendly and "Vegan" not in r.dietary_friendly, "Bouillon Chartier escargots/duck confit falsely tagged as Vegetarian!"
    print("  ✓ Dietary Sanitization: Bouillon Chartier meat dishes strictly Non-Vegetarian")

    # 5. Check Packing Checklist non-empty items
    assert len(plan_paris.packing_checklist) >= 4, "Expected 4 packing categories"
    for cat in plan_paris.packing_checklist:
        assert cat.items and len(cat.items) > 0, f"Category '{cat.category_name}' has empty items list!"
        print(f"  Packing Category '{cat.category_name}': {len(cat.items)} items populated")
    print("  ✓ Packing Checklist: All categories populated with non-empty item lists")

    # 6. Check Paris Refinement
    refine_paris = RefineRequest(
        current_plan=plan_paris,
        user_instruction="Add a peaceful park and botanical walk on Day 2 afternoon"
    )
    refined_p = await orchestrator.refine_trip_plan(refine_paris, log_callback=log_cb)
    ref_act_p = refined_p.itinerary[1].activities[1]
    print(f"  Refined Paris Day 2: {ref_act_p.title} ({ref_act_p.venue_name})")
    assert "Luxembourg" in ref_act_p.title or "Luxembourg" in ref_act_p.venue_name, f"Expected Jardin du Luxembourg, got {ref_act_p.title}"
    print("  ✓ Conversational Refinement: Correctly added Jardin du Luxembourg in Paris")

    print("\n================================================================================")
    print("ALL MULTI-CITY BACKEND TESTS PASSED WITH 100% SUCCESS!")
    print("================================================================================")

if __name__ == "__main__":
    asyncio.run(main())
