import streamlit as st
import pandas as pd
import plotly.express as px
import json
from streamlit_option_menu import option_menu

# Set page config
st.set_page_config(
    page_title="PeepIntoPe",
    page_icon="./phonepe-logo.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load data functions
@st.cache_data
def load_insurance_data():
    return pd.read_csv("./data files/agg_insurance_state_level.csv")

@st.cache_data
def load_device_user_data():
    return pd.read_csv("./data files/agg_user_state_level.csv")

@st.cache_data
def load_country_transaction():
    return pd.read_csv("./data files/agg_transcation_country_level.csv")

@st.cache_data
def load_state_transaction():
    return pd.read_csv("./data files/agg_transcation_state_level.csv")

@st.cache_data
def load_country_insurance():
    return pd.read_csv("./data files/agg_insurance_country_level.csv")

@st.cache_data
def load_state_insurance():
    return pd.read_csv("./data files/agg_insurance_state_level.csv")

@st.cache_data
def load_geojson():
    with open('./data files/states_india.geojson', 'r') as f:
        return json.load(f)

# Menu
selected = option_menu(
    menu_title=None,
    options=["Map","Transaction", "Insurance","User"],
    icons=["geo-alt-fill", "cash-stack", "shield-lock", "person-badge"],
    orientation="horizontal",
    default_index=0,
    styles={
        "container": {"padding": "10px", "background-color": "#6a1b9a"},
        "nav-link": {"color": "white", "font-size": "16px", "margin": "0px"},
        "nav-link-selected": {"background-color": "#7f2da8"},
    }
)

st.markdown("""   
        <style>
  
        [data-testid="stSidebar"] {
            min-width: 300px;
            max-width: 300px;
        }

        .stSelectbox div[data-baseweb="select"] {
            background-color: white !important;
            color: black !important;
            border-radius: 5px;
        }

        .stSelectbox span {
            color: black !important;
        }

        [data-testid="stSidebarContent"] {
            padding: 1rem;
        }
        
        .text {
            font-family: Arial, sans-serif;
            font-weight: bold;                
            color : #58148C;
            font-size: 35px;
            text-align: left;
        }

        .metric-card {
            background-color:#f6f7f8;    
            padding: 2rem;
            border: 2px solid #58148c;
            border-radius:12px;    
            color: #58148c;
            font-family: 'Arial', sans-serif;
        }

        .metric-card h3 {
            color: #58148c;
            margin-bottom: 0.2rem;
            font-size: 35px;
        }

        .metric-card p {
            margin: 0.5rem 0;
            font-size: 32px;
            color:#8445b8;
            font-weight: bold;
        }

        .divider {
            height: 2px;
            background-color: #58148c;
            margin: 1rem 0;
        }

        .sub-label {
            font-weight:bold;
            color:black;    
            font-size: 15px;
            margin-bottom: 0.2rem;
        }

        .sub-value {
            color: black;
            font-size: 22px;
            font-weight: bold;
        }

        .category-card {
            background-color:#f6f7f8;    
            border: 2px solid #58148c;
            border-radius:12px; 
            padding: 1.5rem;
            font-weight:bold;
            font-family: 'Arial', sans-serif;
        }

        .category-card h3 {
            color: #58148c;
            font-size: 35px;
            margin-bottom: 0.5rem;
        }

        .category-row {
            display: flex;
            justify-content: space-between;
            padding: 6px 0;
            font-weight:bold;    
            border-bottom: 0.5px solid #333;
            font-size: 16px;
        }

        .category-name {
            font-weight: bold;
        }

        .category-value {
            color: #8445b8;
            font-weight: 700;
            font-size:18px;    
        }

        .divider {
            height: 2px;
            background-color: #58148c;
            margin-top: 1rem;
        }
            /* Sidebar background */
    [data-testid="stSidebar"] {         
        min-width: 300px;
        max-width: 300px;
    }

    /* Make selectbox text black */
    .stSelectbox div[data-baseweb="select"] {
        background-color: white !important;
        color: black !important;
        border-radius: 5px;
    }

    .stSelectbox span {
        color: black !important;
    }

    /* Optional: padding */
    [data-testid="stSidebarContent"] {
        padding: 1rem;
    }

    /*Insurance info*/              
     .insurance-card {
        font-family: Arial, sans-serif;
        text-align: left;
    }

    .insurance-card .sub{
      margin-bottom:15px;       
    }                       

    .insurance-card h1 {
        color : #58148C;
        font-size: 50px; 
                
    }
                
    .insurance-card h2 {
        font-weighr:bold;
        font-size: 22px; 
                
    }           

    .insurance-card .value {
        font-weight: bold;
        color : #58148C;
        font-size: 22px;
        padding-bottom:20px; 
    }     
        </style>""", unsafe_allow_html=True)

# Pages
if selected == "Map":
    st.title("Insurance Amount by State")
    df_agg_insu = load_insurance_data()
    india_geojson = load_geojson()

    df_agg_insu['State'] = df_agg_insu['State'].str.replace('-', ' ').str.title()
    year = st.sidebar.selectbox("Select Year", sorted(df_agg_insu['Year'].unique()))
    quarter = st.sidebar.selectbox("Select Quarter", sorted(df_agg_insu['Quarter'].unique()))

    filtered_df = df_agg_insu[(df_agg_insu['Year'] == year) & (df_agg_insu['Quarter'] == quarter)]

    fig = px.choropleth(
        filtered_df,
        geojson=india_geojson,
        locations='State',
        featureidkey='properties.st_nm',
        color='InsuranceAmount',
        color_continuous_scale='Purples',
        title=f"Insurance Amount by State - {year} Q{quarter}",
        scope="asia"
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r": 0, "t": 30, "l": 0, "b": 0})
    st.plotly_chart(fig, use_container_width=True)

elif selected == "User":
    st.title("User Count Per Brand")
    df = load_device_user_data()
    df['State'] = df['State'].str.replace('-', ' ').str.title()

    state_list = sorted(df['State'].unique())
    selected_state = st.sidebar.selectbox("Select State", state_list)
    selected_year = st.sidebar.selectbox("Select Year", sorted(df['Year'].unique()))
    selected_quarter = st.sidebar.selectbox("Select Quarter", sorted(df['Quarter'].unique()))

    filtered_df = df[
        (df['State'] == selected_state) &
        (df['Year'] == selected_year) &
        (df['Quarter'] == selected_quarter)
    ]

    if filtered_df.empty:
        st.warning("No data available for the selected filters.")
    else:
        filtered_df["Year"] = filtered_df["Year"].astype(str)
        fig = px.bar(
            filtered_df,
            x="Brand",
            y="Count",
            color="Year",
            barmode="group",
            title=f"{selected_state}, Q{selected_quarter} {selected_year}",
            color_discrete_sequence=["#A745D1", "#7B1FA2", "#6A1B9A", "#7F2DA8", "#58148C"],
            hover_data=["State", "Quarter", "Count"]
        )
        fig.update_layout(xaxis_title="Device Brand", yaxis_title="No. of Users", legend_title="Year", bargap=0.2)
        st.plotly_chart(fig, use_container_width=True)

elif selected == "Transaction":
    st.sidebar.image('./rupee.png', width=150)
    view_option = st.sidebar.selectbox("", ["Country", "State"])

    df_agg_trans = load_state_transaction() if view_option == "State" else load_country_transaction()

    total_transactions = df_agg_trans['TransactionCount'].sum()
    total_payment_value = df_agg_trans['TransactionAmount'].sum()
    avg_transaction_value = df_agg_trans['TransactionAmount'].mean()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""<div class="metric-card">
            <h3>Transactions</h3>
            <div class="sub-label">All PhonePe transactions (UPI + Cards + Wallets)</div>
            <p>{total_transactions:,.0f}</p>
            <div class="divider"></div>
            <div class="sub-label">Total Payment Value</div>
            <div class="sub-value">₹{total_payment_value:,.0f}</div>
            <div class="sub-label" style="margin-top: 0.8rem;">Avg. Transaction Value</div>
            <div class="sub-value">₹{avg_transaction_value:,.0f}</div>
        </div>""", unsafe_allow_html=True)

    with col2:
        categories = df_agg_trans['TransactionType'].unique()
        html = """<div class="category-card">
        <h3>Categories</h3>
        <div class="sub-label">Total Amount Collected Per Category</div>
        <div class="divider"></div>"""

        for category in categories:
            df_filtered = df_agg_trans[df_agg_trans['TransactionType'] == category]
            value = df_filtered['TransactionAmount'].sum()
            html += f"""
            <div class="category-row">
                <div class="category-name">{category}</div>
                <div class="category-value">₹{value:,.0f}</div>
            </div>"""

        html += """</div>"""
        st.markdown(html, unsafe_allow_html=True)

    ### ---- Transction Info End  ------ ###


    
    if view_option == "State":
        state_list = sorted(df_agg_trans['State'].unique())
        selected_state = st.sidebar.selectbox("Select State", state_list)

    year = st.sidebar.selectbox("Select Year", sorted(df_agg_trans['Year'].unique()))
    quarter = st.sidebar.selectbox("Select Quarter", sorted(df_agg_trans['Quarter'].unique()))
    metric = st.sidebar.selectbox("Select Metric", ['TransactionCount', 'TransactionAmount'])

    df_filtered = df_agg_trans[(df_agg_trans['Year'] == year) & (df_agg_trans['Quarter'] == quarter)]
    if view_option == "State":
        df_filtered = df_filtered[df_filtered['State'] == selected_state]

    if df_filtered.empty:
        st.warning("No data available for selected filters.")
    else:
        st.subheader("Pie Chart")
        pie_fig = px.pie(
            df_filtered,
            names="TransactionType",
            values=metric,
            title="Transaction Share by Type",
            color_discrete_sequence=["#A745D1", "#7B1FA2", "#6A1B9A", "#7F2DA8", "#58148C"]
        )
        pie_fig.update_traces(textinfo='percent+label', hole=0.3)
        st.plotly_chart(pie_fig, use_container_width=True)

        st.subheader("Bar Chart")
        bar_fig = px.bar(
            df_filtered,
            x=metric,
            y="TransactionType",
            orientation="h",
            title="Transaction Value by Type",
            color="TransactionType",
            color_discrete_sequence=["#A745D1", "#7B1FA2", "#6A1B9A", "#7F2DA8", "#58148C"]
        )
        st.plotly_chart(bar_fig, use_container_width=True)

elif selected == "Insurance":
    view_option = st.selectbox("", ["India", "State"])
    df_agg_insu = load_country_insurance() if view_option == "India" else load_state_insurance()
    if view_option == "State":
        state = st.selectbox("Select State", sorted(df_agg_insu['State'].unique()))
        df_agg_insu = df_agg_insu[df_agg_insu['State'] == state]
    else:
        state = "India"

    total_policies = df_agg_insu["InsuranceCount"].sum()
    total_value = df_agg_insu["InsuranceAmount"].sum()
    insu_avg = df_agg_insu['InsuranceAmount'].mean()

    st.sidebar.markdown(f"""
    <div class="insurance-card">
        <h1>Insurance</h1>           
        <p>Total Insurance Policies Purchased Across {state} (Nos.)</p>
        <div class="value">{total_policies:,.0f}</div>
            <div class="sub">
                <h2>Total premium value</h2>
                <div>₹{total_value:,.0f}</div>
            </div>
            <div class="sub">
                <h2>Average premium value</h2>
                <div>₹{insu_avg:,.0f}</div>
            </div>
    </div>
    """, unsafe_allow_html=True)

    df_agg_insu["Year"] = df_agg_insu["Year"].astype(str)
    fig = px.bar(
        df_agg_insu,
        x="Quarter",
        y="InsuranceAmount",
        color="Year",
        barmode="group",
        title="Insurance Amount by Quarter and Year",
        color_discrete_sequence=["#A745D1", "#7B1FA2", "#6A1B9A", "#7F2DA8", "#58148C"]
    )
    st.plotly_chart(fig, use_container_width=True)
