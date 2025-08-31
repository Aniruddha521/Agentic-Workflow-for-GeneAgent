from pydantic import BaseModel

class ProcessState(BaseModel):
    process_names: str = ""
    detail: str = ""

    def __or__(self, other):
        if not isinstance(other, ProcessState):
            return NotImplemented
        return ProcessState(
            process_names=self.process_names or other.process_names,
            detail=self.detail if len(self.detail) > len(other.detail) else other.detail
        )