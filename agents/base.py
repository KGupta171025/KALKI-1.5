import time
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from services.inference import ILLMProvider, LLMProviderFactory

class BaseAgent(ABC):
    """
    Abstract base class for all KALKI agent personas.
    Enforces independent prompts, tools, memory context, and health monitoring.
    """
    def __init__(
        self, 
        name: str, 
        system_prompt: str, 
        llm: Optional[ILLMProvider] = None,
        tools: Optional[List[str]] = None
    ):
        self.name = name
        self.system_prompt = system_prompt
        self.llm = llm or LLMProviderFactory.get_provider()
        self.tools = tools or []
        self.memory: List[Dict[str, Any]] = []
        self.task_queue: List[Dict[str, Any]] = []
        self.health_status = "HEALTHY"
        self.last_active = time.time()

    def add_to_queue(self, task: dict):
        self.task_queue.append(task)

    def check_health(self) -> Dict[str, Any]:
        """
        Monitors agent health metrics and task queue lengths.
        """
        return {
            "agent_name": self.name,
            "status": self.health_status,
            "queue_depth": len(self.task_queue),
            "last_active": self.last_active
        }

    async def execute_task(self, task_instruction: str, context: Optional[dict] = None) -> Dict[str, Any]:
        self.last_active = time.time()
        
        # Build prompt incorporating agent-specific system instructions and memory
        messages = [
            {"role": "system", "content": self.system_prompt},
        ]
        # Inject memory context
        for mem in self.memory[-5:]:
            messages.append({"role": "user", "content": mem["input"]})
            messages.append({"role": "assistant", "content": mem["output"]})
            
        messages.append({"role": "user", "content": f"Task: {task_instruction}\nContext: {context or {}}"})

        try:
            # Delegate to abstract LLM model adapter
            response = await self.llm.generate_completion(messages=messages)
            
            # Save to agent-local episodic memory
            self.memory.append({
                "input": task_instruction,
                "output": response["text"],
                "timestamp": time.time()
            })
            
            return {
                "status": "SUCCESS",
                "agent": self.name,
                "output": response["text"],
                "tools_used": self.tools
            }
        except Exception as e:
            self.health_status = "DEGRADED"
            return {
                "status": "FAILED",
                "agent": self.name,
                "error": str(e)
            }
