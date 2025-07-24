import requests
import streamlit as st
from openai import OpenAI

from auth import authenticate_user
from config import settings
from minio_service import get_minio_client
from models import Character
from options.appearance import (
    skin_tone_options,
    body_type_options,
    fully_covering_headgear,
    haircuts,
    expression_options,
    headgear,
    beard_options,
)
from options.factions import Faction, faction_restrictions
from options.items import common_equipment, faction_equipment
from options.presets import archetypes
from options.races import Gender, Race, SynthType, GhoulFeralness, SuperMutantMutation
from options.scenes import pose_options, background_options
from utils import (
    build_prompt,
    closest_color,
    prefill_character,
    get_random_hair_color,
    generate_filenames,
)

authenticate_user()

client = OpenAI(api_key=settings.OPENAI_API_KEY)


@st.cache_resource
def get_cached_minio_client():
    return get_minio_client()


# Main Title
st.title("☢️ Fallout Avatar Generator")

if "hair_color_hex" not in st.session_state:
    st.session_state.hair_color_hex = None

if "refined_prompt" not in st.session_state:
    st.session_state.refined_prompt = None

# Archetype Selection
archetype = st.selectbox("Select a Preset Archetype", ["Custom"] + list(archetypes))

if archetype != "Custom":
    if st.session_state.get("selected_archetype") != archetype:
        st.session_state.selected_archetype = archetype
        character = prefill_character(archetype)

        # Populate session state with archetype defaults
        for field in character.model_fields:
            st.session_state[field] = getattr(character, field)

        st.session_state["hair_color_hex"] = get_random_hair_color(
            st.session_state["race"]
        )

else:
    st.session_state.selected_archetype = None
    st.session_state.setdefault("hair_color_hex", None)


with st.expander("🧬 Character Details", expanded=True):
    st.subheader("Basic Traits")
    col1, col2 = st.columns(2)

    with col1:
        # **Race Selection**
        race = st.selectbox(
            "Race",
            list(Race),
            key="race",
            help="Select your character's race. This determines available factions, attributes, and mutations.",
        )

        gender_options_map = {
            Race.SYNTH: [Gender.OTHER]
            if st.session_state.get("state_of_being") != SynthType.GEN_3
            else list(Gender),
            Race.HUMAN: [Gender.MALE, Gender.FEMALE],
        }
        gender_options = gender_options_map.get(race, [Gender.MALE, Gender.FEMALE])

        gender = st.radio(
            "Gender",
            gender_options,
            horizontal=True,
            key="gender",
            help="Choose gender.\n"
            "- **Humans & Gen 3 Synths:** Can be Male, Female, or Other.\n"
            "- **Gen 2 & Gen 1 Synths:** Must be 'Other' due to synthetic construction.",
        )

    with col2:
        # **Skin Tone & Body Type**
        skin_tone = st.selectbox(
            "Skin Tone",
            skin_tone_options[race],
            key="skin_tone",
            help="Choose a skin tone based on race.\n"
            "- **Humans**: Natural skin tones.\n"
            "- **Ghouls**: Necrotic and mottled skin.\n"
            "- **Super Mutants**: Mutated greenish hues.\n"
            "- **Synths**: May have synthetic or metallic skin.",
        )

        body_type = st.selectbox(
            "Body Type",
            body_type_options[race],
            key="body_type",
            help="Chose a body type that fits your character's race and role.\n"
            "- **Humans & Synths**: Vary from slim to muscular.\n"
            "- **Super Mutants**: Heavily built, ranging from strong to behemoth-sized.",
        )

    # **State of Being / Age Handling**
    if race == Race.HUMAN:
        age = st.slider(
            "Age",
            min_value=18,
            max_value=80,
            value=30,
            key="age",
            help="Set your character's age (18-80).\n"
            "- **Only humans have an adjustable age.**\n"
            "- Ghouls may be over 200 years old but do not track age.",
        )
        state_of_being = None  # Humans don’t have this attribute
    else:
        state_of_being_options = {
            Race.GHOUL: list(GhoulFeralness),
            Race.SUPER_MUTANT: list(SuperMutantMutation),
            Race.SYNTH: list(SynthType),
        }

        state_of_being = st.selectbox(
            "State of Being",
            state_of_being_options[race],
            key="state_of_being",
            help="Defines the biological or synthetic condition of your character.\n"
            "- **Ghouls**: May range from sane to fully feral.\n"
            "- **Super Mutants**: Vary in mutation severity.\n"
            "- **Synths**: Can appear human-like or fully robotic.",
        )

        age = None  # Non-humans don't have age

# Appearance & Facial Features
with st.expander("💇‍♂️ Appearance & Facial Features", expanded=False):
    st.subheader("Hair, Headgear & Face")
    col1, col2 = st.columns(2)

    with col1:
        # Headgear Selection
        headgear = st.selectbox(
            "Headgear",
            headgear.get(race, ["None"]),
            key="headgear",
            help="Choose a **hat, helmet, or head accessory**. Some helmets fully cover the head, hiding hair.",
        )

        # Hair & Hair Color Logic
        hair = None
        hair_color = None
        if headgear not in fully_covering_headgear:
            hair = st.selectbox(
                "Hair",
                haircuts.get(race, ["None"]),
                key="hair",
                help="Select a hairstyle. **Only available for non-fully covered headgear.**",
            )

            hair_color_hex = st.color_picker(
                "Hair Color",
                key="hair_color",
                help="Pick a **hair color**. **Humans have natural shades, while Synths may have neon or artificial tones.**",
            )
            if not hair_color_hex.startswith("#"):
                hair_color = hair_color_hex
            else:
                hair_color = closest_color(hair_color_hex)
            st.write(f"Selected hair color name: {hair_color.title()}")

    with col2:
        # Facial Expression Selection
        expression = st.selectbox(
            "Facial Expression",
            expression_options,
            key="expression",
            help="Choose your character's **facial expression**, from neutral to intense emotions.",
        )

        # Beard Selection (Only for specific cases)
        beard = "None"
        if race == Race.HUMAN and gender in [Gender.MALE, Gender.OTHER]:
            beard = st.selectbox(
                "Beard",
                beard_options,
                key="beard",
                help="Choose a **beard style**. **Only available for male human characters.**",
            )

