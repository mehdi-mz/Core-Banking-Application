from pydantic import BaseModel

class MessageResponseDTO(BaseModel):
    message: str