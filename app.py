import streamlit as st
from openai import OpenAI

# -----------------------------
# PAGE SETTINGS
# -----------------------------
st.set_page_config(
    page_title="What Can I Cook?",
    page_icon="🍳",
    layout="centered"
)

# -----------------------------
# TITLE
# -----------------------------
st.title("🍳 What Can I Cook? AI")
st.write(
    "Enter any ingredients you have and AI will suggest recipes."
)

# -----------------------------
# INGREDIENT INPUT
# -----------------------------
ingredients = st.text_area(
    "🥕 Your ingredients",
    placeholder="Example: potato, tomato, onion, garlic, rice",
    height=120
)

# -----------------------------
# OPTIONAL PREFERENCE
# -----------------------------
preference = st.text_input(
    "✨ Preference (optional)",
    placeholder="Example: Indian, vegetarian, spicy, quick"
)

# -----------------------------
# BUTTON
# -----------------------------
if st.button("🔍 Find Recipes"):

    if not ingredients.strip():
        st.warning("Please enter at least one ingredient.")
        st.stop()

    # Get API key from Streamlit Secrets
    api_key = st.secrets.get("OPENAI_API_KEY")

    if not api_key:
        st.error(
            "OPENAI_API_KEY is missing. Add it in Streamlit Secrets."
        )
        st.stop()

    client = OpenAI(api_key=api_key)

    # -----------------------------
    # AI PROMPT
    # -----------------------------
    prompt = f"""
You are an expert worldwide recipe assistant.

The user has these ingredients:

{ingredients}

The user's optional preference is:

{preference if preference.strip() else "No preference"}

Your job is to suggest 3 recipes that the user can make.

There is NO fixed ingredient list.
The user may enter ingredients from ANY cuisine or country.

For each recipe, provide:

### Recipe Name

**Ingredients I already have:**
- List only ingredients supplied by the user.

**Additional ingredients:**
- List optional ingredients that would improve the recipe.

**Cooking Time:**
- Give an approximate time.

**Difficulty:**
- Easy, Medium, or Hard.

**Steps:**
1. Give simple step-by-step cooking instructions.
2. Keep the instructions beginner-friendly.

Important:
- Use the user's ingredients as the main basis.
- Do not pretend the user has an ingredient they did not enter.
- If the combination is unusual, create a sensible recipe using compatible ingredients.
- Recipes can come from any cuisine in the world.
- Do not restrict the user to a predefined ingredient database.
"""

    # -----------------------------
    # CALL AI
    # -----------------------------
    try:

        with st.spinner("🤖 Creating recipes..."):

            response = client.responses.create(
                model="gpt-5.6-luna",
                input=prompt
            )

        # -----------------------------
        # DISPLAY RESULT
        # -----------------------------
        st.success("🍽️ Your recipes are ready!")

        st.markdown(response.output_text)

    except Exception as e:

        st.error("Something went wrong while generating recipes.")

        st.code(str(e))
