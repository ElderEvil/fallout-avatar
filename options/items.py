from .factions import Faction

# Define common equipment available to all factions
common_equipment = {
    "outfits": [
        "Casual Wastelander Clothes",
        "Scavenger Gear",
        "Tattered Field Jacket",
    ],
    "weapons": [
        "10mm Pistol",
        "Pipe Pistol",
        "Hunting Rifle",
    ],
    "accessories": [
        "Goggles (worn on forehead)",
        "Gloves (fingerless leather)",
        "Bandolier (slung across chest)",
    ],
    "objects": [
        "Stimpak (ready to inject)",
        "Bottlecap Pouch (jingling softly)",
    ],
}

# Define faction-specific equipment using Faction enum as keys
faction_equipment = {
    Faction.VAULT_DWELLER: {
        "outfits": [
            "Blue Vault Suit",
            "Vault Security Armor",
        ],
        "weapons": [
            "10mm Pistol",
            ".44 Magnum",
            "Security Baton",
        ],
        "accessories": [
            "Vault-Tec Badge (pinned on outfit)",
            "Pip-Boy (glowing screen)",
        ],
        "objects": [
            "Pip-Boy (glowing screen)",
            "Holotape (examining closely)",
        ],
    },
    Faction.BROTHERHOOD_OF_STEEL: {
        "outfits": [
            "Brotherhood Combat Armor",
            "Power Armor T-51",
            "Combat Armor",
        ],
        "weapons": [
            "Laser Rifle",
            "Gatling Laser",
            "Power Fist",
            "Gauss Rifle",
        ],
        "accessories": [
            "Faction Insignia (etched on armor)",
            "Shoulder Pads (metal salvaged)",
        ],
        "objects": [
            "Fusion Core (faint glow)",
            "Holotape (examining closely)",
        ],
    },
    Faction.THE_INSTITUTE: {
        "outfits": ["Synth Uniform", "Institute Lab Coat", "Clean Jumpsuit"],
        "weapons": ["Institute Laser Pistol", "Plasma Rifle", "Synth Melee Weapon"],
        "accessories": [
            "Cybernetic Implant (glowing eye, exposed wiring)",
            "Synth Component",
        ],
        "objects": ["Holotape (examining closely)", "Institute Schematic"],
    },
    Faction.RAIDERS: {
        "outfits": [
            "Raider Leathers",
            "Spike Armor",
            "Metal Armor",
        ],
        "weapons": [
            "Pipe Rifle",
            "Board with Nails",
            "Pipe Pistol",
            "Flamer",
        ],
        "accessories": [
            "War Paint (tribal markings on face or arms)",
            "Scar (deep, battle-worn)",
        ],
        "objects": [
            "Nuka-Cola Bottle (condensation forming)",
        ],
    },
    Faction.ENCLAVE: {
        "outfits": [
            "Settler Outfit",
            "Casual Wastelander Clothes",
            "Power Armor X-01",
            "Combat Armor",
        ],
        "weapons": [
            "Plasma Rifle",
            "Baseball Bat",
            "Deathclaw Gauntlet",
            "Ripper",
        ],
        "accessories": [],
    },
    Faction.SUPER_MUTANT_TRIBE: {
        "outfits": [
            "Super Mutant Harness",
            "Super Mutant Cages",
            "Super Mutant Armor",
        ],
        "weapons": [
            "Super Sledge",
            "Board with Nails",
            "Pipe Rifle",
            "Minigun",
        ],
        "accessories": [
            "Bone Necklace (tribal decoration)",
            "Scarred War Paint (intimidating design)",
        ],
        "objects": [
            "Meat Bag (intact and reeking)",
            "Fusion Core (loot from scavenging)",
        ],
    },
    Faction.CHILDREN_OF_ATOM: {
        "outfits": [
            "Rags of the Children of Atom",
            "Glowing robes",
        ],
        "weapons": ["Gamma Gun", "Wrench"],
        "accessories": ["Radiation-Resistant Mask", "Glowing Tattoo"],
        "objects": ["Glowing Mushroom"],
    },
    Faction.RAILROAD: {
        "outfits": [
            "Railroad Armored Coat",
            "Disguise (various)",
            "Wastelander Clothing",
        ],
        "weapons": ["Silenced Pistol", "Combat Knife", "Deliverer"],
        "accessories": ["Railroad Symbol", "Concealed Radio"],
        "objects": ["Encrypted Message"],
    },
    Faction.NCR: {
        "outfits": [
            "NCR Ranger Combat Armor",
            "NCR Trooper Uniform",
            "NCR Officer Uniform",
        ],
        "weapons": ["Service Rifle", "Ranger Sequoia", "Anti-Material Rifle"],
        "accessories": ["NCR Flag Patch", "NCR Dog Tags"],
        "objects": ["NCR Veteran's Duster"],
    },
    Faction.CAESARS_LEGION: {
        "outfits": ["Legionary Armor", "Centurion Armor", "Praetorian Armor"],
        "weapons": ["Machete", "Throwing Spears", "Chainsaw"],
        "accessories": ["Caesar's Legion Branding", "Bear Pelt"],
        "objects": ["Legion Denarius"],
    },
    Faction.NONE: {
        "outfits": ["None"],
        "weapons": ["None"],
        "accessories": ["None"],
        "objects": ["None"],
    },
}
