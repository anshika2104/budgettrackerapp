import sqlite3
import pandas as pd
import streamlit as st
import plotly.express as px
from setup_db import create_connection,create_user,create_user_table,authenticate_user
st.set_page_config(
    page_title="Expense Tracker"
)
st.title(':red[Budget Tracker]')
#initialize session state
if 'login_in' not in st.session_state:
    st.session_state.login_in = False
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
signup_tab,login_tab,category_tab=st.tabs(['Signup','Login','Add and manage categories'])
with signup_tab:
    username=st.text_input('choose your user_id',key='signupkey')
    password=st.text_input('choose your password',type='password',key='passwordkey')
    signup_button=st.button('Signup',key='buttonkey')
    if signup_button:
        if username and password:
            try:
                create_user(username,password)
                st.success('account created')
            except sqlite3.IntegrityError:
                st.error('username already exists')
        else:
            st.error('username or password is empty')
with login_tab:
    username=st.text_input('enter your user_id',key='uernamesignupkey')
    password=st.text_input('enter your password',type='password',key='passwordsignupkey')
    login_button=st.button('Login',key='loginbuttonkey')
    if login_button:
        if username and password:
            user_id=authenticate_user(username,password)
            if user_id:
                st.session_state.login_in=True
                st.session_state.user_id=user_id
                st.success('lets track budget')
            else:
                st.error('username or password is incorrect')
        else:
            st.error('username or password is empty')
if st.session_state.login_in:
    with category_tab:
        
        # Function to add a category
        def add_category(category_name, category_type):
            try:
                conn = create_connection()
                c = conn.cursor()
                c.execute(
                    "INSERT INTO categories_table(category_name, category_type, user_id) VALUES (?, ?, ?)",
                    (category_name, category_type, st.session_state.user_id[0]),
                )
                conn.commit()
                conn.close()
                st.success(f"Category '{category_name}' added successfully!")
            except sqlite3.Error as e:
                st.error(f"Error adding category: {e}")
        
        # Function to display categories
        def display_categories():
            conn = create_connection()
            c = conn.cursor()
            c.execute(
                "SELECT category_name, category_type FROM categories_table WHERE user_id = ?",
                (st.session_state.user_id[0],)
            )
            rows = c.fetchall()
            conn.close()
            if rows:
                df = pd.DataFrame(rows, columns=['Category Name', 'Category Type'])
                st.dataframe(df)
                data=df['Category Type'].value_counts().reset_index()
                data.columns = ['Category Type', 'Count']
                st.dataframe(data)
                fig = px.bar(data_frame=data, x='Category Type', y='Count',text='Count')
                st.plotly_chart(fig)

            else:
                st.write("No categories available.")
        
        # User interface for adding and managing categories
        st.subheader('Add and Manage Categories')
        
        # Input fields for category
        category_name = st.text_input('Enter category name', key='category_name_input')
        category_type = st.selectbox(
            "Select category type",
            ['expense', 'income', 'savings'],  # Match the CHECK constraint values
            key='category_type_select'
        )
        
        # Add category button
        if st.button('Add Category', key='add_category_button'):
            if category_name and category_type:
                add_category(category_name, category_type)
            else:
                st.error("Please provide both category name and type.")
        
        # Display existing categories
        st.subheader('Existing Categories')
        display_categories()
        # # Plotly bar graph
        # if rows_df is not None:
        #     st.subheader('Category Distribution')
        #     category_count = rows_df['Category Type'].value_counts().reset_index()
        #     category_count.columns = ['Category Type', 'Count']

        #     # Create a bar chart
        #     fig = px.bar(
        #         category_count,
        #         x='Category Type',
        #         y='Count',
        #         title='Category Distribution',
        #         color='Category Type',
        #         text='Count',
        #     )
        #     fig.update_traces(textposition='outside')
        #     st.plotly_chart(fig)



# if st.session_state.login_in:
#     with category_tab:
        
#         def add_category(category_name,category_type):
#             conn = create_connection()
#             c = conn.cursor()
#             c.execute("INSERT INTO categories_table(category_name, category_type, user_id) VALUES (?, ?, ?)",
#           (category_name, category_type, st.session_state.user_id[0]))

#             conn.commit()
#             conn.close()
#         def display_categories():
#             conn = create_connection()
#             c = conn.cursor()
#             c.execute("SELECT categories_name,categories_type FROM categories_table WHERE user_id = ?", (st.session_state.user_id[0]
#                                                                            ,))
#             rows = c.fetchall()
#             conn.close()
#             if rows:
#                 df=pd.DataFrame(rows,columns=['category_name','category_type'])
#                 st.dataframe(df)
#             else:
#                 st.write("No categories available")
#     st.subheader('Add and mange categories')
#     category_name = st.text_input('Subcategory',key='categoryname')
#     category_type = st.selectbox("Select category type",key='categorytype' )
#     category_button=st.button('Add category',key='categorybutton')

    

