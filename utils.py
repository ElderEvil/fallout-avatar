import random

from models import Character
from options.appearance import (
    skin_tone_options,
    body_type_options,
    headgear,
    fully_covering_headgear,
    haircuts,
    expression_options,
)
from options.factions import Faction
from options.items import common_equipment, faction_equipment
from options.presets import archetypes
from options.races import (
    Race,
    GhoulFeralness,
    SuperMutantMutation,
    SynthType,
    race_descriptions,
    Gender,
)

COLOR_MAP = {
    # Natural Hair Colors
    "black": "#000000",
    "dark brown": "#5A3825",
    "brown": "#A52A2A",
    "light brown": "#C69C6D",
    "auburn": "#722F37",
    "blonde": "#FFD700",
    "dirty blonde": "#C2A26D",
    "platinum blonde": "#E5E4E2",
    "gray": "#808080",
    "white": "#FFFFFF",
    # Dyed Hair Colors
    "red": "#FF0000",
    "blue": "#0000FF",
    "green": "#008000",
    "purple": "#800080",
    "pink": "#FFC0CB",
    "cyan": "#00FFFF",
    "magenta": "#FF00FF",
    "silver": "#C0C0C0",
    "indigo": "#4B0082",
    "violet": "#EE82EE",
}


def closest_color(hex_color):
    """Find the closest named color to a given hex color using simple RGB distance"""
    # Convert hex to RGB
    hex_color = hex_color.lstrip("#")
    rgb = tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))

    # Find the closest match using Euclidean RGB distance
    min_distance = float("inf")
    closest_name = None

    for name, hex_value in COLOR_MAP.items():
        hex_value = hex_value.lstrip("#")
        named_rgb = tuple(int(hex_value[i : i + 2], 16) for i in (0, 2, 4))

        # Euclidean distance in RGB space
        distance = sum((c1 - c2) ** 2 for c1, c2 in zip(rgb, named_rgb))

        if distance < min_distance:
            min_distance = distance
            closest_name = name

    return closest_name


# Function to generate a fully random hair color
def get_random_hair_color(race: Race) -> str:
    """Returns a random hair color, with unnatural shades for Synths."""

    if race == Race.SYNTH:
        # Synths get artificial/neon hair colors
        synth_colors = [
            "#00FFFF",
            "#FF00FF",
            "#00FF00",
            "#FF4500",
            "#FFD700",
        ]  # Cyan, Magenta, Neon Green, Bright Orange, Gold
        return random.choice(synth_colors)
    else:
        # Generate a random natural shade for humans, ghouls, and super mutants
        r = random.randint(50, 160)  # Avoid extreme dark/light
        g = random.randint(40, 120)  # Keep it in a natural range
        b = random.randint(30, 100)
        return f"#{r:02X}{g:02X}{b:02X}"


def prefill_character(archetype_name: str) -> Character:
    """Returns a validated Character model with default archetype values."""
    archetype_data = archetypes.get(archetype_name, {})

    race = archetype_data.get("race", "Human")

    match race:
        case "Human":
            state_of_being = None
            age = random.randint(18, 80)
        case "Ghoul":
            state_of_being = random.choice(
                list(GhoulFeralness)
            )  # Default: Sane, but can be random
            age = None
        case "Super Mutant":
            state_of_being = random.choice(
                list(SuperMutantMutation)
            )  # Default: Mild Mutation
            age = None
        case "Synth":
            state_of_being = random.choice(
                list(SynthType)
            )  # Default: Gen 3 (Human-like)
            age = None
        case _:
            state_of_being = None
            age = None

    if race == Race.SYNTH:
        gender_options = (
            [Gender.OTHER] if state_of_being != SynthType.GEN_3 else list(Gender)
        )
    else:
        gender_options = [Gender.MALE, Gender.FEMALE]

    gender = random.choice(gender_options)
    skin_tone = random.choice(skin_tone_options[race])
    body_type = random.choice(body_type_options[race])
    faction = archetype_data.get("faction", Faction.NONE)

    # Select headgear first
    selected_headgear = random.choice(headgear[race])

    # If headgear fully covers hair, set hair to None, otherwise select hair
    selected_hair = (
        None
        if selected_headgear in fully_covering_headgear
        else random.choice(haircuts[race])
    )

    hair_color = (
        random.choice(["Black", "Brown", "Blonde", "Red", "Silver", "Blue", "Green"])
        if selected_hair
        else None
    )

    beard = (
        random.choice(["None", "Light Stubble", "Full Beard", "Goatee", "Moustache"])
        if gender != "Female" and race != "Synth"
        else None
    )

    expression = random.choice(expression_options)

    available_equipment = {
        category: common_equipment[category]
        + faction_equipment[faction].get(category, [])
        for category in common_equipment.keys()
    }

    weapon = random.choice(available_equipment["weapons"])
    outfit = random.choice(available_equipment["outfits"])
    object_held = random.choice(available_equipment["objects"])
    accessory = random.choice(available_equipment["accessories"])

    pose = archetype_data.get("pose", "None")
    background = archetype_data.get("background", "None")

    return Character(
        race=race,
        gender=gender,
        skin_tone=skin_tone,
        body_type=body_type,
        faction=faction,
        outfit=outfit,
        headgear=selected_headgear,
        hair=selected_hair,
        hair_color=hair_color,
        beard=beard,
        state_of_being=state_of_being,
        age=age,
        expression=expression,
        weapon=weapon,
        object_held=object_held,
        accessory=accessory,
        pose=pose,
        background=background,
    )