with st.expander("👕 Faction, Outfit & Equipment", expanded=False):
    st.subheader("Faction & Affiliation")

    # Get valid factions for the race
    valid_factions = faction_restrictions.get(race, [Faction.NONE])
    faction = st.selectbox(
        "Faction",
        valid_factions,
        key="faction",
        help="Select a faction. It affects which equipment and items are available to your character.",
    )

    # Get available equipment for the selected faction
    available_equipment = {
        category: common_equipment[category]
        + faction_equipment[faction].get(category, [])
        for category in common_equipment.keys()
    }

    # Create equipment selection columns
    col1, col2 = st.columns(2)

    with col1:
        weapon = st.selectbox(
            "Weapon",
            available_equipment["weapons"],
            key="weapon",
            help="Choose a weapon for your character. Available options depend on selected faction.",
        )
        accessory = st.selectbox(
            "Accessory",
            available_equipment["accessories"],
            key="accessory",
            help="Select character accessories like badges, modifications or decorations.",
        )
    with col2:
        outfit = st.selectbox(
            "Outfit",
            available_equipment["outfits"],
            key="outfit",
            help="Pick character's clothing or armor. Available options depend on selected faction.",
        )
        object_held = st.selectbox(
            "Object",
            available_equipment["objects"],
            key="object_held",
            help="Choose an item your character is holding or interacting with.",
        )

# Scene & Action
with st.expander("🎭 Scene & Action", expanded=False):
    st.subheader("Pose & Background")
    col1, col2 = st.columns(2)
    with col1:
        pose = st.selectbox(
            "Pose",
            pose_options,
            key="pose",
            help="Select character's stance and action in the scene.",
        )
    with col2:
        background = st.selectbox(
            "Background",
            background_options,
            key="background",
            help="Choose the environment or location for your character.",
        )

# Final Character Object
character = Character(
    race=race,
    gender=gender,
    skin_tone=skin_tone,
    body_type=body_type,
    age=age,
    state_of_being=state_of_being,
    faction=faction,
    outfit=outfit,
    headgear=headgear,
    hair=hair,
    hair_color=hair_color,
    beard=beard,
    expression=expression,
    weapon=weapon,
    object_held=object_held,
    accessory=accessory,
    pose=pose,
    background=background,
)

st.session_state.character = character

# Generate Initial Prompt
st.markdown("### 📝 Generated Prompt")
initial_prompt = build_prompt(character)

# Display Initial & Refined Prompt in Two Columns
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🔹 Initial Prompt")
    st.text_area("Initial Prompt", initial_prompt, height=250, key="initial_prompt")
    refined_prompt = None

if "auth_token" not in st.session_state:
    st.warning("Please log in to access this content.")
    st.stop()

# Improve Prompt with GPT
if st.button("✨ Improve Prompt with AI"):
    with st.spinner("Refining prompt..."):
        refined_prompt = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a creative AI assistant improving a character description for an AI image generator. "
                        "Make the prompt more expressive and true to Fallout series lore while shortening it. "
                        "Keep all key details but remove redundancy and excessive wording."
                    )
                },
                {
                    "role": "user",
                    "content": f"Improve this prompt while keeping all details and making it more vivid and true to Fallout series lore:\n\n{initial_prompt}",
                },
            ],
            temperature=0.7,
        )
        st.session_state.refined_prompt = refined_prompt.choices[0].message.content


with col2:
    if "refined_prompt" in st.session_state:
        st.markdown("#### ✨ Refined Prompt")
        refined_prompt = st.text_area(
            "Refined Prompt",
            st.session_state.refined_prompt,
            height=250,
            key="refined_prompt",
            disabled=True,
        )

# Generate Image with Refined Prompt
if "refined_prompt" not in st.session_state or not st.session_state.refined_prompt:
    st.warning("Please refine the prompt before generating an image.")
    st.stop()

st.markdown("### 🎨 Generate Avatar")
if st.button("🎭 Generate Avatar with AI"):
    with st.spinner("Generating avatar..."):
        response = client.images.generate(
            model="dall-e-3",
            prompt=refined_prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        # Download generated image
        image_url = response.data[0].url
        image_data = requests.get(image_url).content

        # Construct the filename
        image_filename, prompt_filename = generate_filenames(character)

        minio_client = get_cached_minio_client()
        bucket_name = "fastapi-minio"

        # Upload to MinIO
        try:
            minio_url = minio_client.upload_file(
                file_data=image_data, file_name=image_filename, bucket_name=bucket_name
            )
            minio_prompt_url = minio_client.upload_file(
                file_data=refined_prompt.encode(),
                file_name=prompt_filename,
                bucket_name=bucket_name,
            )

            # Display stored image
            st.image(
                image_url,
                caption="Generated Avatar (Stored in MinIO)",
                use_container_width=True,
            )

        except Exception as e:
            st.error(f"Failed to upload to MinIO: {e}")
