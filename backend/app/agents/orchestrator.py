import asyncio
import uuid
import logging
import traceback
from datetime import datetime
from typing import Dict, Any, List, Callable, Awaitable, AsyncGenerator, Optional
from app.schemas.travel import (
    TravelRequest, TravelPlanResponse, AgentStepLog, RefineRequest, DayItinerary
)
from app.agents.destination_agent import DestinationAgent, get_city_lat_lng, get_jittered_coords
from app.agents.itinerary_agent import ItineraryAgent, enforce_zero_repetition
from app.agents.budget_agent import BudgetAgent
from app.agents.dining_agent import DiningAgent
from app.agents.packing_agent import PackingAgent
from app.services.llm_factory import llm_provider
from app.services.destination_knowledge import get_authentic_destination

logger = logging.getLogger("orchestrator")

class MultiAgentOrchestrator:
    def __init__(self):
        self.destination_agent = DestinationAgent()
        self.itinerary_agent = ItineraryAgent()
        self.budget_agent = BudgetAgent()
        self.dining_agent = DiningAgent()
        self.packing_agent = PackingAgent()

    async def generate_trip_plan(
        self,
        request: TravelRequest,
        log_callback: Optional[Callable[[str, str, str], Awaitable[None]]] = None
    ) -> TravelPlanResponse:
        """
        Executes the full multi-agent pipeline sequentially & concurrently where appropriate,
        building up context and logging every agent action step.
        """
        trip_id = f"trip_{uuid.uuid4().hex[:8]}"
        logs: List[AgentStepLog] = []

        async def _log(agent_id: str, message: str, status: str = "working"):
            agent_names = {
                "destination_specialist": "Destination Specialist",
                "itinerary_orchestrator": "Itinerary Orchestrator",
                "budget_specialist": "Budget & Accommodation Specialist",
                "dining_specialist": "Dining Specialist",
                "packing_specialist": "Packing & Safety Specialist"
            }
            entry = AgentStepLog(
                agent_id=agent_id,
                agent_name=agent_names.get(agent_id, agent_id),
                status=status,
                message=message,
                timestamp=datetime.now().strftime("%H:%M:%S")
            )
            logs.append(entry)
            if log_callback:
                await log_callback(agent_id, message, status)

        context: Dict[str, Any] = {}

        try:
            # 1. Destination Agent
            await _log("destination_specialist", f"Initializing research on {request.destination}...")
            dest_result = await self.destination_agent.process(
                request, context, lambda aid, msg: _log(aid, msg, "working")
            )
            context["destination_specialist"] = dest_result
            await _log("destination_specialist", f"Completed attraction & landmark analysis.", "completed")

            # 2. Parallel Agent Execution: Itinerary, Budget, Dining, Packing
            await _log("itinerary_orchestrator", f"Dispatching agents for day-by-day scheduling, budget allocation, food curation, and packing checklist...")

            # Run Itinerary, Budget, Dining, Packing concurrently with context
            itinerary_task = self.itinerary_agent.process(request, context, lambda aid, msg: _log(aid, msg, "working"))
            budget_task = self.budget_agent.process(request, context, lambda aid, msg: _log(aid, msg, "working"))
            dining_task = self.dining_agent.process(request, context, lambda aid, msg: _log(aid, msg, "working"))
            packing_task = self.packing_agent.process(request, context, lambda aid, msg: _log(aid, msg, "working"))

            itinerary_res, budget_res, dining_res, packing_res = await asyncio.gather(
                itinerary_task, budget_task, dining_task, packing_task
            )
        except Exception as e:
            logger.error(f"Error in multi-agent orchestration pipeline: {e}\n{traceback.format_exc()}")
            raise e

        # Enforce strict zero repetition across all days and slots
        base_lat, base_lng = get_city_lat_lng(request.destination)
        auth_data = get_authentic_destination(request.destination)
        catalog = auth_data.get("landmarks", []) if auth_data else None
        itinerary_res = enforce_zero_repetition(
            itinerary_res,
            destination=request.destination,
            currency=request.currency,
            base_lat=base_lat,
            base_lng=base_lng,
            available_catalog=catalog
        )

        await _log("itinerary_orchestrator", "Synthesizing all agent outputs into final travel plan...", "completed")

        return TravelPlanResponse(
            trip_id=trip_id,
            destination=request.destination.strip().title(),
            duration_days=request.duration_days,
            overview=dest_result.get("overview", ""),
            best_time_to_visit=dest_result.get("best_time_to_visit", ""),
            itinerary=itinerary_res,
            accommodations=budget_res.get("accommodations", []),
            dining=dining_res,
            budget_breakdown=budget_res.get("budget_breakdown"),
            packing_checklist=packing_res.get("packing_checklist", []),
            travel_tips=packing_res.get("travel_tips"),
            agent_logs=logs
        )

    async def refine_trip_plan(
        self,
        refine_req: RefineRequest,
        log_callback: Optional[Callable[[str, str, str], Awaitable[None]]] = None
    ) -> TravelPlanResponse:
        """
        Conversational Multi-Agent refinement: Updates an existing trip plan
        based on the user's natural language tweak instructions.
        """
        current_plan = refine_req.current_plan
        instruction = refine_req.user_instruction
        base_lat, base_lng = get_city_lat_lng(current_plan.destination)

        async def _log(agent_id: str, message: str, status: str = "working"):
            if log_callback:
                await log_callback(agent_id, message, status)

        await _log("itinerary_orchestrator", f"Processing refinement request: '{instruction}'...")
        await asyncio.sleep(0.5)

        system_prompt = (
            "You are an expert multi-agent travel refinement system. "
            "Given an existing travel plan JSON and a user's refinement instruction, "
            "modify the itinerary, activities, dining recommendations, or budget where requested. "
            "Return the full updated TravelPlanResponse JSON structure."
        )

        user_prompt = f"""
        User Refinement Instruction: "{instruction}"
        Current Plan JSON: {current_plan.model_dump_json()}
        """

        llm_result = await llm_provider.generate_json(system_prompt, user_prompt)

        if llm_result:
            try:
                updated_plan = TravelPlanResponse(**llm_result)
                auth_data = get_authentic_destination(current_plan.destination)
                catalog = auth_data.get("landmarks", []) if auth_data else None
                curr_plan_curr = updated_plan.budget_breakdown.currency if updated_plan.budget_breakdown else "INR"
                updated_plan.itinerary = enforce_zero_repetition(
                    updated_plan.itinerary,
                    destination=current_plan.destination,
                    currency=curr_plan_curr,
                    base_lat=base_lat,
                    base_lng=base_lng,
                    available_catalog=catalog
                )
                await _log("itinerary_orchestrator", "Successfully refined travel plan with AI Agents!", "completed")
                return updated_plan
            except Exception as e:
                logger.error(f"Error parsing refined LLM plan: {e}\n{traceback.format_exc()}")

        # Rule-based fallback refinement logic
        await _log("itinerary_orchestrator", "Applying custom multi-agent refinement to active schedule...", "working")
        await asyncio.sleep(0.5)

        updated_plan_dict = current_plan.model_dump()
        inst_lower = instruction.lower()
        curr = updated_plan_dict.get("budget_breakdown", {}).get("currency", "INR")
        dest_str = current_plan.destination.lower()
        is_tokyo = "tokyo" in dest_str
        is_istanbul = "istanbul" in dest_str or "turkey" in dest_str
        is_paris = "paris" in dest_str or "france" in dest_str

        # Check if user mentioned a specific day or feature
        target_day_num = None
        for d_num in range(1, 15):
            if f"day {d_num}" in inst_lower or f"day-{d_num}" in inst_lower:
                target_day_num = d_num
                break
        target_day = target_day_num if target_day_num is not None else 1

        if "nature" in inst_lower or "park" in inst_lower or "outdoor" in inst_lower:
            for day in updated_plan_dict["itinerary"]:
                if day["day_number"] != target_day:
                    continue
                for act in day["activities"]:
                    if act["time_slot"].lower() == "afternoon":
                        if is_paris:
                            act["title"] = "Jardin du Luxembourg & Medici Fountain Promenade"
                            act["venue_name"] = "Jardin du Luxembourg"
                            act["neighborhood"] = "6th Arrondissement (Saint-Germain)"
                            act["search_query"] = "Jardin du Luxembourg, Paris"
                            act["description"] = "Stroll the Medici fountain, tree-lined promenades, and flowerbeds of the Luxembourg Gardens."
                            act["location"] = "Jardin du Luxembourg, 75006 Paris, France"
                            act["category"] = "Nature & Parks"
                            act["lat"] = 48.8462
                            act["lng"] = 2.3444
                        elif is_tokyo:
                            act["title"] = "Shinjuku Gyoen National Garden & Greenhouse Walk"
                            act["venue_name"] = "Shinjuku Gyoen National Garden"
                            act["neighborhood"] = "Shinjuku, Shinjuku Ward"
                            act["search_query"] = "Shinjuku Gyoen National Garden, Tokyo"
                            act["description"] = "Stroll along traditional Japanese landscaped ponds, maple walking paths, and historic imperial greenhouses."
                            act["location"] = "Shinjuku, Shinjuku Ward, Tokyo"
                            act["category"] = "Nature & Parks"
                            act["lat"] = 35.6852
                            act["lng"] = 139.7100
                        elif is_istanbul:
                            act["title"] = "Gülhane Park & Historic Bosphorus Gardens Walk"
                            act["venue_name"] = "Gülhane Park"
                            act["neighborhood"] = "Cankurtaran, Fatih"
                            act["search_query"] = "Gülhane Park, Fatih, Istanbul"
                            act["description"] = "Stroll through the historic imperial gardens of the Ottoman sultans, shaded by centuries-old plane trees with sweeping vistas over the Bosphorus strait."
                            act["location"] = "Cankurtaran, Fatih, Istanbul"
                            act["category"] = "Nature & Parks"
                            act["lat"] = 41.0135
                            act["lng"] = 28.9818
                        else:
                            lat, lng = get_jittered_coords(base_lat, base_lng)
                            clean_dest = current_plan.destination.strip().title()
                            act["title"] = f"Central Botanical Gardens Walk in {clean_dest}"
                            act["venue_name"] = f"Central Botanical Gardens of {clean_dest}"
                            act["neighborhood"] = "City Center"
                            act["search_query"] = f"Botanical Gardens, {clean_dest}"
                            act["description"] = f"Relaxing outdoor walk surrounded by scenic walking paths, local flora, and lush tree canopies."
                            act["location"] = f"Central District, {clean_dest}"
                            act["category"] = "Nature & Outdoor"
                            act["lat"] = lat
                            act["lng"] = lng
                break

        elif "museum" in inst_lower or "art" in inst_lower or "culture" in inst_lower:
            for day in updated_plan_dict["itinerary"]:
                if day["day_number"] != target_day:
                    continue
                for act in day["activities"]:
                    if act["time_slot"].lower() == "morning":
                        if is_paris:
                            act["title"] = "Musée d'Orsay Impressionist Masterpieces"
                            act["venue_name"] = "Musée d'Orsay"
                            act["neighborhood"] = "7th Arrondissement (Left Bank)"
                            act["search_query"] = "Musée d'Orsay, Paris"
                            act["description"] = "Admire peerless Impressionist collections by Monet, Van Gogh, and Renoir inside the Beaux-Arts railway terminal."
                            act["location"] = "1 Rue de la Légion d'Honneur, 75007 Paris, France"
                            act["category"] = "Culture & Art"
                            act["lat"] = 48.8599
                            act["lng"] = 2.3266
                        elif is_tokyo:
                            act["title"] = "Tokyo National Museum & Ueno Cultural Park"
                            act["venue_name"] = "Tokyo National Museum"
                            act["neighborhood"] = "Ueno Park, Taito Ward"
                            act["search_query"] = "Tokyo National Museum, Ueno, Tokyo"
                            act["description"] = "Explore ancient samurai armor, national treasures, and curated Japanese lacquerware with expert gallery exhibits."
                            act["location"] = "Ueno Park, Taito Ward, Tokyo"
                            act["category"] = "Culture & Art"
                            act["lat"] = 35.7188
                            act["lng"] = 139.7765
                        elif is_istanbul:
                            act["title"] = "Istanbul Archaeological Museums & Imperial Antiquities"
                            act["venue_name"] = "Istanbul Archaeological Museums (İstanbul Arkeoloji Müzeleri)"
                            act["neighborhood"] = "Cankurtaran, Fatih"
                            act["search_query"] = "Istanbul Archaeological Museums, Fatih, Istanbul"
                            act["description"] = "Discover the celebrated Alexander Sarcophagus, ancient Mesopotamian artifacts, and Ottoman imperial antiquity halls located next to Topkapi Palace."
                            act["location"] = "Cankurtaran, Fatih, Istanbul"
                            act["category"] = "Culture & Art"
                            act["lat"] = 41.0117
                            act["lng"] = 28.9812
                        else:
                            lat, lng = get_jittered_coords(base_lat, base_lng)
                            clean_dest = current_plan.destination.strip().title()
                            act["title"] = f"National Historical Museum & Gallery in {clean_dest}"
                            act["venue_name"] = f"National Museum of {clean_dest}"
                            act["neighborhood"] = "Cultural District"
                            act["search_query"] = f"National Museum, {clean_dest}"
                            act["description"] = f"Immerse in regional heritage, historical artifacts, and curated art exhibitions with audio tour."
                            act["location"] = f"Cultural Quarter, {clean_dest}"
                            act["category"] = "Culture & Art"
                            act["lat"] = lat
                            act["lng"] = lng
                break

        elif "budget" in inst_lower or "cheaper" in inst_lower:
            updated_plan_dict["budget_breakdown"]["saving_tips"].insert(0, "Refined for lower costs: take public metro and enjoy street food markets!")
            cost_label = "₹2,500 - ₹4,500" if curr == "INR" else "$30 - $60"
            for day in updated_plan_dict["itinerary"]:
                day["daily_estimated_cost"] = cost_label

        elif "luxury" in inst_lower or "upgrade" in inst_lower:
            cost_label = "₹20,000 - ₹35,000" if curr == "INR" else "$250 - $500"
            for day in updated_plan_dict["itinerary"]:
                day["daily_estimated_cost"] = cost_label

        # Log completion
        step_entry = AgentStepLog(
            agent_id="itinerary_orchestrator",
            agent_name="Itinerary Orchestrator",
            status="completed",
            message=f"Refinement applied: '{instruction}'",
            timestamp=datetime.now().strftime("%H:%M:%S")
        )
        updated_plan_dict["agent_logs"].append(step_entry.model_dump())

        # Enforce zero repetition on refined itinerary
        auth_data = get_authentic_destination(current_plan.destination)
        catalog = auth_data.get("landmarks", []) if auth_data else None
        day_objs = [DayItinerary(**d) for d in updated_plan_dict["itinerary"]]
        day_objs = enforce_zero_repetition(
            day_objs,
            destination=current_plan.destination,
            currency=curr,
            base_lat=base_lat,
            base_lng=base_lng,
            available_catalog=catalog
        )
        updated_plan_dict["itinerary"] = [d.model_dump() for d in day_objs]

        await _log("itinerary_orchestrator", "Refinement complete! Itinerary updated.", "completed")
        return TravelPlanResponse(**updated_plan_dict)

orchestrator = MultiAgentOrchestrator()
