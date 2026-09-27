import streamlit as st

st.set_page_config(
    page_title="What Can I Cook?",
    page_icon="🍳"
)

st.title("🍳 What Can I Cook?")
st.write("Enter any ingredients you have!")

ingredients = st.text_area(
    "🥕 Your ingredients",
    placeholder="Example: potato, onion, tomato, cheese"
)

if st.button("🔍 Find Recipes"):

    if ingredients.strip():

        items = [
            item.strip().title()
            for item in ingredients.split(",")
            if item.strip()
        ]

        st.success("Here are some ideas for you! 🍽️")

        # Universal suggestions based on whatever the user enters
        st.subheader("🍳 Recipe Ideas")

        st.write("1. 🍲 Mixed Ingredient Curry")
        st.write(
            f"Use {', '.join(items)} with spices and cook together."
        )

        st.write("2. 🥘 Quick Stir-Fry")
        st.write(
            f"Stir-fry {', '.join(items)} with oil, salt and your "
            "favorite spices."
        )

        st.write("3. 🍛 One-Pot Meal")
        st.write(
            f"Combine {', '.join(items)} with a suitable base "
            "such as rice, pasta or noodles."
        )

        st.subheader("👩‍🍳 Basic Cooking Method")

        st.write("""
1. Wash and prepare your ingredients.
2. Heat a pan with a little oil.
3. Add the ingredients that need the longest cooking time first.
4. Add spices and seasoning according to taste.
5. Cook until the ingredients are properly cooked.
6. Serve hot! 🍽️
""")

    else:
        st.warning("Please enter at least one ingredient.")
