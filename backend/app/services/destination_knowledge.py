"""
Destination-Agnostic Knowledge Resolver Engine.
Provides factual ground-truth data for global destinations:
- Genuine landmarks, coordinates, and authentic neighborhoods
- Real-world dining with strict universal dietary tagging
- Realistic accommodations across budget, moderate, and luxury tiers
- Official electrical standards (plug types, voltage, frequency)
- Local currency & contactless transit card infrastructure
- Bilateral visa evaluation (Origin country vs Destination country)
- Bilateral diplomatic mission resolution (Embassy in capital vs Consulate General in commercial hubs)
"""

from typing import Dict, Any, List, Optional, Tuple

# Official electrical standards by country/region
ELECTRICAL_STANDARDS: Dict[str, Dict[str, str]] = {
    "turkey": {
        "plugs": "Type C & F (Europlug & Schuko)",
        "voltage": "230 V",
        "frequency": "50 Hz",
        "description": "Standard European two-round-pin plugs (Type C and grounded Type F). Compatible with most European electronics."
    },
    "japan": {
        "plugs": "Type A & B (Two parallel flat pins)",
        "voltage": "100 V",
        "frequency": "50 Hz (Eastern/Tokyo) / 60 Hz (Western/Osaka)",
        "description": "Two flat parallel prongs (Type A ungrounded, Type B with ground pin). Note: 100V is lower than European/Indian 230V."
    },
    "united kingdom": {
        "plugs": "Type G (British three-rectangular-pin)",
        "voltage": "230 V",
        "frequency": "50 Hz",
        "description": "Three rectangular prongs in a triangular pattern with safety shutter."
    },
    "uk": {
        "plugs": "Type G (British three-rectangular-pin)",
        "voltage": "230 V",
        "frequency": "50 Hz",
        "description": "Three rectangular prongs in a triangular pattern with safety shutter."
    },
    "france": {
        "plugs": "Type C & E (Europlug & French type)",
        "voltage": "230 V",
        "frequency": "50 Hz",
        "description": "Two round pins with male grounding pin (Type E) and standard Type C."
    },
    "italy": {
        "plugs": "Type C, F & L",
        "voltage": "230 V",
        "frequency": "50 Hz",
        "description": "Standard European Type C and three-in-line Type L sockets."
    },
    "united states": {
        "plugs": "Type A & B",
        "voltage": "120 V",
        "frequency": "60 Hz",
        "description": "Two flat parallel blades with optional grounding pin (Type B)."
    },
    "usa": {
        "plugs": "Type A & B",
        "voltage": "120 V",
        "frequency": "60 Hz",
        "description": "Two flat parallel blades with optional grounding pin (Type B)."
    },
    "uae": {
        "plugs": "Type G (British standard) & Type C/D",
        "voltage": "230 V",
        "frequency": "50 Hz",
        "description": "British standard three-pin Type G is most common across hotels and residences."
    },
    "united arab emirates": {
        "plugs": "Type G (British standard)",
        "voltage": "230 V",
        "frequency": "50 Hz",
        "description": "British standard three-pin Type G is most common across hotels and residences."
    },
    "indonesia": {
        "plugs": "Type C & F",
        "voltage": "230 V",
        "frequency": "50 Hz",
        "description": "Two round pins (European standard Type C and grounded Type F)."
    },
    "india": {
        "plugs": "Type C, D & M",
        "voltage": "230 V",
        "frequency": "50 Hz",
        "description": "Three round pins in triangle configuration (large Type M or small Type D)."
    },
    "germany": {
        "plugs": "Type C & F",
        "voltage": "230 V",
        "frequency": "50 Hz",
        "description": "Standard European Schuko grounded plugs."
    },
    "spain": {
        "plugs": "Type C & F",
        "voltage": "230 V",
        "frequency": "50 Hz",
        "description": "Standard European Schuko grounded plugs."
    },
    "netherlands": {
        "plugs": "Type C & F",
        "voltage": "230 V",
        "frequency": "50 Hz",
        "description": "Standard European Schuko grounded plugs."
    },
    "singapore": {
        "plugs": "Type G (British standard)",
        "voltage": "230 V",
        "frequency": "50 Hz",
        "description": "Standard UK three-rectangular-pin plug."
    },
    "thailand": {
        "plugs": "Type A, B, C & O",
        "voltage": "220 V",
        "frequency": "50 Hz",
        "description": "Universal sockets accepting flat two-pin and round two-pin plugs."
    },
    "australia": {
        "plugs": "Type I (Two angled flat pins)",
        "voltage": "230 V",
        "frequency": "50 Hz",
        "description": "Two inverted V-shaped flat blades with optional vertical ground blade."
    }
}

# Local currency and contactless transit infrastructure
LOCAL_TRANSIT_AND_CURRENCY: Dict[str, Dict[str, str]] = {
    "istanbul": {
        "country": "Turkey",
        "currency_name": "Turkish Lira",
        "currency_code": "TRY",
        "currency_symbol": "₺",
        "transit_card": "Istanbulkart",
        "transit_details": "Istanbulkart is the universal contactless reloadable smart card required for all public transit across Istanbul: Metro, Tram (T1), Marmaray cross-continental rail, public Şehir Hatları Bosphorus ferries, funiculars, and Metrobus. Available and reloadable with cash or card at yellow/blue Biletmatik kiosks located at all stations and ferry piers."
    },
    "turkey": {
        "country": "Turkey",
        "currency_name": "Turkish Lira",
        "currency_code": "TRY",
        "currency_symbol": "₺",
        "transit_card": "City Transit Card (e.g., Istanbulkart in Istanbul, Ankarakart in Ankara)",
        "transit_details": "Major Turkish cities utilize dedicated contactless smart cards (Istanbulkart in Istanbul, Ankarakart in Ankara, İzmirim Kart in İzmir). Contactless bank cards and cash are also widely accepted for intercity coach and taxi transit."
    },
    "tokyo": {
        "country": "Japan",
        "currency_name": "Japanese Yen",
        "currency_code": "JPY",
        "currency_symbol": "¥",
        "transit_card": "Digital Suica / Pasmo (Apple/Google Wallet)",
        "transit_details": "Digital Suica or Pasmo card added directly to your smartphone's digital wallet for seamless contactless tapping across Tokyo Metro, JR East lines, private railways, buses, and station vending machines."
    },
    "japan": {
        "country": "Japan",
        "currency_name": "Japanese Yen",
        "currency_code": "JPY",
        "currency_symbol": "¥",
        "transit_card": "IC Card (Suica, Pasmo, Icoca)",
        "transit_details": "National IC cards (Suica, Pasmo in Kanto; Icoca in Kansai) are mutually interoperable across virtually all trains, subways, and buses throughout Japan."
    },
    "paris": {
        "country": "France",
        "currency_name": "Euro",
        "currency_code": "EUR",
        "currency_symbol": "€",
        "transit_card": "Navigo Easy / Île-de-France Mobilités App",
        "transit_details": "Navigo Easy rechargeable contactless card or smartphone NFC via the Île-de-France Mobilités app for all Métro lines, RER suburban trains within Paris, trams, and RATP buses."
    },
    "london": {
        "country": "United Kingdom",
        "currency_name": "British Pound",
        "currency_code": "GBP",
        "currency_symbol": "£",
        "transit_card": "Contactless Bank Card / Oyster Card",
        "transit_details": "Direct contactless bank card/smartphone pay-as-you-go or physical Visitor Oyster Card for the London Underground (Tube), Elizabeth Line, Overground, DLR, and red double-decker buses, featuring automatic daily fare capping."
    },
    "new york": {
        "country": "United States",
        "currency_name": "US Dollar",
        "currency_code": "USD",
        "currency_symbol": "$",
        "transit_card": "OMNY (Contactless Tap to Pay) / MetroCard",
        "transit_details": "OMNY contactless tap-to-pay using any debit/credit card or Apple/Google Pay at all subway turnstiles and MTA buses with automatic 7-day fare capping, or traditional magnetic MetroCard."
    },
    "rome": {
        "country": "Italy",
        "currency_name": "Euro",
        "currency_code": "EUR",
        "currency_symbol": "€",
        "transit_card": "Metrebus / Tap & Go",
        "transit_details": "Contactless 'Tap & Go' with your bank card/smartphone or physical BIT integrated ticket (€1.50 for 100 minutes) valid on Rome Metro lines A, B, C and ATAC surface buses and trams."
    },
    "dubai": {
        "country": "United Arab Emirates",
        "currency_name": "UAE Dirham",
        "currency_code": "AED",
        "currency_symbol": "AED",
        "transit_card": "Nol Card (Silver)",
        "transit_details": "RTA Silver Nol Card is the unified contactless smart card required for Dubai Metro (Red and Green lines), Dubai Tram, public RTA buses, and water buses across Dubai Creek."
    },
    "bali": {
        "country": "Indonesia",
        "currency_name": "Indonesian Rupiah",
        "currency_code": "IDR",
        "currency_symbol": "Rp",
        "transit_card": "Ride-Hailing Apps (Grab / Gojek) & Private Driver",
        "transit_details": "Public scheduled transit is limited in Bali. Visitors primarily utilize Grab and Gojek smartphone apps for scooter and car rides, or arrange pre-booked private daily drivers with air-conditioned vehicles for full-day island touring."
    }
}

