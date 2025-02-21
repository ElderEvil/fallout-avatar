# Hair Options
from pydantic_settings import BaseSettings, SettingsConfigDict

races = ["Human", "Ghoul", "Super Mutant", "Synth"]

haircuts = {
    "Human": ["Short Hair", "Long Hair", "Ponytail Haircut", "Mohawk Haircut"],
    "Ghoul": ["Short Hair", "Messy Hair", "Mohawk Haircut", "Burned Hair"],
    "Super Mutant": [],
    "Synth": ["Short Hair", "Slicked Back Hair"],
}

# Headgear Options (Items that cover the head)
headgear = {
    "Human": [
        "None",
        "Baseball Cap",
        "Bandana",
        "Raider Mask",
        "Combat Helmet",
        "Gas Mask",
    ],
    "Ghoul": ["None", "Bandana", "Raider Mask"],
    "Super Mutant": ["None", "Scarred", "Spiked", "Metal Helmet"],
    "Synth": ["None", "Hood", "Metallic Plating"],
}

# Headgear items that fully cover hair (prevents hair selection)
FULLY_COVERING_HEADGEAR = {
    "Combat Helmet",
    "Gas Mask",
    "Raider Mask",
    "Metal Helmet",
    "Hood",
    "Metallic Plating",
}

# Character Attributes
skin_tone_options = {
    "Human": ["Pale", "Fair", "Tan", "Brown", "Dark"],
    "Ghoul": ["Pale Grey", "Grey"],
    "Super Mutant": ["Green", "Dark Green"],
    "Synth": ["Synthetic Skin", "Metallic"],
}

body_type_options = {
    "Human": ["Slim", "Athletic", "Muscular", "Heavy"],
    "Ghoul": ["Slim", "Average", "Worn Down"],
    "Super Mutant": ["Lean", "Muscular", "Bulkier", "Heavy"],
    "Synth": ["Standard", "Combat-Ready", "Heavy-Plated"],
}

faction_options = [
    "None",
    "Vault Dweller",
    "Brotherhood of Steel",
    "Enclave",
    "Minutemen",
    "Raider",
    "Super Mutant Tribe",
    "The Institute",
    "New California Republic (NCR)",
]

outfit_options = [
    "Blue Vault Suit",
    "Combat Armor",
    "Raider Gear",
    "Casual Clothes",
    "Scrap Armor",
    "Power Armor",
    "Lab Coat",
    "Wasteland Survivor Gear",
    "NCR Ranger Armor",
]

weapon_options = [
    "None",
    "10mm Pistol",
    "Laser Rifle",
    "Plasma Pistol",
    "Hunting Rifle",
    "Baseball Bat",
    "Board with nails",
    "Power Fist",
    "Junk Jet",
    "Super Sledge",
    "Alien Blaster",
    "Minigun",
]

expression_options = [
    "Neutral",
    "Smiling",
    "Determined",
    "Heroic",
    "Intense Focus",
    "Suspicious",
    "Angry",
    "Battle Cry",
    "Shocked",
    "Sad",
    "Laughing",
]

# Archetypes
archetypes = {
    "Vault Dweller": {
        "race": "Human",
        "faction": "Vault Dweller",
        "outfit": "Blue Vault Suit",
        "weapon": "10mm Pistol",
    },
    "Brotherhood Knight": {
        "race": "Human",
        "faction": "Brotherhood of Steel",
        "outfit": "Power Armor",
        "weapon": "Laser Rifle",
    },
    "Enclave Soldier": {
        "race": "Human",
        "faction": "Enclave",
        "outfit": "Power Armor",
        "weapon": "Plasma Pistol",
    },
    "Raider Warlord": {
        "race": "Human",
        "faction": "Raider",
        "outfit": "Raider Gear",
        "weapon": "Minigun",
    },
    "Super Mutant Brute": {
        "race": "Super Mutant",
        "faction": "Super Mutant Tribe",
        "outfit": "Scrap Armor",
        "weapon": "Super Sledge",
    },
    "Institute Courser": {
        "race": "Synth",
        "faction": "The Institute",
        "outfit": "Combat Armor",
        "weapon": "Laser Rifle",
    },
    "NCR Ranger": {
        "race": "Human",
        "faction": "New California Republic (NCR)",
        "outfit": "NCR Ranger Armor",
        "weapon": "Hunting Rifle",
    },
    "Ghoul Mercenary": {
        "race": "Ghoul",
        "faction": "None",
        "outfit": "Scrap Armor",
        "weapon": "Plasma Pistol",
    },
}


race_descriptions = {
    "Ghoul": "A Ghoul is a human with visible radiation scarring and leathery, slightly decayed skin.Their facial  features are worn and aged, but they still retain human expressions and emotions. Their eyes may appear sunken, and their skin tone varies from pale to ashen, but they remain distinctly humanoid.",
    "Super Mutant": "A Super Mutant is a large, muscular humanoid with green or dark green skin.Their body appears  strengthened by mutation, giving them a powerful and bulky frame. They have rough skin and battle scars but still maintain an expressive, intelligent face.",
    "Synth": "A Synth is a humanoid with artificial skin, appearing almost indistinguishable from a human.Some areas  may have subtle seams or metallic plating, but their expressions and body language are fully natural, resembling a person with advanced cybernetic enhancements.",
}


accessory_options = [
    "None",
    "Ear Piercings",
    "Goggles",
    "Gloves",
    "Necklace",
    "Bandolier",
    "Shoulder Pads",
    "Eyepatch",
    "Facial Scar",
    "Cybernetic Arm",
    "Power Armor Components",
]


pose_options = [
    "Standing with arms crossed",
    "Thumbs up",
    "Leaning against a wall",
    "Pip-Boy check stance",
    "Saluting",
    "Aiming down sights",
    "Stealth crouching",
    "Holding a weapon",
    "Running",
    "Action pose with explosion behind",
]


object_options = [
    "None",
    "Pip-Boy",
    "Nuka-Cola Bottle",
    "First Aid Kit",
    "Bobblehead",
    "Mini Nuke",
]


background_options = [
    "Vault Interior",
    "Wasteland Ruins",
    "Brotherhood of Steel Base",
    "Nuka-Cola Factory",
    "Diamond City Market",
    "Radiation Storm",
    "The Glowing Sea",
    "Institute Laboratory",
    "Red Rocket Truck Stop",
    "Destroyed Highway",
]


class Settings(BaseSettings):
    OPENAI_API_KEY: str
    MINIO_HOST: str
    MINIO_CUSTOM_PORT: int
    MINIO_ROOT_USER: str
    MINIO_ROOT_PASSWORD: str
    MINIO_PUBLIC_BUCKET_WHITELIST: list[str] = ["fastapi-minio"]

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()