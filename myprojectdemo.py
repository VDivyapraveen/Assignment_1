import mysql.connector
import streamlit as st
import pandas as pd



mydb = mysql.connector.connect(
    host="localhost",
    database="proj_1",
    user="root",
    password=""
)
mycursor=mydb.cursor()
print("Connection Established")



from streamlit_option_menu import option_menu

with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu", # Title of the menu (shows up on top if vertical; not shown if horizontal)
        options=["Home page", "Analysis page", "End page"],   # Menu options the user can click
        icons=["house", "clipboard-data", "arrow-right-circle-fill"],  # Bootstrap icons for each menu item
        menu_icon="cast",                 # Icon beside the menu title (if vertical)
        default_index=0,                  # The menu item selected by default (0 = first item, i.e., "Home")
        orientation="vertical"          # Layout of the menu: "horizontal" or "vertical"
)
if selected == "Home page":
    
    # st.sidebar.title("Tennis data dashboard")
    st.title("Tennis data dashboard :tennis:")
    st.subheader("💡 Sportradar Tennis API Overview ")
    st.write("_Sportradar is a leading global provider of sports data and content. Its Tennis API offers real-time and historical data for men's and women's professional tennis competitions, covering various tours and tournament levels._")
    st.markdown("---")

    st.subheader("💡 What Does the Tennis API Provide?")
   

    st.write("""_The Tennis API provides detailed information for:_""")
    st.write(" _Categories🧩_")
    st.write(" _Competitions_ (e.g., ATP, WTA, ITF)🎾")
    st.write(" _Tournaments & Matches🏆_")
    st.write(" _Venues and Complexes📍_")
    st.write(" _Players and Rankings📊_")
    st.write(" _Competitors🧑‍🤝‍🧑_")
    st.markdown("---")
    st.subheader("💡 What You Can Do Here:")
    st.write(" _Filter and search tennis data dynamically🎯_")
    st.markdown("---")


elif selected == "Analysis page":
   
    # Step 1: Select table
    mycursor.execute("SHOW TABLES")
    tables = [table[0] for table in mycursor.fetchall()]
    st.subheader("Select a table:")
    selected_table = st.selectbox("", tables)
  
    if selected_table:
        # Step 2: Get all column names
        mycursor.execute(f"""
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA = 'proj_1' AND TABLE_NAME = '{selected_table}'
        """)
        columns = [col[0] for col in mycursor.fetchall()]

     
        # Step 3: Let user pick columns to filter by (multi-select)
        
        st.subheader("Select column(s) to filter by:")
        selected_columns = st.multiselect("", columns)

     

        # # Step 4: For each selected column, create a dropdown of distinct values
        
        filter_values = {}
        for col in selected_columns:
            mycursor.execute(f"SELECT DISTINCT `{col}` FROM `{selected_table}`")
            raw_vals = [row[0] for row in mycursor.fetchall()]

    # Check for None and add "<NULL>" explicitly if needed
            display_vals = [val for val in raw_vals if val is not None]
            if any(val is None for val in raw_vals):
                display_vals.append("<NULL>")

    # Sort display values to make it cleaner (optional)
            display_vals = sorted(display_vals, key=lambda x: str(x))

            st.subheader(f"Select value for '{col}':")
            selected_val = st.selectbox("", display_vals, key=col)
            filter_values[col] = None if selected_val == "<NULL>" else selected_val

        st.markdown("---")

        # Step 5: Build query dynamically
        a = []
        b = []
        for col, val in filter_values.items():
            if val is None:
                a.append(f"`{col}` IS NULL")
            else:
                a.append(f"`{col}` = %s")
                b.append(val)

        c = " AND ".join(a)
        query = f"SELECT * FROM `{selected_table}`"
        if c:
            query += f" WHERE {c}"

        mycursor.execute(query, tuple(b))
        data = mycursor.fetchall()
        col_names = [col[0] for col in mycursor.description]
        df = pd.DataFrame(data, columns=col_names)

        st.subheader("Filtered Data")
        st.dataframe(df)

        filtered_rows = len(df)

# Markdown formatting in the sidebar
        st.sidebar.markdown(f"""
        <div style="font-size: 24px; font-weight: bold; color: Black;">
        📊 Filtered Rows(Count): {filtered_rows}
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

elif selected=="End page":
        st.subheader("👩‍💻 Built With ❤️ Using:")
        st.write("_Streamlit for interactive frontend_")
        st.write("_Pandas & MySQL for data management_")
        st.write("_Sportradar API for real-time sports data_")

st.markdown("---")
# Correct direct URL of the image
background_image_url = "https://images.pexels.com/photos/5740526/pexels-photo-5740526.jpeg"




st.markdown(f"""
    <style>
        .stApp {{
            background-image: url("{background_image_url}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
            color: white;
        }}
    </style>
""", unsafe_allow_html=True)



