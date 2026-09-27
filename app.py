import streamlit as st

st.set_page_config(
    page_title="What Can I Cook?",
    page_icon="🍳"
)

st.title("🍳 What Can I Cook? AI")
st.write("Enter the ingredients you have, and discover recipe ideas!")

ingredients = st.text_input(
    "🥕 Enter your ingredients",
    placeholder="Example: tomato, onion, potato"
)

if st.button("🔍 Find Recipes"):

    if ingredients.strip():
        st.success(
            f"Searching for recipes using: {ingredients}"
        )
    else:
        st.warning("Please enter at least one ingredient.")
