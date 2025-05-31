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
if "recipes_data" not in st.session_state:
    st.session_state.recipes_data = []
if "favorites" not in st.session_state:
    st.session_state.favorites = []
if "show_favorites" not in st.session_state:
    st.session_state.show_favorites = False
if "display_count" not in st.session_state:
    st.session_state.display_count = 5
if "people_count" not in st.session_state:
    st.session_state.people_count = 1

# ——— Input Widgets ———
if not st.session_state.show_favorites:
    st.session_state.people_count = st.number_input(
        "Number of people",
        min_value=1,
        max_value=100,
        value=st.session_state.people_count,
        step=1,
    )
    ingredients = st.text_input(
        "Ingredients (comma-separated)",
        key="ingredients",
        placeholder="e.g. flour, eggs, milk",
    )

# ——— Fetch Functions ———
def fetch_recipes(ingredients_str: str):
    params = {"apiKey": API_KEY, "ingredients": ingredients_str, "number": 50}
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

# ——— Buttons for View Toggle ———
if st.session_state.show_favorites:
    if st.button("🔍 Back to Search"):
        st.session_state.show_favorites = False
        st.session_state.display_count = 5
else:
    if st.button("⭐ Show Favorites"):
        st.session_state.show_favorites = True

# ——— Search Action ———
if not st.session_state.show_favorites and st.button("Search Recipes"):
    ingr = st.session_state.ingredients.strip()
    if not ingr:
        st.warning("❗ Please enter at least one ingredient.")
    else:
        try:
            st.session_state.recipes_data = fetch_recipes(ingr)
            st.session_state.display_count = 5
        except requests.HTTPError as e:
            st.error(f"API Error: {e}")
            st.session_state.recipes_data = []

# ——— Display Section ———
if st.session_state.show_favorites:
    st.header("⭐ Favorite Recipes")
    recipes = st.session_state.favorites
else:
    recipes = st.session_state.recipes_data[:st.session_state.display_count]

if not isinstance(recipes, list) or not recipes:
    st.info("No recipes to show.")
else:
    for recipe in recipes:
        st.subheader(recipe.get("title", "Untitled recipe"))
        col1, col2 = st.columns([1, 2])

        with col1:
            for kind in ("usedIngredients", "missedIngredients", "unusedIngredients"):
                items = recipe.get(kind, [])
                if items:
                    label = kind.replace("Ingredients", "")
                    st.markdown(f"**{label} Ingredients**")
                    for ing in items:
                        amt = round(st.session_state.people_count * ing.get("amount", 0), 2)
                        unit = ing.get("unitLong") or ing.get("unit") or ""
                        name = ing.get("originalName") or ing.get("name")
                        st.write(f"- {amt:g} {unit} {name}")
            if recipe not in st.session_state.favorites:
                if st.button("Add to Favorites", key=f"fav_{recipe['id']}"):
                    st.session_state.favorites.append(recipe)
            else:
                if st.button("Remove from Favorites", key=f"rm_{recipe['id']}"):
                    st.session_state.favorites = [
                        r for r in st.session_state.favorites if r["id"] != recipe["id"]
                    ]
                    st.experimental_rerun()

        with col2:
            if recipe.get("image"):
                st.image(
                    recipe["image"],
                    caption=recipe.get("title", ""),
                    use_container_width=True
                )

            combined = recipe.get("usedIngredients", []) + recipe.get("missedIngredients", [])
            data = {
                ing.get("originalName") or ing.get("name"): st.session_state.people_count * ing.get("amount", 0)
                for ing in combined
            }
            df = pd.DataFrame.from_dict(data, orient="index", columns=["Amount"])
            df.index.name = "Ingredient"
            st.bar_chart(df)

            try:
                nutrition = fetch_nutrition(recipe.get("id"))
                carbs = float(nutrition.get("carbs", "0g").rstrip("g")) * st.session_state.people_count
                protein = float(nutrition.get("protein", "0g").rstrip("g")) * st.session_state.people_count
                fat = float(nutrition.get("fat", "0g").rstrip("g")) * st.session_state.people_count

                macros = {"Carbs": carbs, "Protein": protein, "Fat": fat}
                pie_col, val_col = st.columns([1, 1])

                with pie_col:
                    fig, ax = plt.subplots()
                    fig.patch.set_facecolor("white")
                    ax.set_facecolor("white")
                    ax.pie(
                        macros.values(),
                        labels=macros.keys(),
                        autopct="%1.1f%%",
                        startangle=90,
                    )
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

# ——— Show More Button ———
if not st.session_state.show_favorites:
    if "show_more" not in st.session_state:
        st.session_state.show_more = False

    if st.button("Show more"):
        st.session_state.show_more = True

    if st.session_state.show_more:
        st.session_state.display_count += 5
        st.session_state.show_more = False