# Real-world authentic destinations database
AUTHENTIC_DESTINATIONS: Dict[str, Dict[str, Any]] = {
    "istanbul": {
        "city": "Istanbul",
        "country": "Turkey",
        "center_coords": (41.0082, 28.9784),
        "best_time": "April to May (Spring) and September to November (Autumn) offer idyllic temperatures, clear skies, and blooming Bosphorus scenery without midsummer heat.",
        "overview": "Straddling Europe and Asia across the historic Bosphorus strait, Istanbul is a breathtaking tapestry of Roman, Byzantine, and Ottoman imperial heritage. From the soaring dome of Hagia Sophia and the labyrinthine Grand Bazaar to the vibrant rooftop cafes of Beyoğlu and the lively seaside promenades of Kadıköy, the city offers unmatched cultural, culinary, and architectural richness.",
        "districts": ["Sultanahmet", "Fatih", "Beyoğlu", "Karaköy", "Beşiktaş", "Kadıköy", "Ortaköy", "Üsküdar"],
        "landmarks": [
            {
                "title": "Hagia Sophia Grand Mosque (Ayasofya)",
                "venue_name": "Hagia Sophia (Ayasofya-i Kebir Cami-i Şerifi)",
                "neighborhood": "Sultanahmet, Fatih",
                "location": "Sultanahmet Square, Fatih, Istanbul",
                "category": "History & Architecture",
                "search_query": "Hagia Sophia, Sultanahmet, Istanbul",
                "duration": "2.5 hours",
                "lat": 41.0086,
                "lng": 28.9802,
                "description": "Constructed in 537 AD as the imperial cathedral of the Byzantine Empire and later converted into an Ottoman imperial mosque, marvel at its 55-meter soaring dome, marble nave, and Christian mosaics.",
                "tips": "Modest attire required: women must cover head/shoulders and shoes must be removed before carpeted areas. Foreign tourist ticket line is separate on the southern flank."
            },
            {
                "title": "Blue Mosque (Sultan Ahmed Mosque)",
                "venue_name": "Sultan Ahmed Mosque",
                "neighborhood": "Sultanahmet, Fatih",
                "location": "Atmeydanı Cd. No:7, Fatih, Istanbul",
                "category": "Spiritual & Architectural",
                "search_query": "Blue Mosque, Sultanahmet, Istanbul",
                "duration": "1.5 hours",
                "lat": 41.0054,
                "lng": 28.9768,
                "description": "Famed for its six minarets and over 20,000 hand-painted Iznik blue ceramic tiles depicting tulip and floral motifs, this 17th-century masterpiece stands directly opposite Hagia Sophia.",
                "tips": "Free admission; closed to tourists during five daily prayer times (approx. 30 minutes each) and Friday midday congregation."
            },
            {
                "title": "Topkapi Palace & Imperial Harem",
                "venue_name": "Topkapi Palace (Topkapı Sarayı)",
                "neighborhood": "Cankurtaran, Fatih",
                "location": "Cankurtaran, Fatih, Istanbul",
                "category": "Imperial History",
                "search_query": "Topkapi Palace, Istanbul",
                "duration": "3 hours",
                "lat": 41.0115,
                "lng": 28.9834,
                "description": "The lavish primary administrative headquarters and royal residence of Ottoman sultans for nearly four centuries, showcasing imperial courtyards, the jewel-encrusted Topkapi Dagger, the Spoonmaker's Diamond, and the tiled Harem chambers.",
                "tips": "Combined palace and Harem pass is recommended; walk through the Fourth Courtyard terrace for sweeping panoramic vistas over the Bosphorus and Golden Horn."
            },
            {
                "title": "Basilica Cistern (Yerebatan Sarnıcı)",
                "venue_name": "Basilica Cistern",
                "neighborhood": "Sultanahmet, Fatih",
                "location": "Alemdar, Yerebatan Cd. 1/3, Fatih, Istanbul",
                "category": "Ancient Engineering",
                "search_query": "Basilica Cistern, Sultanahmet, Istanbul",
                "duration": "1.5 hours",
                "lat": 41.0084,
                "lng": 28.9779,
                "description": "An underground subterranean palace supported by 336 marble Corinthian and Ionic columns built by Emperor Justinian I in 532 AD, featuring illuminated shallow waters and upside-down sculpted Medusa head pedestals.",
                "tips": "Book skip-the-line digital tickets in advance to bypass long ticket queues during peak hours."
            },
            {
                "title": "Grand Bazaar & Historical Spice Market",
                "venue_name": "Grand Bazaar (Kapalıçarşı)",
                "neighborhood": "Beyazıt / Eminönü, Fatih",
                "location": "Beyazıt, Fatih, Istanbul",
                "category": "Culture & Shopping",
                "search_query": "Grand Bazaar, Istanbul",
                "duration": "3 hours",
                "lat": 41.0107,
                "lng": 28.9680,
                "description": "One of the oldest and largest covered markets in the world, spanning over 60 covered streets and 4,000 shops selling Turkish lamps, handmade ceramics, kilim rugs, gold jewelry, and aromatic Turkish delight.",
                "tips": "Polite bargaining is expected in the Grand Bazaar; visit the nearby Egyptian Spice Market (Mısır Çarşısı) for fresh saffron, sumac, and Turkish tea blends."
            },
            {
                "title": "Galata Tower & Istiklal Avenue Walk",
                "venue_name": "Galata Tower (Galata Kulesi)",
                "neighborhood": "Bereketzade, Beyoğlu",
                "location": "Bereketzade, Beyoğlu, Istanbul",
                "category": "Panoramic Viewpoint",
                "search_query": "Galata Tower, Beyoğlu, Istanbul",
                "duration": "2.5 hours",
                "lat": 41.0256,
                "lng": 28.9741,
                "description": "A 14th-century medieval stone watchtower erected by the Genoese colony, offering sweeping 360-degree vistas across the Golden Horn, historic peninsula, and Bosphorus strait, followed by a walk down pedestrianized Istiklal Avenue.",
                "tips": "Visit around golden hour for sunset over the minarets of Old Istanbul; ride the historic red T2 heritage tramway along Istiklal Street."
            },
            {
                "title": "Bosphorus Public Sunset Ferry Cruise",
                "venue_name": "Şehir Hatları Bosphorus Ferry Pier",
                "neighborhood": "Eminönü / Karaköy",
                "location": "Eminönü Ferry Terminal, Fatih, Istanbul",
                "category": "Scenic Waterways",
                "search_query": "Eminönü Ferry Terminal, Istanbul",
                "duration": "2 hours",
                "lat": 41.0185,
                "lng": 28.9740,
                "description": "Sail between continents on a classic commuter ferry or scenic Bosphorus cruise, gliding past Ottoman wooden waterfront mansions (yalı), Dolmabahçe Palace, Rumeli Fortress, and beneath suspension bridges.",
                "tips": "Public municipal ferries using Istanbulkart cost only a fraction of private tourist boats and offer the same magnificent views; feed simit bread to circling seagulls on the aft deck."
            },
            {
                "title": "Kadıköy & Moda Asian Side Discovery",
                "venue_name": "Kadıköy Historic Market",
                "neighborhood": "Caferağa, Kadıköy",
                "location": "Caferağa, Kadıköy, Istanbul",
                "category": "Local Life & Gastronomy",
                "search_query": "Kadıköy Market, Moda, Istanbul",
                "duration": "3 hours",
                "lat": 40.9897,
                "lng": 29.0254,
                "description": "Cross the Bosphorus to Istanbul's vibrant Asian side, wandering pedestrianized market streets lined with picklers, cheese mongers, independent bookstores, artisan roasters, and the relaxed Moda seaside promenade.",
                "tips": "Take the ferry from Karaköy or Eminönü to Kadıköy around late afternoon; the return ferry at dusk gives unforgettable skyline views of the illuminated Old City."
            },
            {
                "title": "Süleymaniye Mosque & Mimar Sinan Golden Horn Terrace",
                "venue_name": "Süleymaniye Mosque (Süleymaniye Camii)",
                "neighborhood": "Süleymaniye, Fatih",
                "location": "Prof. Sıddık Sami Onar Cd. No:1, Fatih, Istanbul",
                "category": "Imperial Mosque & Panorama",
                "search_query": "Süleymaniye Mosque, Fatih, Istanbul",
                "duration": "2 hours",
                "lat": 41.0163,
                "lng": 28.9644,
                "description": "Imperial master architect Mimar Sinan's masterpiece crowning the Third Hill of Istanbul, featuring harmonious domed acoustic architecture and panoramic garden terraces overlooking the Golden Horn.",
                "tips": "Visit the tomb garden behind the mosque where Sultan Suleiman the Magnificent and Roxelana (Hürrem Sultan) rest."
            },
            {
                "title": "Dolmabahçe Palace & Bosphorus Waterfront Chambers",
                "venue_name": "Dolmabahçe Palace (Dolmabahçe Sarayı)",
                "neighborhood": "Vişnezade, Beşiktaş",
                "location": "Vişnezade, Dolmabahçe Cd., Beşiktaş, Istanbul",
                "category": "19th-Century Royal Palace",
                "search_query": "Dolmabahçe Palace, Beşiktaş, Istanbul",
                "duration": "2.5 hours",
                "lat": 41.0392,
                "lng": 29.0003,
                "description": "The lavish 19th-century European-style Ottoman imperial palace situated directly on the European Bosphorus shore, featuring the 4.5-ton Bohemian crystal chandelier and the famed Crystal Staircase.",
                "tips": "Daily visitor numbers are capped; arrive in the morning to secure entrance tickets."
            },
            {
                "title": "Chora Church & Byzantine Theodosian Land Walls",
                "venue_name": "Kariye Mosque (Chora Church)",
                "neighborhood": "Dervişali, Fatih",
                "location": "Kariye Cami Sk. No:18, Fatih, Istanbul",
                "category": "Byzantine Mosaics & Ancient Fortifications",
                "search_query": "Chora Church, Fatih, Istanbul",
                "duration": "2 hours",
                "lat": 41.0313,
                "lng": 28.9392,
                "description": "Celebrated worldwide for some of the finest surviving 14th-century late-Byzantine mosaics and frescoes, situated beside the imposing 5th-century stone defensive land walls of Emperor Theodosius II.",
                "tips": "Walk atop the restored section of the nearby Theodosian walls for sweeping views over the Edirnekapı district."
            },
            {
                "title": "Egyptian Spice Bazaar & Rüstem Pasha Tile Mosque",
                "venue_name": "Spice Bazaar (Mısır Çarşısı) & Rüstem Pasha Mosque",
                "neighborhood": "Rüstem Paşa, Fatih",
                "location": "Rüstem Paşa, Erzak Ambarı Sok. No:92, Fatih, Istanbul",
                "category": "Historic Bazaars & Iznik Ceramics",
                "search_query": "Spice Bazaar, Eminönü, Istanbul",
                "duration": "2 hours",
                "lat": 41.0166,
                "lng": 28.9705,
                "description": "An L-shaped 1660 covered market laden with mountains of fragrant sumac, Iranian saffron, Turkish dried figs, and herbal teas, adjacent to Rüstem Pasha Mosque, famous for walls completely covered in supreme 16th-century cobalt Iznik tiles.",
                "tips": "Rüstem Pasha Mosque is tucked on an elevated terrace above street market stalls; look for the unassuming stone stairs."
            },
            {
                "title": "Pierre Loti Hill & Eyüp Historic Teleferik",
                "venue_name": "Pierre Loti Cafe & Eyüp Cable Car",
                "neighborhood": "Eyüp Merkez, Eyüpsultan",
                "location": "İdris Köşkü Cd., Eyüpsultan, Istanbul",
                "category": "Panoramic Viewpoint & Historic Cafe",
                "search_query": "Pierre Loti Hill, Eyüpsultan, Istanbul",
                "duration": "2 hours",
                "lat": 41.0543,
                "lng": 28.9344,
                "description": "Named after the 19th-century French naval officer and romantic novelist Pierre Loti, ride the TF2 municipal aerial tramway to the hill's open-air terrace for Turkish coffee overlooking the Golden Horn inlet.",
                "tips": "Visit during the late afternoon to hear the evocative call to prayer echo across the water from surrounding historic minarets."
            },
            {
                "title": "Galata Mevlevi Lodge & Whirling Dervishes Hall",
                "venue_name": "Galata Mevlevihanesi Museum",
                "neighborhood": "Şahkulu, Beyoğlu",
                "location": "Galip Dede Cd. No:15, Beyoğlu, Istanbul",
                "category": "Sufi Culture & Musical Heritage",
                "search_query": "Galata Mevlevihanesi Museum, Beyoğlu, Istanbul",
                "duration": "1.5 hours",
                "lat": 41.0284,
                "lng": 28.9749,
                "description": "Istanbul's oldest Mevlevi Sufi lodge founded in 1491, housing the historic octagonal wooden semahane hall where Mevlevi dervishes perform sacred Sema ceremonies, surrounded by Ottoman musical manuscripts and peaceful dervish graves.",
                "tips": "Located at the quiet southern foot of İstiklal Street beside Tünel station."
            },
            {
                "title": "Balat & Fener Historic Waterfront Heritage Walk",
                "venue_name": "Balat & Fener Heritage Quarter",
                "neighborhood": "Balat, Fatih",
                "location": "Yıldırım Cd., Balat, Fatih, Istanbul",
                "category": "Historic Colorful Architecture",
                "search_query": "Balat, Fatih, Istanbul",
                "duration": "2.5 hours",
                "lat": 41.0315,
                "lng": 28.9482,
                "description": "The historical Greek and Jewish quarter along the Golden Horn, famous for its steep cobblestone slopes lined with pastel-colored timber houses, antique auction houses, vintage cafes, and the towering red-brick Phanar Greek Orthodox College.",
                "tips": "Stroll up Kiremit Street for the iconic postcard perspective of the pastel wooden facades."
            }
        ],
        "dining": [
            {
                "name": "Çiya Sofrası",
                "cuisine": "Authentic Anatolian Regional & Meze Cuisine",
                "meal_type": "Lunch / Dinner",
                "neighborhood": "Caferağa, Kadıköy",
                "price_range": "₺400 - ₺800",
                "must_try_dish": "Vast open meze counter featuring dried eggplant dolma, muhammara walnut dip, sour cherry lamb kebab, or seasonal wild herb stews",
                "dietary_friendly": ["Vegetarian Options", "Halal"],
                "lat": 40.9891,
                "lng": 29.0248
            },
            {
                "name": "Pandeli Restaurant",
                "cuisine": "Historic Ottoman Palace Cuisine",
                "meal_type": "Lunch",
                "neighborhood": "Eminönü, Fatih (Inside Spice Bazaar Upper Floor)",
                "price_range": "₺800 - ₺1,600",
                "must_try_dish": "Hünkar Beğendi (Sultan's Delight - tender slow-cooked beef over creamy roasted eggplant purée) & baked aubergine börek",
                "dietary_friendly": ["Non-Vegetarian", "Meat"],
                "lat": 41.0166,
                "lng": 28.9705
            },
            {
                "name": "Hafiz Mustafa 1864",
                "cuisine": "Historic Ottoman Confectionery & Patisserie",
                "meal_type": "Breakfast / Dessert & Tea",
                "neighborhood": "Sirkeci / Sultanahmet, Fatih",
                "price_range": "₺200 - ₺500",
                "must_try_dish": "Artisan Antep pistachio baklava with buffalo milk kaymak, pomegranate Turkish delight, and traditional Turkish tea",
                "dietary_friendly": ["Vegetarian"],
                "lat": 41.0142,
                "lng": 28.9774
            },
            {
                "name": "Zencefil / Bi Nevi Deli",
                "cuisine": "Plant-Based & Vegetarian Mediterranean Kitchen",
                "meal_type": "Lunch / Healthy Casual",
                "neighborhood": "Beyoğlu / Gümüşsuyu",
                "price_range": "₺350 - ₺650",
                "must_try_dish": "Red lentil soup (Mercimek Çorbası), warm hummus with pine nuts, stuffed zucchini flowers, and vegan Turkish manti dumplings",
                "dietary_friendly": ["Vegan", "Vegetarian", "Gluten-Free Options"],
                "lat": 41.0362,
                "lng": 28.9868
            },
            {
                "name": "Dürümzade",
                "cuisine": "Traditional Charcoal Grilled Wraps (Ocakbaşı)",
                "meal_type": "Evening / Casual Dinner",
                "neighborhood": "Hüseyinağa, Beyoğlu",
                "price_range": "₺250 - ₺450",
                "must_try_dish": "Charcoal-grilled spiced Adana minced lamb kebab wrapped in thin lavash bread brushed with chili and sumac herbs",
                "dietary_friendly": ["Non-Vegetarian", "Meat"],
                "lat": 41.0345,
                "lng": 28.9790
            }
        ],
        "hotels": {
            "budget": [
                {
                    "name": "Cheers Hostel",
                    "type": "Boutique Hostel & Rooftop Guesthouse",
                    "neighborhood": "Sultanahmet, Fatih",
                    "rating": "4.8 / 5",
                    "why_recommended": "Consistently ranked among Europe's best hostels, featuring an open-air rooftop bar with direct unobstructed views of Hagia Sophia, walking distance to all imperial sites.",
                    "lat": 41.0097,
                    "lng": 28.9772
                },
                {
                    "name": "Antique Hostel & Guesthouse",
                    "type": "Budget Guesthouse & Private Rooms",
                    "neighborhood": "Cankurtaran, Sultanahmet",
                    "rating": "4.6 / 5",
                    "why_recommended": "Clean, comfortable private rooms and dorms with a sunny rooftop terrace overlooking the Marmara Sea, just a 5-minute stroll from Blue Mosque.",
                    "lat": 41.0048,
                    "lng": 28.9796
                }
            ],
            "moderate": [
                {
                    "name": "Sirkeci Mansion Hotel",
                    "type": "Traditional Ottoman Boutique Hotel",
                    "neighborhood": "Sirkeci, Fatih",
                    "rating": "4.9 / 5",
                    "why_recommended": "Celebrated for authentic Turkish hospitality, complimentary Turkish cooking classes, an indoor spa pool with hammam, and a quiet location beside Gülhane Park.",
                    "lat": 41.0135,
                    "lng": 28.9775
                },
                {
                    "name": "Hotel Sultania Boutique Class",
                    "type": "Heritage Ottoman Boutique Hotel",
                    "neighborhood": "Sirkeci, Fatih",
                    "rating": "4.8 / 5",
                    "why_recommended": "Each luxury room is uniquely themed after an Ottoman sultana with hand-painted ceilings, authentic Iznik tiles, and rooftop Bosphorus views.",
                    "lat": 41.0130,
                    "lng": 28.9772
                }
            ],
            "luxury": [
                {
                    "name": "Çırağan Palace Kempinski Istanbul",
                    "type": "5-Star Imperial Ottoman Palace Hotel",
                    "neighborhood": "Yıldız, Beşiktaş",
                    "rating": "4.9 / 5",
                    "why_recommended": "The only Ottoman imperial palace and hotel located directly on the Bosphorus, boasting historic marble colonnades, world-class butler service, and an infinity pool reflecting the strait.",
                    "lat": 41.0428,
                    "lng": 29.0163
                },
                {
                    "name": "Four Seasons Hotel Istanbul at Sultanahmet",
                    "type": "5-Star Heritage Luxury Hotel",
                    "neighborhood": "Sultanahmet, Fatih",
                    "rating": "4.9 / 5",
                    "why_recommended": "A century-old neoclassical palace enclosing a lush courtyard garden, offering unmatched five-star tranquility in the heart of Old Istanbul, steps from Hagia Sophia.",
                    "lat": 41.0075,
                    "lng": 28.9813
                }
            ]
        }
    },
    "tokyo": {
        "city": "Tokyo",
        "country": "Japan",
        "center_coords": (35.6762, 139.6503),
        "best_time": "Late March to April (Cherry Blossom season) or October to November (Autumn foliage) offer mild temperatures and vibrant outdoor scenery.",
        "overview": "Tokyo is an exhilarating metropolis seamlessly juxtaposing ancient temple sanctuaries and ultramodern neon skylines. From Asakusa's historic Senso-ji temple and Meiji Jingu's tranquil forested shrine to Shibuya's bustling scramble crossing and Akihabara's electronic subculture, Tokyo delivers unrivaled urban excitement, world-class transit, and exquisite culinary craftsmanship.",
        "districts": ["Shinjuku", "Shibuya", "Taito (Asakusa/Ueno)", "Chiyoda", "Minato", "Chuo (Ginza/Tsukiji)", "Harajuku"],
        "landmarks": [
            {
                "title": "Senso-ji Ancient Temple & Nakamise Dori",
                "venue_name": "Sensō-ji (金龍山浅草寺)",
                "neighborhood": "Asakusa, Taito Ward",
                "location": "2-3-1 Asakusa, Taito City, Tokyo",
                "category": "Historic & Spiritual",
                "search_query": "Sensō-ji Temple, Asakusa, Tokyo",
                "duration": "2.5 hours",
                "lat": 35.7148,
                "lng": 139.7967,
                "description": "Tokyo's oldest and most revered Buddhist temple dedicated to Bodhisattva Kannon, entered through the monumental Kaminarimon (Thunder Gate) and vibrant Nakamise-dori shopping lane.",
                "tips": "Visit in the early morning before 9 AM to experience tranquil incense rituals at the Joukouro burner before tour buses arrive."
            },
            {
                "title": "Meiji Jingu Sacred Forest Shrine",
                "venue_name": "Meiji Jingū (明治神宮)",
                "neighborhood": "Yoyogikamizonocho, Shibuya Ward",
                "location": "1-1 Yoyogikamizonocho, Shibuya City, Tokyo",
                "category": "Heritage & Nature",
                "search_query": "Meiji Jingu Shrine, Harajuku, Tokyo",
                "duration": "2 hours",
                "lat": 35.6764,
                "lng": 139.6993,
                "description": "Shinto imperial shrine nestled within 170 acres of evergreen sacred forest comprising over 100,000 donated trees, offering deep meditative serenity moments away from Harajuku.",
                "tips": "Bow once upon entering under the towering cypress Torii gate and cleanse your hands and mouth at the Temizuya water pavilion."
            },
            {
                "title": "Tsukiji Outer Market Epicurean Discovery",
                "venue_name": "Tsukiji Outer Market (築地場外市場)",
                "neighborhood": "Tsukiji, Chuo Ward",
                "location": "4-16-2 Tsukiji, Chuo City, Tokyo",
                "category": "Culinary & Culture",
                "search_query": "Tsukiji Outer Market, Chuo, Tokyo",
                "duration": "2.5 hours",
                "lat": 35.6655,
                "lng": 139.7708,
                "description": "A historic culinary bazaar featuring hundreds of specialty stalls serving fresh sashimi bowls, dashi tamagoyaki rolled omelettes, matcha desserts, and hand-forged Japanese kitchen knives.",
                "tips": "Carry cash for stall purchases and eat immediately beside the vendor stall; walking while eating is culturally frowned upon."
            },
            {
                "title": "Shibuya Scramble Crossing & Hachiko Memorial",
                "venue_name": "Shibuya Scramble Crossing",
                "neighborhood": "Dogenzaka, Shibuya Ward",
                "location": "2-2-1 Dogenzaka, Shibuya City, Tokyo",
                "category": "Modern Metropolis",
                "search_query": "Shibuya Scramble Crossing, Shibuya, Tokyo",
                "duration": "2 hours",
                "lat": 35.6595,
                "lng": 139.7005,
                "description": "Experience the pulse of modern Tokyo at the world's busiest pedestrian intersection, overlooked by giant LED video screens and the loyal Akita dog Hachiko bronze statue.",
                "tips": "Head to the Shibuya Sky observation deck or the 2nd-floor Tsutaya Starbucks for panoramic aerial views of the crossing."
            },
            {
                "title": "Akihabara Electric Town & Pop Culture District",
                "venue_name": "Akihabara Electric Town",
                "neighborhood": "Sotokanda, Chiyoda Ward",
                "location": "Sotokanda, Chiyoda City, Tokyo",
                "category": "Pop Culture & Tech",
                "search_query": "Akihabara Electric Town, Chiyoda, Tokyo",
                "duration": "3 hours",
                "lat": 35.6984,
                "lng": 139.7731,
                "description": "The global epicenter of electronics, anime, gaming, and collectible retro hardware, featuring multi-story hobby centers like Mandarake and Radio Kaikan.",
                "tips": "Chuo-dori main avenue becomes a pedestrian-only zone on Sunday afternoons, making neighborhood exploration seamless."
            },
            {
                "title": "Shinjuku Gyoen National Garden & Teahouse",
                "venue_name": "Shinjuku Gyoen National Garden",
                "neighborhood": "Shinjuku, Shinjuku Ward",
                "location": "11 Naitomachi, Shinjuku City, Tokyo",
                "category": "Imperial Gardens & Botany",
                "search_query": "Shinjuku Gyoen, Tokyo",
                "duration": "2.5 hours",
                "lat": 35.6852,
                "lng": 139.7100,
                "description": "Blends Japanese traditional landscape gardening with formal French and English landscape styles across 144 acres, complete with historic glasshouse and serene koi ponds.",
                "tips": "Alcohol is strictly prohibited inside the park; enjoy a bowl of whisked matcha in the Rakuutei teahouse."
            },
            {
                "title": "Tokyo National Museum & Ueno Cultural Park",
                "venue_name": "Tokyo National Museum (東京国立博物館)",
                "neighborhood": "Ueno Park, Taito Ward",
                "location": "13-9 Uenokoen, Taito City, Tokyo",
                "category": "National Treasures & Samurai Armor",
                "search_query": "Tokyo National Museum, Ueno, Tokyo",
                "duration": "3 hours",
                "lat": 35.7188,
                "lng": 139.7765,
                "description": "Japan's oldest and largest national museum, housing over 110,000 cultural artifacts including national treasures, samurai swords and armor, Buddhist sculptures, and ukiyo-e woodblock prints.",
                "tips": "Don't miss the Honkan Japanese Gallery and the tranquil museum garden open during spring and autumn."
            },
            {
                "title": "Roppongi Hills Mori Art Museum & Tokyo City View",
                "venue_name": "Mori Art Museum & Tokyo City View",
                "neighborhood": "Roppongi, Minato Ward",
                "location": "6-10-1 Roppongi, Minato City, Tokyo",
                "category": "Contemporary Art & Panoramic Skyline",
                "search_query": "Mori Art Museum, Roppongi, Tokyo",
                "duration": "2 hours",
                "lat": 35.6605,
                "lng": 139.7292,
                "description": "Pioneering contemporary art institution atop the 53rd floor of Roppongi Hills Mori Tower, offering 360-degree glass vistas of the Tokyo Tower and Shinjuku skyscrapers.",
                "tips": "Visit at dusk to watch Tokyo transition into an endless neon sea."
            },
            {
                "title": "Nezu Shrine & Vermilion Torii Tunnel Walk",
                "venue_name": "Nezu Shrine (根津神社)",
                "neighborhood": "Nezu, Bunkyo Ward",
                "location": "1-28-9 Nezu, Bunkyo City, Tokyo",
                "category": "Historic Shinto Shrine",
                "search_query": "Nezu Shrine, Bunkyo, Tokyo",
                "duration": "1.5 hours",
                "lat": 35.7202,
                "lng": 139.7618,
                "description": "One of Tokyo's oldest shrines founded in 1706 with surviving Edo-period wooden pavilions, featuring a photogenic tunnel of miniature vermilion torii gates winding up the hillside.",
                "tips": "A peaceful, uncrowded spiritual retreat offering deep tranquility compared to central tourist hubs."
            },
            {
                "title": "Yanaka Ginza Historic Shitamachi Promenade",
                "venue_name": "Yanaka Ginza Shopping Street",
                "neighborhood": "Yanaka, Taito Ward",
                "location": "3-13-1 Yanaka, Taito City, Tokyo",
                "category": "Old Edo Nostalgia & Street Food",
                "search_query": "Yanaka Ginza, Taito, Tokyo",
                "duration": "2 hours",
                "lat": 35.7275,
                "lng": 139.7686,
                "description": "A preserved nostalgic pre-war shopping street capturing the traditional Shitamachi downtown atmosphere, renowned for artisanal croquettes, roasted senbei, and neighborhood cats.",
                "tips": "Watch the sunset from the Yuyake Dandan stairs overlooking the bustling pedestrian lane."
            },
            {
                "title": "Imperial Palace East Gardens & Nijubashi Bridge",
                "venue_name": "Imperial Palace East Gardens (皇居東御苑)",
                "neighborhood": "Chiyoda, Chiyoda Ward",
                "location": "1-1 Chiyoda, Chiyoda City, Tokyo",
                "category": "Feudal Castle Ruins & Gardens",
                "search_query": "Imperial Palace East Gardens, Tokyo",
                "duration": "2 hours",
                "lat": 35.6852,
                "lng": 139.7570,
                "description": "Walk the historic grounds of the former Edo Castle, including massive stone foundation walls, the Ninomaru Japanese garden, and double-arched stone Nijubashi bridge.",
                "tips": "Admission is free; collect a plastic entry token at the gate and return it upon exit."
            },
            {
                "title": "Ginza Flagship Architecture & Chuo-Dori Walk",
                "venue_name": "Ginza Six & Chuo-Dori Avenue",
                "neighborhood": "Ginza, Chuo Ward",
                "location": "6-10-1 Ginza, Chuo City, Tokyo",
                "category": "Luxury Architecture & Design",
                "search_query": "Ginza Six, Ginza, Tokyo",
                "duration": "2 hours",
                "lat": 35.6696,
                "lng": 139.7640,
                "description": "Tokyo's premier luxury boulevard celebrated for striking contemporary flagship architecture by Shigeru Ban, Renzo Piano, and Yoshio Taniguchi, alongside historic department stores like Wako.",
                "tips": "Chuo-Dori becomes a pedestrian-only paradise (Hokousha Tengoku) on weekend afternoons."
            },
            {
                "title": "Odaiba Waterfront Promenade & Rainbow Bridge",
                "venue_name": "Odaiba Seaside Park & Fuji TV Building",
                "neighborhood": "Daiba, Minato Ward",
                "location": "1-4 Daiba, Minato City, Tokyo",
                "category": "Futuristic Bay & Waterfront Vistas",
                "search_query": "Odaiba Seaside Park, Minato, Tokyo",
                "duration": "2.5 hours",
                "lat": 35.6298,
                "lng": 139.7753,
                "description": "Man-made island in Tokyo Bay offering coastal sandy beach promenades, the miniature Statue of Liberty replica, Kenzo Tange's Fuji TV building, and dazzling views of the Rainbow Bridge.",
                "tips": "Ride the driverless Yurikamome monorail across the Rainbow Bridge for dramatic elevated vistas."
            },
            {
                "title": "teamLab Planets Immersive Digital Art Museum",
                "venue_name": "teamLab Planets TOKYO DMM",
                "neighborhood": "Toyosu, Koto Ward",
                "location": "6-1-16 Toyosu, Koto City, Tokyo",
                "category": "Interactive Digital Art",
                "search_query": "teamLab Planets, Toyosu, Tokyo",
                "duration": "2.5 hours",
                "lat": 35.6491,
                "lng": 139.7898,
                "description": "A museum where you walk through water and a garden where you become one with the flowers, featuring massive full-body immersive light installations.",
                "tips": "Visitors walk barefoot through knee-deep water; pants that can be rolled above the knees are recommended."
            },
            {
                "title": "Kanda Myojin Historic Shrine & Edo Heritage",
                "venue_name": "Kanda Myojin Shrine (神田明神)",
                "neighborhood": "Sotokanda, Chiyoda Ward",
                "location": "2-16-2 Sotokanda, Chiyoda City, Tokyo",
                "category": "Ancient Shrine & Tech Blessings",
                "search_query": "Kanda Myojin Shrine, Chiyoda, Tokyo",
                "duration": "1.5 hours",
                "lat": 35.7020,
                "lng": 139.7679,
                "description": "Enshrining three major Kami including Daikokuten and Ebisu, this 1,300-year-old sanctuary is celebrated for blessing both traditional Edo commerce and modern digital electronics.",
                "tips": "Pick up a unique digital IT security amulet (IT omamori) shaped like a computer memory card."
            }
        ],
        "dining": [
            {
                "name": "Soranoiro NIPPON",
                "cuisine": "Artisan Ramen (Michelin Bib Gourmand Featured)",
                "meal_type": "Lunch / Casual Dinner",
                "neighborhood": "Tokyo Station Ramen Street, Chiyoda Ward",
                "price_range": "¥1,100 - ¥1,800",
                "must_try_dish": "Special Vegan Vegie Soba with paprika-infused noodles, roasted root vegetables, and velvety cabbage-carrot broth",
                "dietary_friendly": ["Vegan", "Vegetarian", "Gluten-Free Options"],
                "lat": 35.6812,
                "lng": 139.7671
            },
            {
                "name": "Tsunahachi Shinjuku Sohonten",
                "cuisine": "Historic Edo-Style Tempura (Est. 1924)",
                "meal_type": "Lunch / Dinner",
                "neighborhood": "Shinjuku, Shinjuku Ward",
                "price_range": "¥3,500 - ¥7,000",
                "must_try_dish": "Counter-served crisp seasonal vegetable tempura (lotus root, shiitake, sweet potato) fried in pure sesame oil",
                "dietary_friendly": ["Vegetarian Options"],
                "lat": 35.6908,
                "lng": 139.7028
            },
            {
                "name": "Afuri Harajuku",
                "cuisine": "Contemporary Light Citrus Ramen",
                "meal_type": "Lunch / Dinner",
                "neighborhood": "Sendagaya, Shibuya Ward",
                "price_range": "¥1,200 - ¥1,900",
                "must_try_dish": "Yuzu Ratan Ramen or 100% Plant-Based Rainbow Vegan Yuzu Ramen topped with seasonal greens",
                "dietary_friendly": ["Vegan", "Vegetarian"],
                "lat": 35.6710,
                "lng": 139.7042
            },
            {
                "name": "Gyukatsu Motomura",
                "cuisine": "Specialty Crispy Beef Cutlet",
                "meal_type": "Lunch / Dinner",
                "neighborhood": "Shibuya / Shinjuku",
                "price_range": "¥2,200 - ¥3,500",
                "must_try_dish": "Lightly panko-crusted beef cutlet served rare with personal stone grill, grated yam, and wasabi dipping sauces",
                "dietary_friendly": ["Non-Vegetarian", "Meat"],
                "lat": 35.6580,
                "lng": 139.7025
            },
            {
                "name": "Torikizoku Shinjuku",
                "cuisine": "Traditional Yakitori Izakaya",
                "meal_type": "Evening / Late Night Izakaya",
                "neighborhood": "Kabukicho, Shinjuku Ward",
                "price_range": "¥1,800 - ¥3,200",
                "must_try_dish": "Charcoal-grilled tare chicken thigh skewers (Yakitori) and cabbage bowls",
                "dietary_friendly": ["Non-Vegetarian", "Poultry"],
                "lat": 35.6945,
                "lng": 139.7018
            }
        ],
        "hotels": {
            "budget": [
                {
                    "name": "UNPLAN Kagurazaka",
                    "type": "Design Boutique Hostel & Cafe",
                    "neighborhood": "Kagurazaka, Shinjuku Ward",
                    "rating": "4.8 / 5",
                    "why_recommended": "Stylish hostel with private pods and bunks in Tokyo's charming French-influenced Kagurazaka district, offering a bright lobby cafe and social lounge.",
                    "lat": 35.7042,
                    "lng": 139.7369
                },
                {
                    "name": "Nui. Hostel & Bar Lounge",
                    "type": "Artisan Hostel & Riverfront Lounge",
                    "neighborhood": "Kuramae, Taito Ward",
                    "rating": "4.8 / 5",
                    "why_recommended": "Converted historic warehouse in craft-focused Kuramae featuring handcrafted timber interiors, a vibrant downstairs barista cafe, and walkability to Asakusa.",
                    "lat": 35.7048,
                    "lng": 139.7925
                },
                {
                    "name": "APA Hotel & Resort Ryogoku Eki Tower",
                    "type": "Modern Value Business Hotel",
                    "neighborhood": "Ryogoku, Sumida Ward",
                    "rating": "4.6 / 5",
                    "why_recommended": "Efficient, modern high-rise rooms directly connected to Ryogoku JR Station featuring large communal bath facilities and sumo district heritage.",
                    "lat": 35.6961,
                    "lng": 139.7933
                },
                {
                    "name": "Sotetsu Fresa Inn Tokyo Kyobashi",
                    "type": "Modern Central Business Hotel",
                    "neighborhood": "Kyobashi, Chuo Ward",
                    "rating": "4.7 / 5",
                    "why_recommended": "Spotlessly clean modern rooms just an 8-minute walk from Tokyo Station and Ginza shopping avenue.",
                    "lat": 35.6775,
                    "lng": 139.7712
                }
            ],
            "moderate": [
                {
                    "name": "Hotel Gracery Shinjuku",
                    "type": "Iconic Contemporary Hotel",
                    "neighborhood": "Kabukicho, Shinjuku Ward",
                    "rating": "4.7 / 5",
                    "why_recommended": "Famous for the life-size Godzilla head overlooking the terrace, situated right in the center of Shinjuku's dining and entertainment district.",
                    "lat": 35.6953,
                    "lng": 139.7022
                },
                {
                    "name": "The Gate Hotel Asakusa Kaminarimon by Hulic",
                    "type": "Boutique Heritage Hotel",
                    "neighborhood": "Asakusa, Taito Ward",
                    "rating": "4.8 / 5",
                    "why_recommended": "Sophisticated boutique retreat directly opposite Kaminarimon Gate featuring a 13th-floor open terrace with spectacular views of Tokyo Skytree and Senso-ji.",
                    "lat": 35.7118,
                    "lng": 139.7963
                }
            ],
            "luxury": [
                {
                    "name": "Aman Tokyo",
                    "type": "5-Star Ultra-Luxury Urban Sanctuary",
                    "neighborhood": "Otemachi, Chiyoda Ward",
                    "rating": "4.9 / 5",
                    "why_recommended": "Occupying the top six floors of Otemachi Tower, blending traditional Japanese washi paper architecture, basalt stone onsen baths, and panoramic imperial garden views.",
                    "lat": 35.6868,
                    "lng": 139.7645
                },
                {
                    "name": "Hoshinoya Tokyo",
                    "type": "5-Star Luxury Ryokan Tower",
                    "neighborhood": "Otemachi, Chiyoda Ward",
                    "rating": "4.9 / 5",
                    "why_recommended": "A 17-story modern ryokan where guests remove their shoes at the cedar entrance to walk on tatami matting, complete with rooftop natural hot spring onsen.",
                    "lat": 35.6881,
                    "lng": 139.7658
                }
            ]
        }
    },
    "paris": {
        "city": "Paris",
        "country": "France",
        "center_coords": (48.8566, 2.3522),
        "best_time": "April to June (Spring) and September to October (Autumn) provide mild temperatures, blooming Parisian gardens, and open-air sidewalk terraces.",
        "overview": "Renowned globally as the City of Light, Paris is an incomparable showcase of classical architectural elegance, grand Haussmannian boulevards, and peerless artistic treasure. From the iron lace of the Eiffel Tower and the monumental galleries of the Louvre to the bohemian cobblestones of Montmartre and the vibrant café culture of Saint-Germain and Le Marais, the French capital offers unmatched romance, history, and gastronomic craft.",
        "districts": ["7th Arrondissement (Eiffel Tower)", "1st/4th Arrondissement (Louvre & Île de la Cité)", "18th Arrondissement (Montmartre)", "6th Arrondissement (Saint-Germain-des-Prés)", "3rd/4th Arrondissement (Le Marais)", "8th Arrondissement (Champs-Élysées)", "5th Arrondissement (Latin Quarter)"],
        "landmarks": [
            {
                "title": "Eiffel Tower & Champ de Mars Gardens",
                "venue_name": "Eiffel Tower (Tour Eiffel)",
                "neighborhood": "7th Arrondissement (Champ de Mars)",
                "location": "Champ de Mars, 5 Av. Anatole France, 75007 Paris, France",
                "category": "Iconic Monument & Skyline",
                "search_query": "Eiffel Tower, Paris",
                "duration": "2.5 hours",
                "lat": 48.8584,
                "lng": 2.2945,
                "description": "Gustave Eiffel's 1889 wrought-iron masterpiece soaring 330 meters above the Seine riverbank, offering panoramic multi-tier observation platforms overlooking all of Paris.",
                "tips": "Book summit elevator tickets at least 6 weeks in advance to avoid 2-hour queue lines, and watch the spectacular golden illumination sparkle on the hour after sunset."
            },
            {
                "title": "Musée du Louvre & Tuileries Garden",
                "venue_name": "Musée du Louvre",
                "neighborhood": "1st Arrondissement",
                "location": "Rue de Rivoli, 75001 Paris, France",
                "category": "Art & Royal Palace",
                "search_query": "Louvre Museum, Paris",
                "duration": "3.5 hours",
                "lat": 48.8606,
                "lng": 2.3376,
                "description": "The world's largest art museum housed inside the former French royal palace, holding over 35,000 masterpieces including Leonardo da Vinci's Mona Lisa, the Venus de Milo, and the Winged Victory of Samothrace.",
                "tips": "Enter through the Carrousel du Louvre underground entrance to bypass long outdoor pyramid queues."
            },
            {
                "title": "Arc de Triomphe & Champs-Élysées Promenade",
                "venue_name": "Arc de Triomphe",
                "neighborhood": "8th Arrondissement (Place Charles de Gaulle)",
                "location": "Pl. Charles de Gaulle, 75008 Paris, France",
                "category": "Historic Monument & Vista",
                "search_query": "Arc de Triomphe, Paris",
                "duration": "1.5 hours",
                "lat": 48.8738,
                "lng": 2.2950,
                "description": "Commissioned by Napoleon in 1806 to honor the Grande Armée, featuring the Tomb of the Unknown Soldier and a rooftop terrace with 12 radiating grand avenues.",
                "tips": "Access the monument strictly via the pedestrian underpass at the top of the Champs-Élysées; never attempt to cross the chaotic roundabout."
            },
            {
                "title": "Montmartre & Sacré-Cœur Basilica",
                "venue_name": "Basilique du Sacré-Cœur de Montmartre",
                "neighborhood": "18th Arrondissement (Montmartre)",
                "location": "35 Rue du Chevalier de la Barre, 75018 Paris, France",
                "category": "Spiritual & Bohemian Arts",
                "search_query": "Sacré-Cœur, Montmartre, Paris",
                "duration": "3 hours",
                "lat": 48.8867,
                "lng": 2.3431,
                "description": "Perched atop Paris's highest hilltop, the Romano-Byzantine white travertine basilica overlooks picturesque cobbled streets, vineyard terraces, and the bustling portrait painters of Place du Tertre.",
                "tips": "Take the Montmartre Funicular using a standard metro ticket if you prefer to avoid the 222-step outdoor staircase climb."
            },
            {
                "title": "Musée d'Orsay & Left Bank Promenade",
                "venue_name": "Musée d'Orsay",
                "neighborhood": "7th Arrondissement (Left Bank)",
                "location": "1 Rue de la Légion d'Honneur, 75007 Paris, France",
                "category": "Impressionist Art & Architecture",
                "search_query": "Musée d'Orsay, Paris",
                "duration": "2.5 hours",
                "lat": 48.8599,
                "lng": 2.3266,
                "description": "Housed within a majestic 1900 Beaux-Arts railway terminal, featuring the world's premier collection of Impressionist and Post-Impressionist masterpieces by Monet, Van Gogh, Degas, Renoir, and Cézanne.",
                "tips": "Head to the 5th-floor gallery to photograph the Seine through the monumental iron station clock face."
            },
            {
                "title": "Sainte-Chapelle & Île de la Cité Historic Heart",
                "venue_name": "Sainte-Chapelle & Notre-Dame Parvis",
                "neighborhood": "Île de la Cité, 4th Arrondissement",
                "location": "10 Bd du Palais, 75001 Paris, France",
                "category": "Gothic Architecture & Heritage",
                "search_query": "Sainte-Chapelle, Paris",
                "duration": "2 hours",
                "lat": 48.8530,
                "lng": 2.3499,
                "description": "A 13th-century Rayonnant Gothic royal jewel box containing 15 soaring stained-glass lancet windows depicting over 1,100 biblical scenes in mesmerizing jewel-toned light, located beside the iconic restored Notre-Dame Cathedral.",
                "tips": "Visit midday when direct sunlight illuminates the upper chapel's radiant red, blue, and gold stained glass."
            },
            {
                "title": "Le Marais Historic Mansions & Place des Vosges",
                "venue_name": "Place des Vosges & Le Marais Historic Quarter",
                "neighborhood": "4th Arrondissement (Le Marais)",
                "location": "Pl. des Vosges, 75004 Paris, France",
                "category": "Historic Quarters & Boutiques",
                "search_query": "Place des Vosges, Le Marais, Paris",
                "duration": "2.5 hours",
                "lat": 48.8554,
                "lng": 2.3653,
                "description": "Paris's oldest planned royal square built in 1612 with uniform red-brick and stone arcades, surrounded by aristocratic hôtels particuliers, independent designer fashion boutiques, and contemporary art galleries.",
                "tips": "Visit Victor Hugo's preserved former residence in the corner arcade of Place des Vosges."
            },
            {
                "title": "Le Panthéon & Latin Quarter Academia Walk",
                "venue_name": "Le Panthéon",
                "neighborhood": "5th Arrondissement (Latin Quarter)",
                "location": "Pl. du Panthéon, 75005 Paris, France",
                "category": "Neoclassical Monument & Crypt",
                "search_query": "Panthéon, Paris",
                "duration": "2 hours",
                "lat": 48.8462,
                "lng": 2.3464,
                "description": "Explore the magnificent neoclassical dome, Foucault's pendulum, and solemn crypt of the Panthéon, the final resting place of Voltaire, Jean-Jacques Rousseau, Victor Hugo, and Marie Curie.",
                "tips": "Climb the colonnade dome during spring and summer for striking 360-degree vistas across the Latin Quarter."
            },
            {
                "title": "Palais Garnier National Opera House",
                "venue_name": "Opéra Garnier (Palais Garnier)",
                "neighborhood": "9th Arrondissement (Opéra)",
                "location": "Pl. de l'Opéra, 75009 Paris, France",
                "category": "Opera, Ballet & Grand Architecture",
                "search_query": "Palais Garnier, Paris",
                "duration": "2 hours",
                "lat": 48.8719,
                "lng": 2.3316,
                "description": "Charles Garnier's 1875 Beaux-Arts architectural marvel with the famous grand marble staircase, gilded mirrors in the Grand Foyer, and Marc Chagall's colorful painted auditorium ceiling.",
                "tips": "Self-guided tour tickets give full access to the royal boxes and grand foyer; visit on weekday mornings."
            },
            {
                "title": "Centre Pompidou Modern Art & Beaubourg Piazza",
                "venue_name": "Centre Pompidou (Musée National d'Art Moderne)",
                "neighborhood": "4th Arrondissement (Beaubourg)",
                "location": "Place Georges-Pompidou, 75004 Paris, France",
                "category": "Modern & Contemporary Art",
                "search_query": "Centre Pompidou, Paris",
                "duration": "2.5 hours",
                "lat": 48.8606,
                "lng": 2.3522,
                "description": "Renzo Piano and Richard Rogers' revolutionary high-tech inside-out architecture featuring Europe's largest modern art museum, with masterpieces by Picasso, Matisse, and Kandinsky.",
                "tips": "Ride the outdoor glass caterpillar escalators to the 6th-floor rooftop terrace for magnificent sweeping views of Paris."
            },
            {
                "title": "Catacombes de Paris Historical Underground Ossuary",
                "venue_name": "Les Catacombes de Paris",
                "neighborhood": "14th Arrondissement (Denfert-Rochereau)",
                "location": "1 Av. du Colonel Henri Rol-Tanguy, 75014 Paris, France",
                "category": "Historical Subterranean Heritage",
                "search_query": "Catacombes de Paris, Paris",
                "duration": "1.5 hours",
                "lat": 48.8338,
                "lng": 2.3324,
                "description": "Walk 20 meters beneath the city through ancient limestone quarries housing the resting place of over six million Parisians arranged in solemn decorative bone galleries.",
                "tips": "Temperature remains a constant 14°C (57°F) underground; bring a light sweater and wear shoes with good traction."
            },
            {
                "title": "Grand Palais & Pont Alexandre III Gilded Bridge",
                "venue_name": "Pont Alexandre III & Grand Palais",
                "neighborhood": "8th Arrondissement (Champs-Élysées / Seine)",
                "location": "Pont Alexandre III, 75008 Paris, France",
                "category": "Historic Bridge & Beaux-Arts Monuments",
                "search_query": "Pont Alexandre III, Paris",
                "duration": "1.5 hours",
                "lat": 48.8639,
                "lng": 2.3135,
                "description": "Paris's most opulent bridge built for the 1900 Exposition Universelle, adorned with gilded bronze statues of winged horses, cherubs, and Art Nouveau lampposts framing the Grand Palais.",
                "tips": "Stand on the southern bridge parapet at dusk for one of the most celebrated photography angles of the illuminated Eiffel Tower."
            },
            {
                "title": "Canal Saint-Martin Bohemian Footbridges & Cafes",
                "venue_name": "Canal Saint-Martin Promenade",
                "neighborhood": "10th Arrondissement (Canal Saint-Martin)",
                "location": "Quai de Valmy, 75010 Paris, France",
                "category": "Bohemian Waterways & Local Life",
                "search_query": "Canal Saint-Martin, Paris",
                "duration": "2 hours",
                "lat": 48.8715,
                "lng": 2.3653,
                "description": "A picturesque 19th-century canal flanked by arched green iron footbridges, vintage water locks, chestnut trees, and independent coffee roasteries.",
                "tips": "Pick up a fresh baguette, cheese, and pastries to join young Parisians picnicking on the canal banks."
            },
            {
                "title": "Musée de l'Orangerie Monet Water Lilies",
                "venue_name": "Musée de l'Orangerie",
                "neighborhood": "1st Arrondissement (Jardin des Tuileries)",
                "location": "Jardin des Tuileries, 75001 Paris, France",
                "category": "Impressionist Masterpieces",
                "search_query": "Musée de l'Orangerie, Paris",
                "duration": "1.5 hours",
                "lat": 48.8638,
                "lng": 2.3227,
                "description": "Two custom oval galleries designed by Claude Monet himself to showcase his monumental 360-degree Water Lilies (Nymphéas) mural cycle under diffuse natural sky light.",
                "tips": "Sit in the center of the oval room in silence to experience the immersive optical tranquility Monet envisioned."
            },
            {
                "title": "Seine River Sunset Cruise & Pont Neuf Discovery",
                "venue_name": "Vedettes du Pont Neuf / Bateaux Parisiens",
                "neighborhood": "1st Arrondissement (Île de la Cité Pier)",
                "location": "Square du Vert-Galant, 75001 Paris, France",
                "category": "Scenic River Cruise & Monuments",
                "search_query": "Vedettes du Pont Neuf, Paris",
                "duration": "1.5 hours",
                "lat": 48.8570,
                "lng": 2.3400,
                "description": "Glide along the UNESCO-listed Seine river banks at golden hour, passing beneath Paris's oldest bridge (Pont Neuf, 1607) and marveling at illuminated waterfront palaces.",
                "tips": "Board 30 minutes before twilight for optimal photography of both golden hour and the sparkling night illumination."
            }
        ],
        "dining": [
            {
                "name": "Bouillon Chartier",
                "cuisine": "Traditional Belle Époque Parisian Brasserie",
                "meal_type": "Lunch / Dinner",
                "neighborhood": "9th Arrondissement (Grands Boulevards)",
                "price_range": "€15 - €30",
                "must_try_dish": "Classic escargots de Bourgogne with garlic parsley butter, roasted confit de canard with baby potatoes, and artisanal profiteroles",
                "dietary_friendly": ["Non-Vegetarian", "Meat", "Poultry"],
                "lat": 48.8718,
                "lng": 2.3431
            },
            {
                "name": "Café de Flore",
                "cuisine": "Historic Saint-Germain Literary Bistro & Cafe",
                "meal_type": "Breakfast / Afternoon Tea",
                "neighborhood": "6th Arrondissement (Saint-Germain-des-Prés)",
                "price_range": "€20 - €45",
                "must_try_dish": "Traditional toasted Croque Monsieur on pain Poilâne, rich hot chocolate (chocolat chaud spécial Flore), and freshly baked croissants",
                "dietary_friendly": ["Vegetarian Options"],
                "lat": 48.8542,
                "lng": 2.3326
            },
            {
                "name": "L'As du Fallafel",
                "cuisine": "Celebrated Middle Eastern & Street Food (Kosher)",
                "meal_type": "Casual Lunch / Street Food",
                "neighborhood": "4th Arrondissement (Rue des Rosiers, Le Marais)",
                "price_range": "€10 - €18",
                "must_try_dish": "Special Fallafel Pita loaded with golden fried chickpea patties, roasted spiced eggplant, pickled red cabbage, cucumber salad, and rich tahini",
                "dietary_friendly": ["Vegetarian", "Vegan", "Kosher"],
                "lat": 48.8575,
                "lng": 2.3592
            },
            {
                "name": "Breizh Café Le Marais",
                "cuisine": "Artisan Organic Brittany Crêperie & Cider Bar",
                "meal_type": "Lunch / Dinner",
                "neighborhood": "3rd Arrondissement (Le Marais)",
                "price_range": "€18 - €35",
                "must_try_dish": "Crispy organic buckwheat galette with artisanal Bordier butter, Gruyère cheese, egg, and organic Brittany dry cider",
                "dietary_friendly": ["Vegetarian Options", "Gluten-Free Options"],
                "lat": 48.8598,
                "lng": 2.3625
            },
            {
                "name": "Le Potager de Charlotte",
                "cuisine": "Gourmet Plant-Based Haute Gastronomy",
                "meal_type": "Dinner",
                "neighborhood": "9th Arrondissement (Rue Condorcet)",
                "price_range": "€35 - €60",
                "must_try_dish": "Hard-boiled style avocado mimosa with silken tofu, roasted cauliflower steak with hazelnut cream, and dark chocolate ganache",
                "dietary_friendly": ["Vegan", "Vegetarian", "Gluten-Free Options"],
                "lat": 48.8804,
                "lng": 2.3468
            }
        ],
        "hotels": {
            "budget": [
                {
                    "name": "Generator Paris",
                    "type": "Design Boutique Hostel & Rooftop Bar",
                    "neighborhood": "10th Arrondissement (Canal Saint-Martin)",
                    "rating": "4.7 / 5",
                    "why_recommended": "Contemporary design hostel featuring private rooms and shared pods, complete with a rooftop bar overlooking Sacré-Cœur, moments from vibrant Canal Saint-Martin.",
                    "lat": 48.8783,
                    "lng": 2.3695
                },
                {
                    "name": "The People Paris Marais",
                    "type": "Eco-Design Boutique Hostel & Suites",
                    "neighborhood": "4th Arrondissement (Le Marais)",
                    "rating": "4.8 / 5",
                    "why_recommended": "Modern lifestyle boutique stay featuring private rooms and pods, rooftop terrace, and exceptional walkability to the Seine and Île Saint-Louis.",
                    "lat": 48.8505,
                    "lng": 2.3642
                }
            ],
            "moderate": [
                {
                    "name": "Hotel Le Relais Saint-Germain",
                    "type": "Authentic Left Bank Heritage Hotel",
                    "neighborhood": "6th Arrondissement (Saint-Germain-des-Prés)",
                    "rating": "4.9 / 5",
                    "why_recommended": "Charming 17th-century boutique hotel in the heart of Saint-Germain, celebrated for its literary salon heritage and quintessential Parisian hospitality.",
                    "lat": 48.8523,
                    "lng": 2.3385
                },
                {
                    "name": "Hotel Caron de Beaumarchais",
                    "type": "18th-Century Historical Boutique Hotel",
                    "neighborhood": "4th Arrondissement (Le Marais)",
                    "rating": "4.8 / 5",
                    "why_recommended": "Inspired by the Marriage of Figaro, featuring period antiques, exposed ceiling beams, and intimate Parisian charm in central Le Marais.",
                    "lat": 48.8575,
                    "lng": 2.3571
                }
            ],
            "luxury": [
                {
                    "name": "Le Meurice - Dorchester Collection",
                    "type": "5-Star Historic Palace Hotel",
                    "neighborhood": "1st Arrondissement (Rue de Rivoli)",
                    "rating": "4.9 / 5",
                    "why_recommended": "A Parisian palace hotel since 1835 blending 18th-century Versailles grandeur with Philippe Starck interiors, directly overlooking the Tuileries Garden.",
                    "lat": 48.8651,
                    "lng": 2.3298
                },
                {
                    "name": "Hôtel de Crillon, A Rosewood Hotel",
                    "type": "5-Star Neoclassical Palace Hotel",
                    "neighborhood": "8th Arrondissement (Place de la Concorde)",
                    "rating": "4.9 / 5",
                    "why_recommended": "Commissioned by King Louis XV in 1758, offering peerless five-star luxury, Marie Antoinette suites, and direct views of the Place de la Concorde obelisk.",
                    "lat": 48.8675,
                    "lng": 2.3216
                }
            ]
        }
    }
}

