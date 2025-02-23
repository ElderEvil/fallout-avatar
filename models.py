from pydantic import BaseModel, Field

from options.factions import Faction
from options.races import GhoulFeralness, SuperMutantMutation, SynthType, Race, Gender

STATE_OF_BEING_TYPE = GhoulFeralness | SuperMutantMutation | SynthType


class Character(BaseModel):
    race: Race
    gender: Gender
    skin_tone: str
    body_type: str
    age: int | None = Field(None, ge=18, le=80, description="Only for human")
    state_of_being: STATE_OF_BEING_TYPE | None = Field(
        None, description="For ghouls/supermutants/synths"
    )
    headgear: str
    hair: str | None = None
    hair_color: str | None = None
    expression: str
    beard: str | None = None
    faction: Faction
    outfit: str
    weapon: str
    object_held: str
    accessory: str
    pose: str
    background: str
