import random

from options import (
    race_descriptions,
    object_options,
    accessory_options,
    pose_options,
    background_options,
    expression_options,
    headgear,
    FULLY_COVERING_HEADGEAR,
    skin_tone_options,
    body_type_options,
    haircuts,
    archetypes,
)
from models import Character

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


def prefill_character(archetype_name: str) -> Character:
    """Returns a validated Character model with default archetype values."""
    archetype_data = archetypes.get(archetype_name, {})

    race = archetype_data.get("race", "Human")
    gender = random.choice(["Male", "Female"])
    skin_tone = random.choice(skin_tone_options[race])
    body_type = random.choice(body_type_options[race])
    faction = archetype_data.get("faction", "None")
    outfit = archetype_data.get("outfit", "Casual Clothes")
    weapon = archetype_data.get("weapon", "None")

    # Select headgear first
    selected_headgear = random.choice(headgear[race])

    # If headgear fully covers hair, set hair to None, otherwise select hair
    selected_hair = (
        None
        if selected_headgear in FULLY_COVERING_HEADGEAR
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

    age = random.randint(18, 80) if race == "Human" else None

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
        age=age,
        expression=random.choice(expression_options),
        weapon=weapon,
        object_held=random.choice(object_options),
        accessory=random.choice(accessory_options),
        pose=random.choice(pose_options),
        background=random.choice(background_options),
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
        f"A {character.gender.lower()} {character.race} {faction_text}, with {character.skin_tone.lower()} skin and a "
        f"{character.body_type.lower()} body, wearing {character.outfit}."
    )

    # Describe hair only if visible
    if character.hair and character.hair not in ["None", "Bald"]:
        prompt += f" Has {character.hair_color.lower()} {character.hair.lower()}."

    # Mention headgear if it's worn
    if character.headgear and character.headgear != "None":
        prompt += f" Wearing {character.headgear.lower()}."

    # Add beard details only if applicable
    if character.beard and character.beard != "None":
        prompt += f" Has a {character.beard.lower()}."

    # Age description
    if character.age:
        prompt += f" Appears to be around {character.age} years old."

    # Add facial expression if it's not neutral
    if character.expression != "Neutral":
        prompt += f" Facial expression is {character.expression.lower()}."

    # Extra details (weapon, accessory, objects)
    details = []
    if character.accessory and character.accessory != "None":
        details.append(character.accessory.lower())
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
