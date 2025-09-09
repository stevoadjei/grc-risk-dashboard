import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="GRC Risk Assessment Dashboard",
    page_icon="🛡️",
    layout="wide"
)

# --- DATA LOADING ---
@st.cache_data
def load_data():
    df = pd.read_csv('vendor_risk_data.csv')
    # Create a categorical risk level for easier filtering
    bins = [0, 8, 16, 25]
    labels = ['Low', 'Medium', 'High']
    df['RiskLevel'] = pd.cut(df['OverallRiskScore'], bins=bins, labels=labels, right=True)
    return df

df = load_data()

# --- SIDEBAR FILTERS ---
st.sidebar.header("Dashboard Filters")

# FIX: Convert the unique() output to a list with .tolist() for all multiselects
options_risk_level = df['RiskLevel'].unique().tolist()
risk_levels = st.sidebar.multiselect(
    "Filter by Risk Level",
    options=options_risk_level,
    default=options_risk_level
)

options_service_type = df['ServiceType'].unique().tolist()
service_types = st.sidebar.multiselect(
    "Filter by Service Type",
    options=options_service_type,
    default=options_service_type
)

options_country = df['Country'].unique().tolist()
countries = st.sidebar.multiselect(
    "Filter by Country",
    options=options_country,
    default=options_country
)


# --- APPLY FILTERS ---
# Create a new dataframe that reflects the user's filter selections
df_filtered = df[
    df['RiskLevel'].isin(risk_levels) &
    df['ServiceType'].isin(service_types) &
    df['Country'].isin(countries)
]

# --- MAIN PAGE ---
st.title("🛡️ GRC Third-Party Risk Assessment Dashboard")
st.markdown("Use the filters on the left to analyze vendor risk profiles, compliance, and potential threats.")

# --- CREATE TABS FOR DIFFERENT VIEWS ---
tab1, tab2 = st.tabs(["📊 Overall Risk Landscape", "🤖 AI Vendor Assessment"])

# --- TAB 1: OVERALL RISK LANDSCAPE ---
with tab1:
    # --- KEY METRICS (NOW DYNAMIC) ---
    st.header("Key Risk Indicators")

    HIGH_RISK_THRESHOLD = 15

    # Calculate metrics based on the FILTE RED data
    total_vendors = len(df_filtered)
    high_risk_vendors = len(df_filtered[df_filtered['OverallRiskScore'] > HIGH_RISK_THRESHOLD])
    ai_vendors = df_filtered['Is_AI_Vendor'].sum()
    # Handle division by zero if no vendors are selected
    avg_breach_likelihood = df_filtered['BreachLikelihoodScore'].mean() if not df_filtered.empty else 0


    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Total Vendors Selected", value=total_vendors)
    with col2:
        st.metric(label="High-Risk Vendors", value=high_risk_vendors)
    with col3:
        st.metric(label="AI-Powered Vendors", value=ai_vendors)
    with col4:
        st.metric(label="Avg. Breach Likelihood", value=f"{avg_breach_likelihood:.0f}%")

    st.markdown("---")

    # --- VISUALIZATIONS (NOW DYNAMIC) ---
    st.header("Risk Analysis")
    viz_col1, viz_col2 = st.columns(2)

    with viz_col1:
        st.subheader("Vendor Risk Matrix")
        if not df_filtered.empty:
            fig_heatmap = px.density_heatmap(
                df_filtered, x="RiskLikelihood", y="RiskImpact",
                color_continuous_scale="Reds",
                title="Heatmap of Vendor Risk Distribution"
            )
            st.plotly_chart(fig_heatmap, use_container_width=True)
        else:
            st.warning("No data to display based on current filters.")

    with viz_col2:
        st.subheader("ISO 27001 Compliance Status")
        if not df_filtered.empty:
            compliance_counts = df_filtered['ISO27001_Compliance'].value_counts()
            fig_donut = go.Figure(data=[go.Pie(
                labels=compliance_counts.index, values=compliance_counts.values, hole=.4,
                marker_colors=['#2ca02c', '#ff7f0e', '#d62728']
            )])
            st.plotly_chart(fig_donut, use_container_width=True)
        else:
            st.warning("No data to display based on current filters.")

    # --- DATA TABLE (NOW DYNAMIC) ---
    st.header("Filtered Vendor Details")
    with st.expander("Show Filtered Vendor Data"):
        st.dataframe(df_filtered)


# --- TAB 2: AI VENDOR ASSESSMENT ---
with tab2:
    st.header("Specialized AI Vendor Risk Analysis")
    st.markdown("This view focuses exclusively on vendors providing AI services, assessing them against emerging threats like those in the **OWASP Top 10 for LLMs**.")

    # Filter data for AI vendors only
    df_ai = df_filtered[df_filtered['Is_AI_Vendor']].copy() # Use the already filtered dataframe

    if df_ai.empty:
        st.warning("No AI vendors found with the current filter settings.")
    else:
        # Metrics for AI Vendors
        ai_col1, ai_col2 = st.columns(2)
        with ai_col1:
            st.metric(label="Total AI Vendors Selected", value=len(df_ai))
        with ai_col2:
            vulnerable_ai_vendors = len(df_ai[df_ai['OWASP_LLM_Check'].str.contains("Vulnerable")])
            st.metric(label="AI Vendors with Vulnerabilities", value=vulnerable_ai_vendors)

        st.markdown("---")

        # Chart for OWASP LLM Checks
        st.subheader("OWASP LLM Risk Breakdown")
        
        # Clean up the OWASP data for charting
        df_ai['OWASP_Risk_Type'] = df_ai['OWASP_LLM_Check'].apply(lambda x: x.split(':')[0])
        owasp_counts = df_ai['OWASP_Risk_Type'].value_counts()
        
        fig_bar = px.bar(
            x=owasp_counts.index,
            y=owasp_counts.values,
            title="Count of Top OWASP LLM Risks Identified",
            labels={'x': 'OWASP Risk Type', 'y': 'Number of Vendors'}
        )
        st.plotly_chart(fig_bar, use_container_width=True)

        # Data Table for AI Vendors
        st.subheader("AI Vendor Details")
        st.dataframe(df_ai[['VendorName', 'ServiceType', 'OverallRiskScore', 'BreachLikelihoodScore', 'OWASP_LLM_Check']])