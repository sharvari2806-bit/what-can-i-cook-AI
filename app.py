import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="What Can I Cook?",
    page_icon="🍳",
    layout="centered"
)

st.title("🍳 What Can I Cook?")
st.write("Find recipes using the ingredients you already have.")

# -----------------------------
# LOAD RECIPES
# -----------------------------

@st.cache_data
def load_recipes():
    return pd.read_csv("recipes.csv")

df = load_recipes()

# -----------------------------
# ADD YOUR OWN RECIPE
# -----------------------------

st.header("➕ Add Your Own Recipe")

with st.expander("Add a new recipe"):

    recipe_name = st.text_input(
        "🍴 Recipe name",
        placeholder="Example: Cheese Maggi"
    )

    recipe_ingredients = st.text_input(
        "🥕 Ingredients",
        placeholder="Example: noodles, cheese, onion"
    )

    recipe_time = st.text_input(
        "⏱️ Cooking time",
        placeholder="Example: 15 minutes"
    )

    recipe_difficulty = st.selectbox(
        "👩‍🍳 Difficulty",
        ["Easy", "Medium", "Hard"]
    )

    recipe_steps = st.text_area(
        "📖 How to make it",
        placeholder="Write the cooking steps here..."
    )

    if st.button("➕ Add Recipe"):

        if (
            recipe_name.strip()
            and recipe_ingredients.strip()
            and recipe_steps.strip()
        ):

            new_recipe = pd.DataFrame([{
                "recipe": recipe_name,
                "ingredients": recipe_ingredients,
                "time": recipe_time,
                "difficulty": recipe_difficulty,
                "steps": recipe_steps
            }])

            df = pd.concat(
                [df, new_recipe],
                ignore_index=True
            )

            st.session_state["recipes"] = df

            st.success(
                f"✅ {recipe_name} added successfully!"
            )

        else:
            st.warning(
                "Please fill in the recipe name, ingredients and steps."
            )

# Use newly added recipes during this session
if "recipes" in st.session_state:
    df = st.session_state["recipes"]

st.divider()

# -----------------------------
# FIND RECIPES
# -----------------------------

st.header("🔎 Find a Recipe")

ingredients = st.text_area(
    "🥕 What ingredients do you have?",
    placeholder="Example: potato, onion, tomato, cheese",
    height=100
)

if st.button("🔍 Find Recipes"):

    if not ingredients.strip():
        st.warning("Please enter at least one ingredient.")
        st.stop()

    user_ingredients = set(
        item.strip().lower()
        for item in ingredients.split(",")
        if item.strip()
    )

    recommendations = []

    for _, recipe in df.iterrows():

        recipe_ingredients = set(
            item.strip().lower()
            for item in recipe["ingredients"].split(",")
        )

        matching = user_ingredients.intersection(
            recipe_ingredients
        )

        if matching:

            score = (
                len(matching)
                / len(recipe_ingredients)
            ) * 100

            recommendations.append({
                "recipe": recipe["recipe"],
                "ingredients": recipe["ingredients"],
                "time": recipe["time"],
                "difficulty": recipe["difficulty"],
                "steps": recipe["steps"],
                "matching": matching,
                "score": score
            })

    recommendations.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    if not recommendations:

        st.error("😕 No matching recipes found.")

        st.info(
            "Try adding different ingredients or add your own recipe above."
        )

        st.stop()

    st.success(
        f"🍽️ Found {len(recommendations)} matching recipes!"
    )

    # -----------------------------
    # DISPLAY TOP 3
    # -----------------------------

    for recipe in recommendations[:3]:

        st.subheader(
            "🍴 " + recipe["recipe"]
        )

        st.progress(
            min(int(recipe["score"]), 100)
        )

        st.write(
            f"🎯 **Ingredient match: "
            f"{recipe['score']:.0f}%**"
        )

        st.write(
            "✅ **You have:** "
            + ", ".join(recipe["matching"])
        )

        st.write(
            "🥕 **Ingredients:** "
            + recipe["ingredients"]
        )

        st.write(
            "⏱️ **Cooking time:** "
            + str(recipe["time"])
        )

        st.write(
            "👩‍🍳 **Difficulty:** "
            + str(recipe["difficulty"])
        )

        with st.expander("📖 How to make it"):
            st.write(recipe["steps"])

        st.divider()

# -----------------------------
# FOOTER
# -----------------------------

st.caption(
    "🤖 What Can I Cook? | FY B.Sc. AI & DS Project"
)