def resolve_electrical_standards(destination: str) -> Dict[str, str]:
    """Resolves official plug type and voltage for destination without any hardcoded country bias."""
    dest_lower = destination.lower()
    for country, specs in ELECTRICAL_STANDARDS.items():
        if country in dest_lower:
            return specs
    # Default international European standard if country unknown
    return {
        "plugs": "Type C & F (Europlug & Schuko) or standard international adapter",
        "voltage": "220-240 V",
        "frequency": "50 Hz",
        "description": "Standard international travel plug adapter recommended."
    }

def resolve_transit_and_currency(destination: str) -> Dict[str, str]:
    """Resolves local currency and authentic transit card for the destination."""
    dest_lower = destination.lower()
    for key, info in LOCAL_TRANSIT_AND_CURRENCY.items():
        if key in dest_lower:
            return info
    # Sensible default
    return {
        "country": destination.split(",")[-1].strip() if "," in destination else destination,
        "currency_name": "Local Currency",
        "currency_code": "USD",
        "currency_symbol": "$",
        "transit_card": "Local Public Transit Card / Contactless Pay",
        "transit_details": "Use local contactless debit/credit cards or purchase reloadable transit cards at central metro/rail stations."
    }

def resolve_bilateral_visa(origin: str, destination: str) -> str:
    """
    Evaluates real bilateral visa and immigration requirements between origin and destination.
    Accurately handles Indian passports entering Turkey, Japan, Schengen, UK, UAE, etc.
    """
    orig_lower = (origin or "").lower()
    dest_lower = (destination or "").lower()

    is_indian_origin = any(w in orig_lower for w in ["india", "bangalore", "bengaluru", "delhi", "mumbai", "chennai", "hyderabad", "kolkata", "pune", "kochi"])
    is_us_origin = any(w in orig_lower for w in ["usa", "united states", "new york", "california", "texas", "chicago", "los angeles"])
    is_uk_origin = any(w in orig_lower for w in ["uk", "united kingdom", "london", "manchester", "birmingham"])
    is_eu_origin = any(w in orig_lower for w in ["france", "germany", "italy", "spain", "netherlands", "paris", "berlin", "rome"])

    # 1. Destination: Turkey
    if "turkey" in dest_lower or "istanbul" in dest_lower or "ankara" in dest_lower or "antalya" in dest_lower:
        if is_indian_origin:
            return (
                "Bilateral Visa Notice for Indian Passport Holders entering Turkey: "
                "Ordinary Indian passport holders require an entry visa prior to departure. "
                "CRITICAL CONDITIONAL E-VISA RULE: Indian citizens holding a valid visa or residence permit from Schengen member states, USA, UK, or Ireland "
                "are eligible to apply for a 30-day single-entry Turkish e-Visa online via the official Republic of Türkiye e-Visa portal (evisa.gov.tr). "
                "Indian passport holders WITHOUT a valid Schengen/US/UK/Ireland visa MUST apply in advance for a physical sticker tourist visa through Gateway Globe / VFS Global centers in India before travel. "
                "Visa-on-Arrival (VoA) is strictly NOT available at Turkish airports. Passport must be valid for at least 6 months beyond the arrival date with at least two blank pages."
            )
        elif is_us_origin or is_uk_origin or is_eu_origin:
            return (
                "US, UK, and European passport holders can enter Turkey visa-free for touristic visits of up to 90 days within any 180-day period. "
                "Ensure your passport is valid for at least 150 days from the date of entry into Turkey."
            )
        else:
            return (
                f"Visitors from {origin} must check the official Republic of Türkiye Ministry of Foreign Affairs portal (evisa.gov.tr). "
                "Eligible nationalities can secure a digital e-Visa online prior to boarding; others require an advance sticker visa through Turkish consular missions."
            )

    # 2. Destination: Japan
    if "japan" in dest_lower or "tokyo" in dest_lower or "kyoto" in dest_lower or "osaka" in dest_lower:
        if is_indian_origin:
            return (
                "Bilateral Visa Notice for Indian Passport Holders entering Japan: "
                "Indian citizens departing from India require a pre-approved Japan Tourist eVisa (single-entry for tourism applied via the official Japan eVisa website) "
                "or a standard sticker visa processed through VFS Global before departure. "
                "Visa-on-Arrival (VoA) is STRICTLY NOT AVAILABLE for Indian passport holders. "
                "Ensure your passport has at least 6 months validity from the date of return and bring printed accommodation vouchers and return flight tickets for immigration."
            )
        elif is_us_origin or is_uk_origin or is_eu_origin:
            return (
                "US, UK, and EU passport holders are granted visa-free entry to Japan for tourism for up to 90 days. "
                "Complete the digital Visit Japan Web customs and immigration declaration QR code prior to departure."
            )

    # 3. Destination: Schengen / European Union (France, Italy, Spain, etc.)
    if any(c in dest_lower for c in ["france", "paris", "italy", "rome", "spain", "barcelona", "germany", "netherlands", "amsterdam", "greece", "santorini"]):
        if is_indian_origin:
            return (
                "Bilateral Visa Notice for Indian Passport Holders entering Schengen Area: "
                "Indian citizens require a pre-approved Schengen Short-Stay Visa (Type C) applied through the consular mission / VFS center of your main destination country. "
                "Visa-on-Arrival is NOT available. Processing typically takes 15-20 calendar days; applications require confirmed flights, hotel vouchers, 3-month bank statements, and travel insurance covering at least €30,000."
            )
        elif is_us_origin or is_uk_origin:
            return (
                "US and UK citizens can travel to the Schengen Area for tourism up to 90 days in any 180-day period without a visa. "
                "Ensure passport has at least 3 months validity beyond intended departure from Schengen."
            )

    # 4. Destination: United Kingdom
    if "united kingdom" in dest_lower or "london" in dest_lower or "uk" in dest_lower or "scotland" in dest_lower:
        if is_indian_origin:
            return (
                "Indian passport holders require a pre-approved UK Standard Visitor Visa applied online via UK Visas and Immigration (UKVI) and biometric appointment at VFS Global. "
                "Visa-on-Arrival is strictly not available. Processing takes approximately 3 weeks."
            )
        elif is_us_origin or is_eu_origin:
            return (
                "US and EU citizens do not need a visa to visit the UK for tourism stays of up to 6 months. "
                "Electronic Travel Authorisation (ETA) may apply depending on arrival date."
            )

    # 5. Destination: UAE / Dubai
    if "uae" in dest_lower or "dubai" in dest_lower or "abu dhabi" in dest_lower:
        if is_indian_origin:
            return (
                "Indian passport holders can obtain an advance tourist visa (30 or 60 days) arranged through airlines or travel agencies. "
                "Indian citizens with a valid US visa/Green Card or UK/EU residence permit (valid for at least 6 months) are eligible for a 14-day Visa on Arrival at UAE airports."
            )

    # 6. Destination: Indonesia / Bali
    if "indonesia" in dest_lower or "bali" in dest_lower:
        if is_indian_origin:
            return (
                "Indian passport holders are eligible for an Indonesian Visa on Arrival (VoA) or electronic Visa on Arrival (e-VoA) for a 30-day tourism stay, "
                "payable upon arrival (approx. IDR 500,000 / ~₹2,700) or online prior to departure via molina.imigrasi.go.id. Passport must have 6 months validity."
            )

    # Generic Fallback
    return (
        f"Travelers departing from {origin} to {destination} should verify entry requirements with the destination's immigration authority. "
        "Ensure your passport holds at least 6 months validity from departure date and verify whether an advance visa, electronic travel authorization (eTA/eVisa), or visa-free entry applies."
    )

