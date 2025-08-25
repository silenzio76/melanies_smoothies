# Import python packages
import datetime
import requests
import streamlit as st

from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col


smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")


# Write directly to the app
st.title(f":cup_with_straw: Customize YOUR Smoothie!:cup_with_straw: {st.__version__}")
st.write("Choose the fruits you want in your smoothie of choice!.")

name_of_order = st.text_input("Name on smoothie:")
st.write("the name on your smoothie will be: " + name_of_order)

contactOptions = st.selectbox("How we can contact you?", ('E-Mail', 'Home phone', 'Mobile phone'),2)

from snowflake.snowpark.functions import col

#session = get_active_session() -- used directly in snowflake
# in github use
cnx = st.connection("snowflake")
session = cnx.session()
sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=true)
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))

#ingredient_list = st.multiselect('Chose up to 6 fruits!', my_dataframe, max_selections=6)
ingredient_list = st.multiselect('Chose up to 6 fruits!', sf_df, max_selections=6)
ingredient_str = ''

for fruit_chosen in ingredient_list:
    if len(ingredient_str) > 0:
        ingredient_str += ','
    ingredient_str += fruit_chosen


time_to_insert = st.button('Submit order')

insert_stmt = """INSERT INTO SMOOTHIES.PUBLIC.ORDERS (order_INGREDIENTS, order_CONTACT, order_NAME_ON_ORDER, order_OPEN_DATE_TIME) VALUES ('""" + ingredient_str + """', '""" + contactOptions + """', '""" + name_of_order + """', '""" + datetime.datetime.now().isoformat() + """');"""

if time_to_insert:
    session.sql(insert_stmt).collect()
    st.success('Your Smoothie is ordered! '+ name_of_order + '!!!', icon="✅")
