# Recipe Finder

Our project is a Streamlit web application that helps users discover recipes based on ingredients they have at home. Using the Spoonacular API, this app fetches recipes, shows ingredient quantities based on number of people, and displays nutritional information like calories, protein, fat, and carbohydrates.

---

## Features

- Search recipes by entering ingredients (separate with commas)
- Adjust number of people: dynamically scale ingredient amounts
- Mark recipes as favorites to save them easily
- Sort recipes by:
  - Calories (low/high)
  - Carbs (low/high)
  - Protein (low/high)
  - Fat (low/high)
- Visual nutrition breakdown with pie chart

---

## Requirements

- Python 3.8+
- Streamlit
- Requests
- Pandas
- Matplotlib

Install dependencies:

```bash
pip install -r requirements.txt
```

API key (Spoonacular):

```bash
API_KEY= "4b1abeabfae84cddae3ee1e0803ebc01"
```
