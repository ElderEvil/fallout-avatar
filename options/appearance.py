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


expression_options = {
    "Neutral 😐": "with a calm, neutral expression, showing no strong emotions",
    "Smiling 😊": "with a warm, friendly smile, radiating positivity",
    "Laughing 😂": "laughing heartily, eyes squinting with joy",
    "Proud 😎": "standing confidently, exuding self-assurance and pride",
    "Sad 😔": "with a melancholic expression, eyes slightly downcast",
    "Angry 😠": "with a furious glare, jaw clenched in anger",
    "Frustrated 😫": "visibly frustrated, brows furrowed and lips pressed tightly",
    "Shocked 😲": "with wide eyes and an open mouth, frozen in shock",
    "Terrified 😱": "trembling, eyes wide with fear and panic",
    "Determined 💪": "with a firm, resolute look, ready to face any challenge",
    "Heroic 🦸": "standing tall, gaze sharp, radiating bravery and heroism",
    "Stoic 🗿": "with a stone-cold, unreadable expression, unmoved by surroundings",
    "Skeptical 🤔": "raising an eyebrow, lips pressed in skepticism",
    "Suspicious 🤨": "narrowing eyes slightly, expression filled with doubt",
    "Confused 😕": "with a puzzled look, eyebrows raised in uncertainty",
    "Awkward 😬": "with a forced, uneasy smile, avoiding eye contact",
    "Mischievous 😈": "grinning slyly, eyes gleaming with playful intent",
    "Flirty 😉": "with a coy smile, eyes glimmering with playful charm",
}