def resolve_diplomatic_mission(origin: str, destination: str) -> str:
    """
    Distinguishes whether destination is a national capital (Embassy/High Commission)
    or a commercial/cultural hub (Consulate General), ensuring accurate diplomatic info.
    """
    dest_lower = (destination or "").lower()
    orig_lower = (origin or "").lower()
    is_india = any(w in orig_lower for w in ["india", "bangalore", "delhi", "mumbai", "chennai", "hyderabad", "kolkata", "bengaluru"])

    if is_india:
        # Turkey: Istanbul (Commercial Hub) vs Ankara (Capital)
        if "istanbul" in dest_lower:
            return (
                "Consulate General of India, Istanbul (Commercial Hub):\n"
                "Address: Cumhuriyet Caddesi, No: 42, Dörtler Apt, 5th Floor, Harbiye, Şişli, 34367 Istanbul, Turkey.\n"
                "Tel: +90 212 296 2131 / +90 212 296 2132 | 24/7 Consular Emergency: +90 530 069 5488\n"
                "Email: cgi.istanbul@mea.gov.in | Website: cgiistanbul.gov.in\n"
                "(Note: The Embassy of India to Turkey is located in the capital, Ankara: Cinnah Caddesi No. 77, Çankaya, Ankara)."
            )
        elif "ankara" in dest_lower:
            return (
                "Embassy of India, Ankara (Capital Mission):\n"
                "Address: Cinnah Caddesi No. 77, Çankaya, 06680 Ankara, Turkey.\n"
                "Tel: +90 312 438 2195 | Consular Helpline: +90 312 440 8259\n"
                "Email: hoc.ankara@mea.gov.in | Website: indembassyankara.gov.in"
            )
        # Japan: Tokyo (Capital)
        elif "tokyo" in dest_lower or "japan" in dest_lower:
            return (
                "Embassy of India, Tokyo (Capital Mission):\n"
                "Address: 2-2-11 Kudan-Minami, Chiyoda-ku, Tokyo 102-0074, Japan.\n"
                "General Tel: +81-3-3262-2101 | 24/7 Consular Emergency: +81-80-3214-4701\n"
                "Email: cons.tokyo@mea.gov.in | Website: indembassy-tokyo.gov.in"
            )
        # France: Paris (Capital)
        elif "paris" in dest_lower or "france" in dest_lower:
            return (
                "Embassy of India, Paris (Capital Mission):\n"
                "Address: 13-15 Rue Cimarosa, 75116 Paris, France.\n"
                "Tel: +33 1 40 50 70 70 | Consular Emergency: +33 1 40 50 71 71\n"
                "Email: cons.paris@mea.gov.in | Website: eoiparis.gov.in"
            )
        # UK: London (Capital)
        elif "london" in dest_lower or "uk" in dest_lower or "united kingdom" in dest_lower:
            return (
                "High Commission of India, London (Capital Mission):\n"
                "Address: India House, Aldwych, London WC2B 4NA, United Kingdom.\n"
                "Tel: +44 20 7836 9147 | Emergency Consular Helpline: +44 776 876 1363\n"
                "Email: info.london@hcilondon.in | Website: hcilondon.gov.in"
            )
        # USA: New York (Commercial Hub) vs Washington DC (Capital)
        elif "new york" in dest_lower or "nyc" in dest_lower:
            return (
                "Consulate General of India, New York (Commercial Hub):\n"
                "Address: 3 East 64th Street (between 5th and Madison Ave), New York, NY 10065, USA.\n"
                "Tel: +1-212-774-0600 | 24/7 Consular Emergency Helpline: +1-212-774-0662\n"
                "Email: visa.newyork@mea.gov.in | Website: indiacgny.org\n"
                "(Note: The Embassy of India to the United States is in the capital, Washington DC: 2107 Massachusetts Ave NW)."
            )
        # UAE: Dubai (Commercial Hub) vs Abu Dhabi (Capital)
        elif "dubai" in dest_lower:
            return (
                "Consulate General of India, Dubai (Commercial Hub):\n"
                "Address: Al Hamriya, Diplomatic Enclave, Bur Dubai, Dubai, UAE.\n"
                "Tel: +971 4 397 1222 | 24/7 Toll-Free PBSK Helpline: 800 46342\n"
                "Website: cgidubai.gov.in\n"
                "(Note: The Embassy of India to the UAE is in the capital, Abu Dhabi: Plot W-59, Diplomatic Area, Embassies District)."
            )
        # Italy: Rome (Capital)
        elif "rome" in dest_lower or "italy" in dest_lower:
            return (
                "Embassy of India, Rome (Capital Mission):\n"
                "Address: Via Venti Settembre, 5, 00187 Rome, Italy.\n"
                "Tel: +39 06 4884 642 | Consular Emergency: +39 345 613 2162\n"
                "Email: cons.rome@mea.gov.in | Website: indianembassyrome.gov.it"
            )

    # General Fallback
    dest_clean = destination.strip().title()
    return (
        f"Diplomatic Representation for travelers in {dest_clean}:\n"
        f"Consular assistance is coordinated through your home country's Embassy (in the capital city) or Consulate General (in regional commercial centers).\n"
        f"Always carry registered copies of your passport, entry visa, and travel insurance details."
    )

def get_authentic_destination(destination: str) -> Optional[Dict[str, Any]]:
    """Resolves authentic destination dataset if cataloged, else None."""
    dest_lower = (destination or "").lower()
    for key, data in AUTHENTIC_DESTINATIONS.items():
        if key in dest_lower:
            return data
    return None

