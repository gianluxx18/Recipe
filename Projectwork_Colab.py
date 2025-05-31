import os
import requests
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ——— Configuration ———
API_KEY = os.getenv("API_KEY")
API_BASE_URL = "https://api.spoonacular.com"

st.set_page_config(page_title="Recipe Finder", page_icon="🍽️")
st.title("Recipe Finder")
st.write("Discover delicious recipes based on the ingredients you have on hand!")

# ——— Session State Initialization ———
for key in ["recipes_data", "favorites", "selected_fav"]:
    if key not in st.session_state:
        st.session_state[key] = [] if key != "selected_fav" else None

# ——— Input Widgets ———
people_count = st.number_input(
    "Number of people",
    min_value=1,
    max_value=100,
    value=1,
    step=1,
    key="people_count",
)
ingredients = st.text_input(
    "Ingredients (comma-separated)",
    key="ingredients",
    placeholder="e.g. flour, eggs, milk",
)

# ——— Fetch Functions ———
def fetch_recipes(ingredients_str: str):
    params = {"apiKey": API_KEY, "ingredients": ingredients_str}
    resp = requests.get(f"{API_BASE_URL}/recipes/findByIngredients", params=params)
    resp.raise_for_status()
    return resp.json()

def fetch_nutrition(recipe_id: int) -> dict:
    resp = requests.get(
        f"{API_BASE_URL}/recipes/{recipe_id}/nutritionWidget.json",
        params={"apiKey": API_KEY}
    )
    resp.raise_for_status()
    return resp.json()

# ——— Button: Search Recipes ———
if st.button("Search Recipes"):
    ingr = ingredients.strip()
    if not ingr:
        st.warning("❗ Please enter at least one ingredient.")
    else:
        try:
            st.session_state.recipes_data = fetch_recipes(ingr)
        except requests.HTTPError as e:
            st.error(f"API Error: {e}")
            st.session_state.recipes_data = []

# ——— Button: Show Favorites List ———
st.subheader("Favorites")
if not st.session_state.favorites:
    st.info("⭐ No favorites yet.")
else:
    for fav in st.session_state.favorites:
        col1, col2 = st.columns([3, 1])
        with col1:
            if st.button(f"📄 {fav['title']}", key=f"show_{fav['id']}"):
                st.session_state.selected_fav = fav
        with col2:
            if st.button("❌ Remove", key=f"remove_{fav['id']}"):
                st.session_state.favorites = [
                    f for f in st.session_state.favorites if f["id"] != fav["id"]
                ]
                if st.session_state.selected_fav and st.session_state.selected_fav["id"] == fav["id"]:
                    st.session_state.selected_fav = None

# ——— Helper: Show Recipe Details ———
def show_recipe(recipe):
    st.subheader(recipe.get("title", "Untitled recipe"))
    col1, col2 = st.columns([1, 2])

    with col1:
        for kind in ("usedIngredients", "missedIngredients", "unusedIngredients"):
            items = recipe.get(kind, [])
            if items:
                label = kind.replace("Ingredients", "")
                st.markdown(f"**{label} Ingredients**")
                for ing in items:
                    amt = round(people_count * ing.get("amount", 0), 2)
                    unit = ing.get("unitLong") or ing.get("unit") or ""
                    name = ing.get("originalName") or ing.get("name")
                    st.write(f"- {amt:g} {unit} {name}")

    with col2:
        if recipe.get("image"):
            st.image(recipe["image"], caption=recipe.get("title", ""), use_container_width=True)

        combined = recipe.get("usedIngredients", []) + recipe.get("missedIngredients", [])
        data = {
            ing.get("originalName") or ing.get("name"): people_count * ing.get("amount", 0)
            for ing in combined
        }
        df = pd.DataFrame.from_dict(data, orient="index", columns=["Amount"])
        df.index.name = "Ingredient"
        st.bar_chart(df)

        try:
            nutrition = fetch_nutrition(recipe.get("id"))
            carbs = float(nutrition.get("carbs", "0g").rstrip("g")) * people_count
            protein = float(nutrition.get("protein", "0g").rstrip("g")) * people_count
            fat = float(nutrition.get("fat", "0g").rstrip("g")) * people_count

            macros = {"Carbs": carbs, "Protein": protein, "Fat": fat}
            pie_col, val_col = st.columns([1, 1])

            with pie_col:
                fig, ax = plt.subplots()
                fig.patch.set_facecolor("white")
                ax.set_facecolor("white")
                ax.pie(macros.values(), labels=macros.keys(), autopct="%1.1f%%", startangle=90)
                ax.set_title("Macronutrient Distribution")
                ax.axis("equal")
                st.pyplot(fig)

            with val_col:
                st.markdown("**Total (g):**")
                st.write(f"- Carbs: {carbs:.1f} g")
                st.write(f"- Protein: {protein:.1f} g")
                st.write(f"- Fat: {fat:.1f} g")

        except requests.HTTPError:
            st.warning("⚠️ Could not fetch nutrition info.")

# ——— Display Selected Favorite ———
if st.session_state.selected_fav:
    st.markdown("---")
    st.write("### Selected Favorite Recipe")
    show_recipe(st.session_state.selected_fav)

# ——— Display Search Results ———
if isinstance(st.session_state.recipes_data, list) and st.session_state.recipes_data:
    st.markdown("---")
    st.subheader("Search Results")
    for recipe in st.session_state.recipes_data:
        show_recipe(recipe)
        if any(f["id"] == recipe["id"] for f in st.session_state.favorites):
            st.button("⭐ Favorited", disabled=True, key=f"disabled_{recipe['id']}")
        else:
            if st.button("⭐ Add to Favorites", key=f"fav_{recipe['id']}"):
                st.session_state.favorites.append(recipe)
