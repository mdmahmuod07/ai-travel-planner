import io
from app.schemas.travel import TravelPlanResponse

def generate_markdown_plan(plan: TravelPlanResponse) -> str:
    """Generates a clean Markdown document of the generated travel plan."""
    md = []
    md.append(f"# Travel Itinerary: {plan.destination}")
    md.append(f"**Trip ID:** `{plan.trip_id}` | **Duration:** {plan.duration_days} Days\n")
    md.append("## Overview")
    md.append(f"{plan.overview}\n")
    md.append(f"**Best Time to Visit:** {plan.best_time_to_visit}\n")
    
    md.append("## Day-by-Day Itinerary")
    for day in plan.itinerary:
        md.append(f"### {day.date_label or f'Day {day.day_number}'}: {day.theme}")
        md.append(f"*{day.summary}*\n")
        for act in day.activities:
            venue_info = f" ({act.venue_name})" if act.venue_name else ""
            md.append(f"- **[{act.time_slot}] {act.title}**{venue_info} ({act.duration}) - *Cost: {act.estimated_cost}*")
            loc_str = act.location
            if act.neighborhood:
                loc_str = f"{act.neighborhood} ({act.location})"
            md.append(f"  - *Location:* {loc_str}")
            md.append(f"  - {act.description}")
            if act.tips:
                md.append(f"  - *Tip:* {act.tips}")
            if act.search_query:
                md.append(f"  - *Map Query:* `{act.search_query}`")
        md.append(f"\n*Estimated Daily Cost:* {day.daily_estimated_cost}\n")

    md.append("## Accommodation Recommendations")
    for acc in plan.accommodations:
        md.append(f"### {acc.name} ({acc.rating})")
        md.append(f"- **Type:** {acc.type} | **Location:** {acc.neighborhood}")
        md.append(f"- **Price:** {acc.price_per_night} / night")
        md.append(f"- **Why recommended:** {acc.why_recommended}\n")

    md.append("## Dining & Culinary Guide")
    for res in plan.dining:
        md.append(f"- **{res.name}** ({res.cuisine})")
        md.append(f"  - *Meal:* {res.meal_type} | *Neighborhood:* {res.neighborhood} | *Price:* {res.price_range}")
        md.append(f"  - *Must Try:* {res.must_try_dish}")
        if res.dietary_friendly:
            md.append(f"  - *Dietary options:* {', '.join(res.dietary_friendly)}")

    if plan.budget_breakdown:
        b = plan.budget_breakdown
        md.append("\n## Budget Summary")
        md.append(f"- **Accommodation:** {b.accommodation}")
        md.append(f"- **Dining:** {b.dining}")
        md.append(f"- **Activities & Sightseeing:** {b.activities_and_tours}")
        md.append(f"- **Local Transport:** {b.local_transport}")
        md.append(f"- **Miscellaneous:** {b.miscellaneous}")
        md.append(f"### **Total Estimated Cost:** {b.total_estimated} {b.currency}\n")

    if plan.packing_checklist:
        md.append("## Packing Checklist")
        for cat in plan.packing_checklist:
            md.append(f"### {cat.category_name}")
            for item in cat.items:
                md.append(f"- [ ] {item}")

    if plan.travel_tips:
        t = plan.travel_tips
        md.append("\n## Travel & Safety Essentials")
        md.append(f"- **Weather:** {t.weather_summary}")
        md.append(f"- **Visa & Entry Guidance:** {t.visa_and_entry}")
        if t.electrical_specs:
            md.append(f"- **Electrical & Power Specifications:** {t.electrical_specs}")
        if t.transit_tips:
            md.append(f"- **Contactless Transit & Local Mobility:** {t.transit_tips}")
        if t.local_customs:
            md.append("- **Local Customs & Etiquette:**")
            for custom in t.local_customs:
                md.append(f"  - {custom}")
        md.append(f"- **Payment & Currency:** {t.currency_and_payment_tips}")
        if t.embassy_info:
            md.append(f"- **Consular & Diplomatic Mission Information:**\n  {t.embassy_info}")

    return "\n".join(md)
