from pydantic import BaseModel, Field
from typing import Literal


class Character(BaseModel):
    race: Literal["Human", "Ghoul", "Super Mutant", "Synth"]
    gender: Literal["Male", "Female", "Other"]
    skin_tone: str
    body_type: str
    age: int | None = Field(None, ge=18, le=80)
    hair: str | None = None
    headgear: str
    expression: str
    hair_color: str | None = None
    beard: str | None = None
    faction: str
    outfit: str
    weapon: str
    object_held: str
    accessory: str
    pose: str
    background: str
