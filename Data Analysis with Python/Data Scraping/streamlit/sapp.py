import pandas as pd
import streamlit as st

def intro():
    import streamlit as st

    st.write("# Welcome to my simple WebApp 👋")
    st.sidebar.success("Select a page above.")

    st.markdown(
        """
        ### Some Context

        This App explores the relation between price, size and number of rooms along a relatively large dataset. The data was scraped from 2 property websites in the area that I live in. The motivation behind this project was
        to try and find a solution to easily having a large excel file with properties and filtering them while having an easily accessable link that leads directly to the posting after hearing a friend who was complaining about finding a 
        property to rent because going through several website and interfaces was a waste of time.

        &nbsp;
        ### 🌱 I am currently working on:
        - Learning Data Analysis and Visualization using Python, SQL, Excel, [Tableau](https://public.tableau.com/app/profile/yousef.barakat)
        - Expanding my [Portfolio](https://github.com/YousefBarakat99/My_Portfolio)
        
        &nbsp;
        ### :mailbox_with_mail: Where you could find me:
        [<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/01/LinkedIn_Logo.svg/2560px-LinkedIn_Logo.svg.png" width="150"/>](https://www.linkedin.com/in/yousef-barakat-019816205/)
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[<img src="https://cdn-icons-png.flaticon.com/512/3037/3037366.png" height="40"/>](https://yousefbarakat99.github.io/website/)
        
    """
    , unsafe_allow_html=True)

def general():
    import streamlit as st
    import pandas as pd
    import numpy as np
    import seaborn as sns
    import matplotlib.pyplot as plt

    st.subheader('General property info')
    df = pd.read_excel('Houses_Cleaned.xlsx')
    st.dataframe(df.sort_values(['Rooms', 'Price (HUF)']).reset_index(drop=True))
    count = df['Price (HUF)'].count()
    ravg = np.mean(df['Rooms']).round(1)
    savg = np.mean(df['Size (m2)']).round(2)
    pavg = int(np.mean(df['Price (HUF)']))
    st.write(f'''There is a total of {count} properties. The average number of rooms is {ravg},
     the average size is {savg} m2 and the average rent price is {pavg} HUF.''')
    st.write('')
    st.write('')
    st.write('Choose a visualization from below.')
    tab1, tab2 = st.tabs(['Room count', 'Parameter correlation'])
    with tab1:
        fig, ax = plt.subplots(figsize=(10,10))
        ax.hist('Rooms', data=df)
        ax.set_xlim(right=8)
        ax.set_xlabel('Number of rooms')
        ax.set_title('Count of properties with number of rooms')
        st.write('''The most common number of rooms amongst properties is 3, followed by 4 then by 2. 
        This can be due to the fact that some properties count the living room as an additional room or bedroom.''')
        st.pyplot(fig)
    with tab2:
        corr = df.corr(numeric_only=True)
        st.write('An obvious correlation can be found between size of property and the rent price of it.')
        fig = plt.figure(figsize=(6,4))
        sns.heatmap(corr, annot=True)
        st.pyplot(fig)

def rooms_ft():
    import streamlit as st
    import pandas as pd
    import matplotlib.pyplot as plt

    st.write('Filter by rooms')
    rooms = st.radio('Number of rooms', ('1', '2', '3', '>3'))
    df = pd.read_excel('Houses_Cleaned.xlsx')
    if rooms == '1':
        st.dataframe(df[df['Rooms'] == 1].sort_values('Price (HUF)').reset_index(drop=True))
        df1 = df[(df['Rooms'] == 1) & (df['Price (HUF)'] > 50_000) & (df['Size (m2)'].notna())].sort_values('Price (HUF)').reset_index(drop=True)
        fig, ax = plt.subplots()
        ax.plot('Price (HUF)', 'Size (m2)', data=df1)
        ax.set_title('Price vs Size in m2')
        ax.set_xlabel('Price in HUF')
        ax.set_ylabel('Size of property in m2')
        st.pyplot(fig)
    elif rooms == '2':
        st.dataframe(df[df['Rooms'] == 2].sort_values('Price (HUF)').reset_index(drop=True))
        df1 = df[(df['Rooms'] == 2) & (df['Price (HUF)'] > 40_000) & (df['Size (m2)'].notna())].sort_values('Price (HUF)').reset_index(drop=True)
        fig, ax = plt.subplots()
        ax.plot('Price (HUF)', 'Size (m2)', data=df1)
        ax.set_title('Price vs Size in m2')
        ax.set_xlabel('Price in HUF')
        ax.set_ylabel('Size of property in m2')
        st.pyplot(fig)
    elif rooms == '3':
        st.dataframe(df[df['Rooms'] == 3].sort_values('Price (HUF)').reset_index(drop=True))
        df1 = df[(df['Rooms'] == 3) & (df['Price (HUF)'] > 40_000) & (df['Size (m2)'].notna())].sort_values('Price (HUF)').reset_index(drop=True)
        fig, ax = plt.subplots()
        ax.plot('Price (HUF)', 'Size (m2)', data=df1)
        ax.set_title('Price vs Size in m2')
        ax.set_xlabel('Price in HUF')
        ax.set_ylabel('Size of property in m2')
        st.pyplot(fig)
    elif rooms == '>3':
        st.dataframe(df[df['Rooms'] >3 ].sort_values('Price (HUF)').reset_index(drop=True))
        df1 = df[(df['Rooms'] > 3) & (df['Price (HUF)'] > 40_000) & (df['Size (m2)'].notna())].sort_values('Price (HUF)').reset_index(drop=True)
        fig, ax = plt.subplots()
        ax.plot('Price (HUF)', 'Size (m2)', data=df1)
        ax.set_title('Price vs Size in m2')
        ax.set_xlabel('Price in HUF')
        ax.set_ylabel('Size of property in m2')
        ax.ticklabel_format(style='plain')
        st.pyplot(fig)


page_names_to_funcs = {
    "—": intro,
    "General info": general,
    "Filter by rooms": rooms_ft
}

demo_name = st.sidebar.selectbox("Choose a page", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()

