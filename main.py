import os
import uuid

import requests
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

from config import (
    archetypes,
    expression_options,
    weapon_options,
    headgear,
    haircuts,
    skin_tone_options,
    body_type_options,
    faction_options,
    outfit_options,
    object_options,
    accessory_options,
    pose_options,
    background_options,
    FULLY_COVERING_HEADGEAR,
    races,
    settings,
)
from minio_service import get_minio_client
from models import Character
from utils import closest_color, build_prompt, prefill_character

OPENAI_API_KEY = settings.OPENAI_API_KEY

# Ensure API key is set
if not OPENAI_API_KEY:
    st.error("Missing OpenAI API key. Please set OPENAI_API_KEY in a .env file.")
    st.stop()

client = OpenAI(api_key=OPENAI_API_KEY)
minio_client = get_minio_client()
bucket_name = "fastapi-minio"  # Ensure this matches the MinIO config

# 🎨 **Main Title**
st.title("☢️ Fallout Avatar Generator")

# 🧬 **Character Customization**
st.markdown("## 🎨 Customize Your Character")

# **Archetype Selection**
archetype = st.selectbox(
    "Select a Preset Archetype", ["Custom"] + list(archetypes.keys())
)

if archetype != "Custom":
    if st.session_state.get("selected_archetype") != archetype:
        st.session_state.selected_archetype = archetype
        character = prefill_character(archetype)

        # Populate session state
        st.session_state.race = character.race
        st.session_state.gender = character.gender
        st.session_state.skin_tone = character.skin_tone
        st.session_state.body_type = character.body_type
        st.session_state.faction = character.faction
        st.session_state.outfit = character.outfit
        st.session_state.weapon = character.weapon
        st.session_state.headgear = character.headgear
        st.session_state.hair = character.hair or "None"
        st.session_state.hair_color = character.hair_color or "None"
        st.session_state.beard = character.beard or "None"
        st.session_state.age = character.age if character.age else 30  # Default age
else:
    st.session_state.selected_archetype = None

# **Character Details**
with st.expander("🧬 Character Details", expanded=True):
    st.subheader("Basic Traits")
    col1, col2 = st.columns(2)
    with col1:
        race = st.selectbox(
            "Race", races, key="race", help="Choose a race for your character."
        )
        gender = st.radio(
            "Gender",
            ["Male", "Female", "Other"],
            horizontal=True,
            key="gender",
            help="Select gender identity.",
        )
    with col2:
        skin_tone = st.selectbox(
            "Skin Tone",
            skin_tone_options[race],
            key="skin_tone",
            help="Choose a skin tone.",
        )
        body_type = st.selectbox(
            "Body Type",
            body_type_options[race],
            key="body_type",
            help="Choose a body type.",
        )

    if race == "Human":
        age = st.slider(
            "Age",
            min_value=18,
            max_value=80,
            value=30,
            key="age",
            help="Adjust the character's age.",
        )
    else:
        age = None

# 💇‍♂️ **Appearance & Facial Features**
with st.expander("💇‍♂️ Appearance & Facial Features", expanded=False):
    st.subheader("Hair, Headgear & Face")
    col1, col2 = st.columns(2)
    with col1:
        headgear = st.selectbox(
            "Headgear",
            headgear[race],
            key="headgear",
            help="Choose a hat, helmet, or head accessory.",
        )
        if headgear in FULLY_COVERING_HEADGEAR:
            hair = "None"
            hair_color = "None"
        else:
            hair = st.selectbox(
                "Hair", haircuts[race], key="hair", help="Select a hairstyle."
            )
            hair_color_hex = st.color_picker(
                "Hair Color", "#5A3825", help="Choose a hair color."
            )
            hair_color = closest_color(hair_color_hex)
    with col2:
        expression = st.selectbox(
            "Facial Expression",
            expression_options,
            key="expression",
            help="Choose the character's expression.",
        )
        if race == "Human" and gender in ["Male", "Other"]:
            beard = st.selectbox(
                "Beard",
                ["None", "Light Stubble", "Goatee", "Moustache", "Full Beard"],
                key="beard",
                help="Choose a beard style.",
            )
        else:
            beard = "None"

# 👕 **Faction, Outfit, and Equipment**
with st.expander("👕 Faction, Outfit & Equipment", expanded=False):
    st.subheader("Dress & Gear")
    col1, col2 = st.columns(2)
    with col1:
        faction = st.selectbox(
            "Faction",
            faction_options,
            key="faction",
            help="Select the character's faction.",
        )
    with col2:
        outfit = st.selectbox(
            "Outfit", outfit_options, key="outfit", help="Choose an outfit."
        )

    col1, col2 = st.columns(2)
    with col1:
        weapon = st.selectbox(
            "Weapon",
            weapon_options,
            key="weapon",
            help="Select a weapon for the character.",
        )
    with col2:
        object_held = st.selectbox(
            "Object", object_options, key="object_held", help="Choose an item to hold."
        )

    accessory = st.selectbox(
        "Accessory",
        accessory_options,
        key="accessory",
        help="Choose an additional accessory.",
    )

# 🎭 **Scene & Action**
with st.expander("🎭 Scene & Action", expanded=False):
    st.subheader("Pose & Background")
    col1, col2 = st.columns(2)
    with col1:
        pose = st.selectbox(
            "Pose", pose_options, key="pose", help="Choose a pose for your character."
        )
    with col2:
        background = st.selectbox(
            "Background",
            background_options,
            key="background",
            help="Select a background for the scene.",
        )

# ✅ **Final Character Object**
character = Character(
    race=race,
    gender=gender,
    skin_tone=skin_tone,
    body_type=body_type,
    age=age,
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
st.json(character.model_dump(), expanded=False)

# 📝 **Generate Initial Prompt**
st.markdown("### 📝 Generated Prompt")
initial_prompt = build_prompt(character)

# 🧠 **Improve Prompt with GPT**
if st.button("✨ Improve Prompt with AI"):
    with st.spinner("Refining prompt..."):
        refined_prompt = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a creative AI assistant improving a character description for an AI image generator.",
                },
                {
                    "role": "user",
                    "content": f"Improve this prompt while keeping all details and making it more vivid and true to Fallout series lore:\n\n{initial_prompt}",
                },
            ],
            temperature=0.7,
        )
        st.session_state.refined_prompt = refined_prompt.choices[0].message.content

# 📝 **Display Initial & Refined Prompt in Two Columns**
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🔹 Initial Prompt")
    st.text_area("Initial Prompt", initial_prompt, height=250, key="initial_prompt")

with col2:
    if "refined_prompt" in st.session_state:
        st.markdown("#### ✨ Refined Prompt")
        refined_prompt = st.text_area("Refined Prompt", st.session_state.refined_prompt, height=250, key="refined_prompt", disabled=True)


# 🚀 **Generate Image with Refined Prompt**
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
        generated_filename = f"avatar_{character.race}_{character.gender}_{uuid.uuid4()}"
        image_filename = generated_filename + ".png"
        prompt_filename = generated_filename + "_prompt.txt"

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
            st.image(image_url, caption="Generated Avatar (Stored in MinIO)", use_container_width=True)

        except Exception as e:
            st.error(f"Failed to upload to MinIO: {e}")