# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Customize your Smoothie! :cup_with_straw:")
st.write(
  """Choose the fruits you want in your Smoothie
  
  :apple: :banana: :orange:  :Figs: :strawberry:
  """
)

name_on_order = st.text_input('Name on Smoothie:')
st.write('The Name on your Smoothie will be!', name_on_order)
#option = st.selectbox("What is your favorite fruit?",
#                      ('Banana','Strwawberries','Peaches'))                     )
#st.write('Your favorite food is ', option)
#dataframe fruit list from table

session = get_active_session()
my_dataframe = session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredient_list = st.multiselect("Choose upto 5 ingredients:", my_dataframe,max_selections=5)

if ingredient_list:
    #st.write(ingredient_list)
    #st.text(ingredient_list)
    #st.table(ingredient_list)

    ingredient_string = ''
    for fruit_chosen in ingredient_list:
        ingredient_string += fruit_chosen + ' '
    st.write(ingredient_string)

    my_insert_stmt = """ INSERT INTO SMOOTHIES.PUBLIC.ORDERS(ingredients,name_on_order) 
    values ('"""+ingredient_string+"""','"""+name_on_order+"""')"""
    #st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is Ordered!', icon="✅")
