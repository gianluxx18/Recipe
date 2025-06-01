# Recipe Finder

Our project is a Streamlit web application that helps users discover recipes based on ingredients they have at home. Using the Spoonacular API, this app fetches recipes, shows ingredient quantities based on number of people, and displays nutritional information like calories, protein, fat, and carbohydrates.

--- 

Group Members: Behar Saqipi, Gianluca Schorer, Deniz Staufer, Alexandre Zaza

---

# Disclosure: 

This project builds upon a previous work by one of the group members and has been further developed and extended through different features (e.g. sort-function, save-favorites function, showing of nutritional data). ChatGPT was used to assist in the set-up and error correction of the code.

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
requirements.txt
```

API key (Spoonacular):

```bash
API_KEY= "4b1abeabfae84cddae3ee1e0803ebc01"
```

## Set Up via GitHub + Streamlit Cloud

- Fork or clone this repository to your own GitHub account.

- Visit https://streamlit.io/cloud and sign in with your GitHub account.

- Make sure your Github and Streamlit account are linked

- Click “New app”, then:

    - Select the repository containing this project

    - Choose the branch (e.g. "main")

    - Set the file path to the app script ("Recipe_Finder_App.py")

- Click “Deploy” to launch the app.

The API key is already embedded in the code, so no secrets configuration is necessary.

After deployment, you will receive a public URL to share the app.

You can also test the app by clicking on the following link https://recipe-gi4clazwzoysxnaksqlnme.streamlit.app/ (no set-up required).
