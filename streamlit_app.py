# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd  # Added Pandas import

# Write directly to the app
st.title("Smoothie App 🥤")
st.write(
    """Choose the Fruits you want in your custom Smoothie!
    """
)

# Establish connection securely for cloud deployment
cnx = st.connection("snowflake")
session = cnx.session()

# Select BOTH columns from your fruit_options table now
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))

# Convert the Snowpark Dataframe to a Pandas Dataframe so we can use LOC later
pd_df = my_dataframe.to_pandas()

# Debugging block from the lab instructions to view the new structure
st.dataframe(pd_df)
st.stop()

# 1. Capture the customer's name
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

# 2. Ingredient multiselect dropdown wrapper
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,  # Keep this as my_dataframe for the UI picker dropdown
    max_selections = 5
)

if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        
        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    my_insert_stmt = """insert into smoothies.public.orders(ingredients, name_on_order)
        values ('""" + ingredients_string + """', '""" + name_on_order + """')"""

    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")
