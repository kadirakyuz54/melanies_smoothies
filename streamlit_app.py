# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("Smoothie App 🥤")
st.write(
    """Choose the Fruits you want in your custom Smoothie!
    """
)

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

# 1. Capture the customer's name
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

# 2. Ingredient multiselect dropdown wrapper
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections = 5
)

if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    # 3. FIXED: Added 'name_on_order' column to the target column list
    my_insert_stmt = """insert into smoothies.public.orders(ingredients, name_on_order)
        values ('""" + ingredients_string + """', '""" + name_on_order + """')"""

    # Comment out debugging lines so they don't clutter the final UI
    # st.write(my_insert_stmt)
    # st.stop()
    
    # 4. Form Submission Button Gatekeeper
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        
        # EXTRA CREDIT: Appending the customer's name dynamically to the success banner!
        st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")


import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
# st.text(smoothiefroot_response)
# Convert the JSON payload into a clean, wide dataframe layout
sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
