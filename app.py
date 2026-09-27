import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="What Can I Cook?",
    page_icon="🍳"
)

st.title("🍳 What Can I Cook?")
st.write("Enter the ingredients you have and get recipe recommendations.")

# Load recipes
df = pd.read_csv("recipes.csv")

# User input
ingredients = st.text_area(
    "🥕 Enter your ingredients",
    placeholder="Example: potato, onion, tomato, cheese",
    height=120
)

if st.button("🔍 Find Recipes"):

    if not ingredients.strip():
        st.warning("Please enter at least one ingredient.")
        st.stop()

    # Convert user ingredients into words
    user_ingredients = [
        x.strip().lower()
        for x in ingredients.split(",")
        if x.strip()
    ]

    results = []

    # Check every recipe
    for _, recipe in df.iterrows():

        recipe_ingredients = [
            x.strip().lower()
            for x in recipe["ingredients"].split(",")
        ]

        matches = set(user_ingredients) & set(recipe_ingredients)

        if len(matches) > 0:
            results.append(
                (
                    len(matches),
                    recipe
                )
            )

    # Sort by number of matching ingredients
    results.sort(
        key=lambda x: x[0],
        reverse=True
    )

    if not results:
        st.warning(
            "😕 No matching recipe found in our current recipe dataset."
        )
        st.info(
            "Try entering ingredients such as potato, onion, tomato, "
            "paneer, pasta, rice, egg or mango."
        )
        st.stop()

    st.success("🍽️ Recipes found!")

    # Show maximum 3 recipes
    for match_count, recipe in results[:3]:

        st.subheader("🍴 " + recipe["recipe"])

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

        st.write(
            "📖 **How to make:** "
            + recipe["steps"]
        )

        st.write(
            "✅ **Your matching ingredients:** "
            + ", ".join(
                set(user_ingredients)
                & set(
                    x.strip().lower()
                    for x in recipe["ingredients"].split(",")
                )
            )
        )

        st.divider()

st.caption(
    "🤖 Recipe Recommendation App | FY B.Sc. AI & DS Project"
)
