from .races import Race

haircuts = {
    Race.HUMAN: [
        "Short Hair",
        "Long Hair",
        "Ponytail",
        "Mohawk",
        "Buzz Cut",
        "Curly Hair",
        "Bun",
        "Braided Hair",
        "Wavy Hair",
        "Dreadlocks",
    ],
    Race.GHOUL: [
        "Patchy Hair",
        "Stringy Hair",
        "Messy Hair",
        "Mohawk",
        "Burned Scalp",
        "Radiation-Scarred",
        "Thinning Hair",
        "Wispy Remains",
    ],
    Race.SUPER_MUTANT: [
        "Bald",
        "Scalp Ridges",
        "Patchy Tufts",
        "Mohawk",
        "Thick Stubble",
        "War Paint Scalp",
    ],
    Race.SYNTH: [
        "Clean Cut",
        "Slicked Back",
        "Military Precision Cut",
        "Exposed Circuits",
        "Synthetic Fiber Weave",
        "Metallic Sheen Hair",
    ],
}

# Headgear Options by Race (with diverse selections)
headgear = {
    Race.HUMAN: [
        "Baseball Cap",
        "Bandana",
        "Combat Helmet",
        "Gas Mask",
        "Cowboy Hat",
        "Bowler Hat",
        "Fedora",
        "Ushanka",
        "Beanie",
        "Military Beret",
        "Newsboy Cap",
        "Vault-Tec Helmet",
        "Hooded Coat",
    ],
    Race.GHOUL: [
        "Tattered Bandana",
        "Raider Cage Mask",
        "Wrapped Head Bandages",
        "Radiation Suit Hood",
        "Scrapped Metal Helmet",
        "Faded Cap",
        "Glowing One Crown",
        "Leather Hood",
    ],
    Race.SUPER_MUTANT: [
        "Metal Helmet",
        "Spiked Helmet",
        "Chain Headdress",
        "Skull Trophy",
        "Heavy Plate Helmet",
        "Makeshift Face Guard",
        "Mutant Battle Helm",
    ],
    Race.SYNTH: [
        "Institute Hood",
        "Metallic Plating",
        "Stealth Field Generator",
        "Neural Interface Helmet",
        "Courser Hood",
        "Synth Component Display",
        "Reinforced Circuitry Cap",
    ],
}

# Fully Covering Headgear (prevents hair selection)
fully_covering_headgear = {
    # Common fully covering headgear
    "Combat Helmet",
    "Gas Mask",
    "Hooded Coat",
    # Ghoul-specific fully covering
    "Wrapped Head Bandages",
    "Radiation Suit Hood",
    "Scrapped Metal Helmet",
    # Super Mutant-specific fully covering
    "Metal Helmet",
    "Spiked Helmet",
    "Heavy Plate Helmet",
    # Synth-specific fully covering
    "Institute Hood",
    "Metallic Plating",
    "Neural Interface Helmet",
    "Courser Hood",
}

beard_options = ["None", "Light Stubble", "Goatee", "Moustache", "Full Beard"]

# Character Attributes
skin_tone_options = {
    Race.HUMAN: [
        "Pale",
        "Light",
        "Tan",
        "Brown",
        "Dark Brown",
        "Ebony",
    ],
    Race.GHOUL: [
        "Pale Grey",
        "Ashen",
        "Mottled",
        "Necrotic",
        "Glowing",
    ],
    Race.SUPER_MUTANT: [
        "Light Green",
        "Green",
        "Dark Green",
        "Olive Green",
    ],
    Race.SYNTH: [
        "Synthetic Fair",
        "Synthetic Dark",
        "Metallic Silver",
        "Exposed Component",
    ],
}

body_type_options = {
    Race.HUMAN: [
        "Slim",  # Lean, narrow frame
        "Muscular",  # Athletic, strong build
        "Stocky",  # Solid, broader build
        "Heavy",  # Larger, heavier build
    ],
    Race.GHOUL: [
        "Skeletal",  # Extremely thin, bony
        "Withered",  # Thin but with some mass
        "Twisted",  # Asymmetrical, deformed
    ],
    Race.SUPER_MUTANT: [
        "Muscular",  # Basic mutant physique
        "Brutish",  # Larger, more intimidating
        "Towering",  # Extremely large and imposing
    ],
    Race.SYNTH: [
        "Slender",  # Lighter, agile frame
        "Muscular",  # Combat-oriented build
        "Armored",  # Heavily reinforced build
    ],
}

expression_emojis = {
    # Neutral
    "Neutral": "😐",
    # Positive Emotions
    "Smiling": "😊",
    "Laughing": "😂",
    "Proud": "😎",
    # Negative Emotions
    "Sad": "😔",
    "Angry": "😠",
    "Frustrated": "😫",
    # Fear & Surprise
    "Shocked": "😲",
    "Terrified": "😱",
    # Confidence & Strength
    "Determined": "💪",
    "Heroic": "🦸",
    "Stoic": "🗿",
    # Suspicion & Doubt
    "Skeptical": "🤔",
    "Suspicious": "🤨",
    # Confusion & Mixed Feelings
    "Confused": "😕",
    "Awkward": "😬",
    # Social & Playful
    "Mischievous": "😈",
    "Flirty": "😉",
}

expression_options = [f"{text} {emoji}" for text, emoji in expression_emojis.items()]
