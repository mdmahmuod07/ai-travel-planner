from abc import ABC, abstractmethod
from typing import Dict, Any, Callable, Awaitable, Optional
from app.schemas.travel import TravelRequest

class BaseAgent(ABC):
    def __init__(self, agent_id: str, name: str, role: str):
        self.agent_id = agent_id
        self.name = name
        self.role = role

    @abstractmethod
    async def process(self, request: TravelRequest, context: Dict[str, Any], log_cb: Optional[Callable[[str, str], Awaitable[None]]] = None) -> Dict[str, Any]:
        """
        Processes the request using prior context, optional external LLM, or fallback domain logic.
        Sends real-time updates via log_cb if provided.
        """
        pass
