import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="What Can I Cook?",
    page_icon="🍳",
    layout="centered"
)

st.title("🍳 What Can I Cook?")
st.write("Find recipes using the ingredients you already have.")

# -----------------------------
# LOAD ORIGINAL RECIPES
# -----------------------------

@st.cache_data
def load_original_recipes():
    return pd.read_csv("recipes.csv")

df = load_original_recipes()

# -----------------------------
# LOAD USER RECIPES
# -----------------------------

if os.path.exists("user_recipes.csv"):

    user_df = pd.read_csv("user_recipes.csv")

    if not user_df.empty:
        df = pd.concat(
            [df, user_df],
            ignore_index=True
        )

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
        placeholder="Example: 10 minutes"
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
                "recipe": recipe_name.strip(),
                "ingredients": recipe_ingredients.strip(),
                "time": recipe_time.strip(),
                "difficulty": recipe_difficulty,
                "steps": recipe_steps.strip()
            }])

            # Save recipe permanently
            new_recipe.to_csv(
                "user_recipes.csv",
                mode="a",
                header=False,
                index=False
            )

            st.success(
                f"✅ {recipe_name} saved successfully!"
            )

            st.cache_data.clear()

        else:
            st.warning(
                "Please fill in the recipe name, ingredients and steps."
            )

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

    # Reload all recipes
    df = load_original_recipes()

    if os.path.exists("user_recipes.csv"):

        user_df = pd.read_csv("user_recipes.csv")

        if not user_df.empty:
            df = pd.concat(
                [df, user_df],
                ignore_index=True
            )

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
            "Try different ingredients or add your own recipe."
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

st.caption(
    "🤖 What Can I Cook? | FY B.Sc. AI & DS Project"
)