def build_prompt(character: Character) -> str:
    """Generates a structured prompt from a validated Character model."""

    # Add race description if available
    prompt = (
        f"**{character.race}:** {race_descriptions.get(character.race, '')}\n\n"
        if character.race in race_descriptions
        else ""
    )

    # Base character description
    faction_text = (
        f"from the {character.faction} faction"
        if character.faction != "None"
        else "with no faction affiliation"
    )
    prompt += (
        f"A {character.gender.lower()} {character.race.lower()} {faction_text}, with {character.skin_tone.lower()} "
        f"skin tone and a {character.body_type.lower()} body, wearing {character.outfit}."
    )

    # Use match-case for "State of Being"
    match character.race:
        case "Ghoul":
            match character.state_of_being:
                case GhoulFeralness.SANE:
                    prompt += (
                        " This ghoul retains their sanity and functions like a human."
                    )
                case GhoulFeralness.PARTIALLY_FERAL:
                    prompt += " This ghoul is partially feral, showing erratic behavior but some awareness."
                case GhoulFeralness.FULLY_FERAL:
                    prompt += " This ghoul is fully feral, driven by instinct and aggressive towards non-ghouls."

        case "Super Mutant":
            match character.state_of_being:
                case SuperMutantMutation.MILD:
                    prompt += " This super mutant has a mild mutation, retaining some intelligence and reasoning."
                case SuperMutantMutation.SEVERE:
                    prompt += " This super mutant has undergone severe mutation, becoming larger and more aggressive."
                case SuperMutantMutation.BEHEMOTH:
                    prompt += " This super mutant has reached behemoth-level mutation, towering over most beings with near-limitless strength."

        case "Synth":
            match character.state_of_being:
                case SynthType.GEN_3:
                    prompt += " This synth is Gen 3, indistinguishable from a human with fully organic-like features."
                case SynthType.GEN_2:
                    prompt += " This synth is Gen 2, blending synthetic and cybernetic enhancements with visible mechanical parts."
                case SynthType.GEN_1:
                    prompt += " This synth is Gen 1, appearing fully robotic with exposed servos and metallic plating."

    # Describe hair only if visible
    if character.hair and character.hair not in ["None", "Bald"]:
        prompt += f" Has {character.hair_color.lower()} {character.hair.lower()}."

    # Mention headgear if it's worn
    if character.headgear and character.headgear != "None":
        prompt += f" Wearing {character.headgear}."

    # Add beard details only if applicable
    if character.beard and character.beard != "None":
        prompt += f" Has a {character.beard.lower()}."

    # Age description for humans
    if character.age and character.race == Race.HUMAN:
        prompt += f" Appears to be around {character.age} years old."

    # Add facial expression if it's not neutral
    if character.expression != "Neutral":
        prompt += f" Facial expression is {character.expression.lower()}."

    # Extra details (weapon, accessory, objects)
    details = []
    if character.accessory and character.accessory != "None":
        details.append(character.accessory)
    if character.weapon and character.weapon != "None":
        details.append(f"holding a {character.weapon}")
    if character.object_held and character.object_held != "None":
        details.append(f"carrying a {character.object_held}")

    if details:
        prompt += " " + ", ".join(details) + "."

    # Pose and background details
    prompt += f" Posed {character.pose.lower()}."
    if character.background != "None":
        prompt += f" The scene is set in a {character.background.lower()}, with atmospheric lighting enhancing the depth."

    # Art direction and style
    prompt += (
        " The image should feature a detailed, immersive composition with a Fallout-inspired retro-futuristic, post-apocalyptic aesthetic. "
        "It should include bold outlines, vibrant yet worn-out colors, and atmospheric lighting. The setting should convey environmental storytelling, "
        "capturing the world’s desolation while maintaining Vault-Tec’s signature cartoon realism."
    )

    return prompt
