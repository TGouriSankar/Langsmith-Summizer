from datetime import datetime,timezone
from dataclasses import dataclass,asdict
from langchain_core.callbacks.base import BaseCallbackHandler
from pathlib import Path
from typing import Any, Dict, List, Tuple, Union
from langchain.schema.output import LLMResult
import json
from langchain_groq import ChatGroq

@dataclass
class Event:
    event: str
    timestamp: str
    text: str

def _current_time() -> str:
    return datetime.now(timezone.utc).isoformat()

class LLMCallbackHandler(BaseCallbackHandler):
    def __init__(self, log_path: Path):
        self.log_path = log_path
    
    def on_llm_start(self, serialized: Dict[str,Any], prompts:List[str], **Kwargs:Any) -> Any:
        """Run when LLM start running. """
        assert len(prompts) == 1
        event = Event(event="llm_start", timestamp=_current_time(), text=prompts[0])
        with self.log_path.open("a", encoding="utf-8") as file:
            file.write(json.dumps(asdict(event)) + "\n")

    def on_ll_end(self, response: LLMResult, **kwargs: Any) -> Any:
        """Run when LLM ends running. """
        generation = response.generations[-1][-1].message.context
        event = Event(event="llm_end", timestamp=_current_time(), text=generation)
        with self.log_path.open("a", encoding="utf-8") as file:
            file.write(json.dumps(asdict(event)) + "\n")

llm = ChatGroq(
    model="llama3-70b-8192",
    temperature=0,
    callbacks=[LLMCallbackHandler(Path("prompts.json"))]
    )

