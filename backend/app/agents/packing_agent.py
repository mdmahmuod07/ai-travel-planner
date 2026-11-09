import asyncio
import logging
from typing import Dict, Any, List, Optional, Callable, Awaitable
from app.agents.base_agent import BaseAgent
from app.schemas.travel import TravelRequest, PackingCategory, TravelSafetyTips
from app.services.llm_factory import llm_provider
from app.services.destination_knowledge import (
    resolve_electrical_standards,
    resolve_transit_and_currency,
    resolve_bilateral_visa,
    resolve_diplomatic_mission
)

logger = logging.getLogger("packing_agent")

class PackingAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_id="packing_specialist",
            name="Packing & Travel Safety Specialist",
            role="Compiles customized weather-aware packing lists, visa advice, and local etiquette."
        )

    async def process(self, request: TravelRequest, context: Dict[str, Any], log_cb: Optional[Callable[[str, str], Awaitable[None]]] = None) -> Dict[str, Any]:
        dest_clean = request.destination.strip().title()
        dest_lower = request.destination.lower()
        origin_clean = (request.origin or "Your departure origin").strip().title()

        if log_cb:
            await log_cb(self.agent_id, f"Evaluating climate data, electrical standards, and bilateral visa regulations for {dest_clean} (Origin: {origin_clean})...")
            await asyncio.sleep(0.4)

        # Knowledge-grounded data resolution
        elec_info = resolve_electrical_standards(request.destination)
        transit_info = resolve_transit_and_currency(request.destination)
        visa_info = resolve_bilateral_visa(request.origin, request.destination)
        mission_info = resolve_diplomatic_mission(request.origin, request.destination)

        system_prompt = (
            "You are an expert travel safety adviser, consular consultant, and packing expert. "
            "Generate a structured packing checklist and authoritative safety/visa advice based strictly on the destination and origin provided. "
            "\n"
            "STRICT CONTEXT-DRIVEN RESOLUTION & PURGE ALL HARDCODED DEFAULTS:\n"
            "- Purge all hardcoded defaults or templates from other countries (do NOT bleed Japanese or Asian artifacts into European, Middle Eastern, or American destinations).\n"
            "- Look up the official electrical standards for the destination: exact plug types (e.g., Type C & F for Turkey/Europe, Type G for UK) and voltage.\n"
            "- Identify the official currency and contactless transit system for the destination (e.g., Istanbulkart for Istanbul, Oyster Card for London, Navigo for Paris).\n"
            "- Bilateral Visa & Entry Evaluation: Compare the origin nationality/passport against destination entry laws (e.g. for Indian passports entering Turkey: conditional Turkish eVisa only with valid Schengen/US/UK/Ireland visa, otherwise advance visa required).\n"
            "- Bilateral Diplomatic Mission: Identify whether the destination is a capital or commercial hub. Distinguish between an Embassy (in the capital) and a Consulate General (in commercial hubs like Istanbul, NYC, Frankfurt).\n"
            "- DO NOT invent or include generic emergency hotline numbers.\n"
            "\n"
            "Return JSON with keys: 'packing_checklist' (list of objects with category_name, items) "
            "and 'travel_tips' (object with weather_summary, visa_and_entry, local_customs, currency_and_payment_tips, electrical_specs, transit_tips, embassy_info)."
        )

        user_prompt = f"""
        Destination: {request.destination}
        Origin: {request.origin}
        Duration: {request.duration_days} days
        Travel Style: {request.travel_style}
        Electrical Standards: {elec_info['plugs']}, {elec_info['voltage']}
        Local Transit System: {transit_info['transit_card']}
        Bilateral Visa Law: {visa_info}
        Diplomatic Mission: {mission_info}
        """

        llm_result = await llm_provider.generate_json(system_prompt, user_prompt)

        if log_cb:
            await log_cb(self.agent_id, f"Packing checklist, electrical specifications, and consular protocols finalized for {dest_clean}.")
            await asyncio.sleep(0.3)

        if llm_result and "packing_checklist" in llm_result and "travel_tips" in llm_result:
            try:
                raw_pack = llm_result["packing_checklist"]
                packs: List[PackingCategory] = []

                if isinstance(raw_pack, dict):
                    label_map = {
                        "essential_documents": "Essential Documents & Travel Funds",
                        "clothing": "Clothing & Climate-Appropriate Apparel",
                        "electronics": "Electronics, Adapters & Power",
                        "health": "Health, Medications & Personal Care"
                    }
                    for k, v in raw_pack.items():
                        cname = label_map.get(k, k.replace("_", " ").title())
                        raw_items = v if isinstance(v, list) else [v]
                        cleaned_items = [
                            str(x.get("item") or x.get("name") or x) if isinstance(x, dict) else str(x)
                            for x in raw_items
                            if x
                        ]
                        if cleaned_items:
                            packs.append(PackingCategory(category_name=cname, items=cleaned_items))

                elif isinstance(raw_pack, list):
                    for p in raw_pack:
                        if isinstance(p, dict):
                            cname = p.get("category_name") or p.get("name") or p.get("category") or "Essentials"
                            raw_items = p.get("items") or p.get("checklist") or p.get("list") or []
                            cleaned_items = [
                                str(x.get("item") or x.get("name") or x) if isinstance(x, dict) else str(x)
                                for x in raw_items
                                if x
                            ]
                            if cleaned_items:
                                packs.append(PackingCategory(category_name=cname, items=cleaned_items))

                tips_data = llm_result["travel_tips"]
                # Guarantee ground-truth accuracy on critical bilateral data
                if not tips_data.get("visa_and_entry") or len(tips_data.get("visa_and_entry", "")) < 30:
                    tips_data["visa_and_entry"] = visa_info
                if not tips_data.get("embassy_info") or len(tips_data.get("embassy_info", "")) < 30:
                    tips_data["embassy_info"] = mission_info
                if not tips_data.get("electrical_specs"):
                    tips_data["electrical_specs"] = f"{elec_info['plugs']} ({elec_info['voltage']}, {elec_info['frequency']})"
                if not tips_data.get("transit_tips"):
                    tips_data["transit_tips"] = transit_info["transit_details"]
                tips = TravelSafetyTips(**tips_data)

                if packs:
                    return {"packing_checklist": packs, "travel_tips": tips}
            except Exception as e:
                logger.error(f"Error parsing LLM packing response: {e}")

        # Deterministic knowledge-grounded fallback resolution (zero template bleed)
        checklist = [
            PackingCategory(
                category_name="Essential Travel Documents & Money",
                items=[
                    "Original Passport (valid for at least 6 months beyond travel date) & 2 printed photocopies",
                    f"Official Visa Documentation / Approval confirmation for {dest_clean}",
                    "Printed return flight confirmations and confirmed accommodation vouchers for immigration inspection",
                    f"International debit/credit card (activated for international transactions) + modest amount of local currency ({transit_info['currency_code']})",
                    "Comprehensive international travel & medical insurance policy documentation"
                ]
            ),
            PackingCategory(
                category_name=f"Electrical & Power Adapters ({elec_info['plugs']})",
                items=[
                    f"Power Plug Adapter: Compatible with {elec_info['plugs']} ({elec_info['voltage']}, {elec_info['frequency']})",
                    "High-capacity portable power bank (10,000mAh+) for full-day smartphone navigation",
                    "Dual-voltage charging cables and USB-C multi-device charging brick",
                    f"Pre-ordered regional eSIM QR voucher or local SIM card for reliable data access across {dest_clean}"
                ]
            ),
            PackingCategory(
                category_name="Clothing & Destination Etiquette Apparel",
                items=[
                    "Comfortable, supportive walking shoes suitable for exploring historic cobblestones, marble plazas, and urban hills",
                    "Modest attire covering shoulders and knees (essential when visiting active mosques, cathedrals, and sacred heritage sites)",
                    "Lightweight scarf or shawl (for women when entering historic places of worship)",
                    "Breathable daytime layering pieces plus a versatile evening jacket for temperature shifts",
                    "Compact travel umbrella or lightweight rain shell"
                ]
            ),
            PackingCategory(
                category_name="Personal Care & Health Essentials",
                items=[
                    "Personal prescription medications in original pharmacy containers with doctor's prescription copy",
                    "Compact first-aid kit (pain relievers, antacids, rehydration salts, blister bandages)",
                    "Broad-spectrum sunscreen (SPF 30+) & moisturizing lip balm",
                    "Reusable insulated water bottle"
                ]
            )
        ]

        # Destination customs tailored to destination
        if "turkey" in dest_lower or "istanbul" in dest_lower:
            customs = [
                "Mosque Etiquette: Remove shoes at the entrance and place them in the cubbies; women must cover their hair, shoulders, and legs (complimentary scarves are provided at major mosques if needed).",
                "Hospitality & Tea Culture: Accepting a glass of tulip-shaped Turkish tea (çay) is a warm gesture of hospitality and goodwill in shops and restaurants.",
                "Tipping (Bahşiş): In sit-down restaurants in Turkey, a tip of 5-10% in cash left on the table is customary and appreciated for attentive service, even if a service fee is listed.",
                "Bargaining Etiquette: Polite, good-natured bargaining is traditional in the Grand Bazaar and antique shops, but fixed prices apply in grocery stores, modern boutiques, and restaurants."
            ]
        elif "japan" in dest_lower or "tokyo" in dest_lower:
            customs = [
                "Tipping is strictly not customary in Japan and should not be offered; exceptional service is included in the bill.",
                "Transit Etiquette: Keep phone conversations silent on trains and subways; maintain orderly queues on platforms.",
                "Shoes: Remove footwear when entering traditional ryokans, temple halls, and tatami dining spaces.",
                "Waste: Public trash cans are rare; carry a small bag to pack out rubbish to your hotel room or convenience store bins."
            ]
        else:
            customs = [
                f"Greet local shopkeepers and servers politely in {dest_clean}.",
                "Dress respectfully when entering historic religious monuments, cathedrals, and sacred shrines.",
                "Keep a small amount of local currency cash handy for small vendors, street food stalls, and public restrooms.",
                "Be mindful of personal belongings in crowded transit hubs and tourist plazas."
            ]

        tips = TravelSafetyTips(
            weather_summary=f"Seasonal conditions in {dest_clean} generally feature comfortable touring weather in Spring/Autumn (15°C - 24°C / 59°F - 75°F). Prepare layered clothing for cooler waterfront breezes in the evening.",
            visa_and_entry=visa_info,
            local_customs=customs,
            currency_and_payment_tips=(
                f"The official local currency in {dest_clean} is the {transit_info['currency_name']} ({transit_info['currency_code']} {transit_info['currency_symbol']}). "
                f"Credit and debit cards are widely accepted at hotels, modern shops, and sit-down dining. "
                f"However, carry modest amounts of {transit_info['currency_code']} cash for street food stalls, bazaar bargaining, and municipal restrooms."
            ),
            electrical_specs=f"{elec_info['plugs']} • Standard Voltage: {elec_info['voltage']} ({elec_info['frequency']})",
            transit_tips=transit_info["transit_details"],
            embassy_info=mission_info,
            emergency_contacts=[]  # Deprecated and removed
        )

        return {
            "packing_checklist": checklist,
            "travel_tips": tips
        }
