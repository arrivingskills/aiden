from dataclasses import dataclass, field
from typing import List, Callable


@dataclass
class Quest:
    name: str
    description: str
    is_complete: bool = False
    on_complete: Callable[[], None] = lambda: None


@dataclass
class QuestLog:
    quests: List[Quest] = field(default_factory=list)
    current_index: int = 0

    def add(self, quest: Quest):
        self.quests.append(quest)

    def current(self) -> Quest:
        return self.quests[self.current_index]

    def complete_current(self):
        q = self.current()
        if not q.is_complete:
            q.is_complete = True
            try:
                q.on_complete()
            except Exception:
                pass
        if self.current_index < len(self.quests) - 1:
            self.current_index += 1

    def all_complete(self) -> bool:
        return all(q.is_complete for q in self.quests)

    def objective_text(self) -> str:
        q = self.current()
        status = "(done)" if q.is_complete else ""
        return f"Objective: {q.description} {status}"
