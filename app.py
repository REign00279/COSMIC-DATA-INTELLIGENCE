
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Cosmic Data Intelligence",
    page_icon="🪐",
    layout="wide"
)

st.title("🪐 COSMIC DATA INTELLIGENCE")
st.subheader("Interactive Exoplanet Analytics")
st.caption(
    "Explore confirmed exoplanets, their discovery methods, "
    "host stars, and available measurements."
)

@st.cache_data
def load_data():
    df = pd.read_csv("exoplanet_dashboard_data.csv")

    df["discovery_method"] = (
        df["discovery_method"].fillna("Unknown").astype(str)
    )
    df["host_star_name"] = (
        df["host_star_name"].fillna("Unknown").astype(str)
    )
    df["planet_name"] = (
        df["planet_name"].fillna("Unknown").astype(str)
    )

    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error(
        "The file exoplanet_dashboard_data.csv is missing. "
        "Please upload it to the same GitHub repository as app.py."
    )
    st.stop()

# Sidebar filters
st.sidebar.header("🔎 Explore the data")

methods = sorted(df["discovery_method"].dropna().unique().tolist())
selected_methods = st.sidebar.multiselect(
    "Discovery method",
    methods,
    default=methods
)

years = pd.to_numeric(df["discovery_year"], errors="coerce")
valid_years = years.dropna()

if not valid_years.empty:
    min_year = int(valid_years.min())
    max_year = int(valid_years.max())

    selected_years = st.sidebar.slider(
        "Discovery year",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year)
    )
else:
    selected_years = None

filtered = df[df["discovery_method"].isin(selected_methods)].copy()

if selected_years is not None:
    filtered_years = pd.to_numeric(
        filtered["discovery_year"], errors="coerce"
    )
    filtered = filtered[
        filtered_years.between(
            selected_years[0], selected_years[1]
        )
    ]

# Key metrics
st.markdown("### 📊 Catalogue Overview")

c1, c2, c3 = st.columns(3)

c1.metric("Planets in selection", f"{len(filtered):,}")
c2.metric(
    "Host stars",
    f"{filtered['host_star_name'].nunique():,}"
)
c3.metric(
    "Discovery methods",
    f"{filtered['discovery_method'].nunique():,}"
)

st.info(
    "This dashboard uses a selected sample of 5,000 catalogue "
    "records, not the complete history of all exoplanet discoveries."
)

# Charts
left, right = st.columns(2)

with left:
    st.markdown("### Discovery Methods")

    method_counts = (
        filtered["discovery_method"]
        .value_counts()
        .rename_axis("Discovery Method")
        .reset_index(name="Planets")
    )

    if not method_counts.empty:
        fig_method = px.bar(
            method_counts,
            x="Discovery Method",
            y="Planets",
            color="Planets",
            title="Planets by Discovery Method"
        )
        fig_method.update_layout(xaxis_tickangle=-35)
        st.plotly_chart(fig_method, use_container_width=True)
    else:
        st.warning("No records match the selected filters.")

with right:
    st.markdown("### Discoveries by Year")

    yearly = filtered.copy()
    yearly["discovery_year"] = pd.to_numeric(
        yearly["discovery_year"], errors="coerce"
    )
    yearly = (
        yearly.dropna(subset=["discovery_year"])
        .groupby("discovery_year")
        .size()
        .reset_index(name="Planets")
        .sort_values("discovery_year")
    )

    if not yearly.empty:
        fig_year = px.line(
            yearly,
            x="discovery_year",
            y="Planets",
            markers=True,
            title="Records by Discovery Year in This Sample"
        )
        st.plotly_chart(fig_year, use_container_width=True)

# Planet radius categories
st.markdown("### 🪐 Planet Radius Categories")

if "radius_category" in filtered.columns:
    radius_counts = (
        filtered["radius_category"]
        .fillna("Unknown")
        .value_counts()
        .rename_axis("Radius Category")
        .reset_index(name="Planets")
    )

    fig_radius = px.pie(
        radius_counts,
        names="Radius Category",
        values="Planets",
        hole=0.45,
        title="Distribution of Recorded Radius Categories"
    )
    st.plotly_chart(fig_radius, use_container_width=True)

# Data explorer
st.markdown("### 🔭 Planet Explorer")

search = st.text_input(
    "Search by planet or host-star name",
    placeholder="e.g. Kepler"
)

explorer = filtered.copy()

if search.strip():
    planet_match = explorer["planet_name"].str.contains(
        search, case=False, na=False
    )
    star_match = explorer["host_star_name"].str.contains(
        search, case=False, na=False
    )
    explorer = explorer[planet_match | star_match]

preferred_columns = [
    "planet_name",
    "host_star_name",
    "discovery_method",
    "discovery_year",
    "planet_radius_earth",
    "planet_mass_earth",
    "orbital_period_days",
    "radius_category"
]

display_columns = [
    col for col in preferred_columns if col in explorer.columns
]

st.dataframe(
    explorer[display_columns],
    use_container_width=True,
    hide_index=True
)

st.caption(
    "Data source: NASA Exoplanet Archive. "
    "Missing measurements are left blank rather than treated as zero."
)
