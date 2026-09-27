import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# -----------------------------
# PAGE SETTINGS
# -----------------------------

st.set_page_config(
    page_title="What Can I Cook?",
    page_icon="🍳",
    layout="centered"
)

# -----------------------------
# LOAD DATASET
# -----------------------------

@st.cache_data
def load_data():
    return pd.read_csv("recipes.csv")

df = load_data()

# -----------------------------
# TITLE
# -----------------------------

st.title("🍳 What Can I Cook?")

st.write(
    "Enter the ingredients you have and get recipe recommendations."
)

# -----------------------------
# USER INPUT
# -----------------------------

ingredients = st.text_area(
    "🥕 Enter your ingredients",
    placeholder="Example: potato, onion, tomato, garlic",
    height=120
)

# -----------------------------
# RECOMMEND RECIPES
# -----------------------------

if st.button("🔍 Find Recipes"):

    if not ingredients.strip():
        st.warning("Please enter at least one ingredient.")
        st.stop()

    # Convert ingredients to lowercase
    user_ingredients = ingredients.lower()

    # Create TF-IDF model
    vectorizer = TfidfVectorizer()

    recipe_vectors = vectorizer.fit_transform(
        df["ingredients"]
    )

    user_vector = vectorizer.transform(
        [user_ingredients]
    )

    # Calculate similarity
    similarity = cosine_similarity(
        user_vector,
        recipe_vectors
    )[0]

    # Add similarity score
    df_result = df.copy()

    df_result["similarity"] = similarity

    # Get top 3 different recipes
    recommendations = (
        df_result
        .sort_values(
            by="similarity",
            ascending=False
        )
        .head(3)
    )

    # -----------------------------
    # DISPLAY RESULTS
    # -----------------------------

    st.success("🍽️ Recipes found!")

    for _, recipe in recommendations.iterrows():

        st.subheader(
            "🍴 " + recipe["recipe"]
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

        st.write(
            "📖 **How to make:** "
            + recipe["steps"]
        )

        st.divider()

# -----------------------------
# FOOTER
# -----------------------------

st.caption(
    "🤖 AI Recipe Recommender | FY B.Sc. AI & DS Project"
)
