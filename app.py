
import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="Cosmic Data Intelligence",
    page_icon="🪐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# COSMIC DESIGN SYSTEM
# --------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.stApp {
    background:
        radial-gradient(ellipse at 15% 0%, #172554 0%, transparent 38%),
        radial-gradient(ellipse at 90% 15%, #31205b 0%, transparent 32%),
        #070b18;
    color: #edf2ff;
    font-family: 'Inter', sans-serif;
}

[data-testid="stHeader"] {
    background: rgba(7, 11, 24, 0.8);
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #10172c, #0b1020);
    border-right: 1px solid #273453;
}

.block-container {
    padding-top: 2.3rem;
    padding-bottom: 3rem;
    max-width: 1500px;
}

.hero {
    padding: 28px 30px;
    border-radius: 22px;
    border: 1px solid #34466f;
    background: linear-gradient(115deg,
        rgba(19, 34, 68, 0.96),
        rgba(31, 24, 65, 0.94));
    margin-bottom: 22px;
}

.eyebrow {
    color: #67e8f9;
    font-size: 0.76rem;
    font-weight: 800;
    letter-spacing: 3px;
    text-transform: uppercase;
}

.hero h1 {
    font-size: clamp(2rem, 4vw, 3.25rem);
    font-weight: 800;
    letter-spacing: -1.8px;
    margin: 10px 0;
    color: #f8fbff;
}

.hero p {
    color: #b9c8e8;
    font-size: 1rem;
    margin-bottom: 0;
}

.section-title {
    color: #f1f5ff;
    font-size: 1.25rem;
    font-weight: 750;
    margin: 26px 0 14px;
}

.metric-card {
    background: linear-gradient(145deg, #151f38, #101629);
    border: 1px solid #2c3d60;
    border-radius: 17px;
    padding: 21px 20px;
    min-height: 132px;
    box-shadow: 0 8px 26px rgba(0,0,0,0.16);
}

.metric-label {
    color: #9aafd2;
    font-size: 0.78rem;
    font-weight: 650;
    letter-spacing: 1px;
    text-transform: uppercase;
}

.metric-value {
    color: #f6f8ff;
    font-size: clamp(1.55rem, 2.4vw, 2.15rem);
    font-weight: 800;
    margin-top: 12px;
    letter-spacing: -0.8px;
}

.metric-note {
    color: #7dd3fc;
    font-size: 0.76rem;
    margin-top: 4px;
}

.panel {
    background: rgba(16, 23, 43, 0.88);
    border: 1px solid #273653;
    border-radius: 17px;
    padding: 18px 20px;
}

.notice {
    background: rgba(8, 145, 178, 0.10);
    border: 1px solid rgba(103, 232, 249, 0.28);
    border-radius: 12px;
    padding: 13px 16px;
    color: #c5f5ff;
    margin: 16px 0 22px;
    font-size: 0.88rem;
}

div[data-testid="stDataFrame"] {
    border: 1px solid #273653;
    border-radius: 12px;
    overflow: hidden;
}

.stButton button {
    border-radius: 10px;
}

h2, h3 {
    color: #eef3ff;
}

small, .stCaption {
    color: #9aafd2;
}

hr {
    border-color: #273653;
}

@media (max-width: 768px) {
    .block-container {
        padding-top: 1rem;
    }
    .hero {
        padding: 20px;
    }
}


/* COSMIC FILTER CONTROLS */
[data-testid="stMultiSelect"] span[data-baseweb="tag"] {
    background-color: #26365f !important;
    border: 1px solid #67e8f9 !important;
    border-radius: 8px !important;
    color: #e0f2fe !important;
}

[data-testid="stMultiSelect"] span[data-baseweb="tag"] span {
    color: #e0f2fe !important;
}

[data-testid="stMultiSelect"] span[data-baseweb="tag"] svg {
    fill: #67e8f9 !important;
    color: #67e8f9 !important;
}

[data-testid="stMultiSelect"] div[data-baseweb="select"] > div {
    border-color: #34466f !important;
    border-radius: 10px !important;
}

[data-testid="stSlider"] [role="slider"] {
    background-color: #22d3ee !important;
    border-color: #22d3ee !important;
}


[data-testid="stMultiSelect"] [data-baseweb="tag"] svg {
    fill: #67e8f9 !important;
}

[data-testid="stSlider"] [role="slider"] {
    background-color: #22d3ee !important;
    border-color: #22d3ee !important;
}

[data-testid="stSlider"] [data-baseweb="slider"] > div > div {
    background-color: #22d3ee !important;
}

[data-testid="stMultiSelect"] > div > div {
    border-color: #34466f !important;
    border-radius: 10px !important;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("exoplanet_dashboard_data.csv")

    df["discovery_method"] = (
        df["discovery_method"].fillna("Unknown").astype(str)
    )
    df["planet_name"] = df["planet_name"].fillna("Unnamed planet").astype(str)
    df["host_star_name"] = df["host_star_name"].fillna("Unknown").astype(str)

    numeric_columns = [
        "discovery_year",
        "planet_radius_earth",
        "planet_mass_earth",
        "orbital_period_days"
    ]

    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "radius_category" not in df.columns:
        df["radius_category"] = "Unknown"
    else:
        df["radius_category"] = df["radius_category"].fillna("Unknown").astype(str)

    return df


try:
    data = load_data()
except Exception as exc:
    st.error("Could not load the dashboard dataset.")
    st.code(str(exc))
    st.info(
        "Check that exoplanet_dashboard_data.csv is in the same "
        "GitHub repository directory as app.py."
    )
    st.stop()

# --------------------------------------------------
# HERO HEADER
# --------------------------------------------------
st.markdown("""
<div class="hero">
    <div class="eyebrow">✦ Astronomy · Data Engineering · Discovery</div>
    <h1>🪐 COSMIC DATA INTELLIGENCE</h1>
    <p>
        Explore distant worlds, investigate discovery methods, and uncover
        patterns in the NASA Exoplanet Archive sample.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="notice">
    <b>DATA NOTE</b> &nbsp; This dashboard analyses a selected sample of
    5,000 catalogue records, not the complete exoplanet archive.
    Yearly counts and other statistics describe the displayed sample.
    Blank measurements mean the value is unavailable, not zero.
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------
st.sidebar.markdown("## 🛰️ Mission controls")
st.sidebar.caption("Configure your exploration")

methods = sorted(data["discovery_method"].unique().tolist())
selected_methods = st.sidebar.multiselect(
    "Discovery method",
    options=methods,
    default=methods
)

year_values = data["discovery_year"].dropna()
filtered = data.copy()

if not year_values.empty:
    min_year = int(year_values.min())
    max_year = int(year_values.max())

    if min_year < max_year:
        year_range = st.sidebar.slider(
            "Discovery year",
            min_value=min_year,
            max_value=max_year,
            value=(min_year, max_year)
        )
        filtered = filtered[
            filtered["discovery_year"].between(
                year_range[0], year_range[1]
            ) | filtered["discovery_year"].isna()
        ]

filtered = filtered[
    filtered["discovery_method"].isin(selected_methods)
]

st.sidebar.divider()
st.sidebar.markdown("### 📡 Dataset status")
st.sidebar.metric("Records in view", f"{len(filtered):,}")
st.sidebar.caption("Source: NASA Exoplanet Archive")
st.sidebar.caption("Refreshes when the repository data updates.")

# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------
st.markdown('<div class="section-title">01 — Mission overview</div>',
            unsafe_allow_html=True)

k1, k2, k3, k4 = st.columns(4)

unique_planets = (
    filtered["planet_name"].nunique()
    if not filtered.empty else 0
)
unique_stars = (
    filtered["host_star_name"].nunique()
    if not filtered.empty else 0
)
unique_methods = (
    filtered["discovery_method"].nunique()
    if not filtered.empty else 0
)

radius_count = (
    filtered["planet_radius_earth"].notna().sum()
    if not filtered.empty else 0
)

def metric_card(container, label, value, note):
    container.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

metric_card(k1, "Planets in view", f"{unique_planets:,}", "Catalogue records")
metric_card(k2, "Host stars", f"{unique_stars:,}", "Distinct host names")
metric_card(k3, "Discovery methods", f"{unique_methods:,}", "Methods represented")
metric_card(k4, "Radius available", f"{radius_count:,}", "Records with measurements")

st.caption(
    f"Showing {len(filtered):,} of {len(data):,} records in the selected sample."
)

# --------------------------------------------------
# CHARTS
# --------------------------------------------------
st.markdown('<div class="section-title">02 — Discovery analytics</div>',
            unsafe_allow_html=True)

chart_left, chart_right = st.columns(2)

chart_template = "plotly_dark"
chart_background = "rgba(0,0,0,0)"
grid_color = "#263451"

with chart_left:
    st.markdown("#### 🔭 Discovery methods")
    if filtered.empty:
        st.info("No records match the current filters.")
    else:
        method_counts = (
            filtered["discovery_method"]
            .value_counts()
            .rename_axis("Method")
            .reset_index(name="Records")
            .sort_values("Records", ascending=True)
            .tail(12)
        )

        fig_method = px.bar(
            method_counts,
            x="Records",
            y="Method",
            orientation="h",
            color="Records",
            color_continuous_scale=["#4338ca", "#22d3ee"],
            template=chart_template
        )
        fig_method.update_layout(
            height=420,
            margin=dict(l=5, r=5, t=15, b=5),
            paper_bgcolor=chart_background,
            plot_bgcolor=chart_background,
            coloraxis_showscale=False,
            xaxis_title="Records in selected sample",
            yaxis_title="",
            font=dict(color="#dbeafe"),
            xaxis=dict(gridcolor=grid_color),
            yaxis=dict(gridcolor=grid_color)
        )
        st.plotly_chart(fig_method, use_container_width=True)

with chart_right:
    st.markdown("#### 📈 Records by discovery year")
    yearly = filtered.dropna(subset=["discovery_year"]).copy()

    if yearly.empty:
        st.info("No dated records match the current filters.")
    else:
        yearly["discovery_year"] = yearly["discovery_year"].astype(int)
        yearly_counts = (
            yearly.groupby("discovery_year")
            .size()
            .reset_index(name="Records")
            .sort_values("discovery_year")
        )

        fig_year = px.line(
            yearly_counts,
            x="discovery_year",
            y="Records",
            markers=True,
            template=chart_template
        )
        fig_year.update_traces(
            line=dict(color="#22d3ee", width=3),
            marker=dict(color="#a78bfa", size=7)
        )
        fig_year.update_layout(
            height=420,
            margin=dict(l=5, r=5, t=15, b=5),
            paper_bgcolor=chart_background,
            plot_bgcolor=chart_background,
            xaxis_title="Discovery year",
            yaxis_title="Records in selected sample",
            font=dict(color="#dbeafe"),
            xaxis=dict(gridcolor=grid_color),
            yaxis=dict(gridcolor=grid_color)
        )
        st.plotly_chart(fig_year, use_container_width=True)

# --------------------------------------------------
# PLANET RADIUS DISTRIBUTION
# --------------------------------------------------
st.markdown('<div class="section-title">03 — Planet characteristics</div>',
            unsafe_allow_html=True)

radius_left, radius_right = st.columns([1, 1])

with radius_left:
    st.markdown("#### 🪐 Radius categories")

    radius_data = filtered.copy()
    radius_data["radius_category"] = radius_data["radius_category"].replace(
        "", "Unknown"
    )
    radius_counts = (
        radius_data["radius_category"]
        .value_counts()
        .rename_axis("Category")
        .reset_index(name="Records")
    )

    if radius_counts.empty:
        st.info("No radius categories are available.")
    else:
        fig_radius = px.pie(
            radius_counts,
            names="Category",
            values="Records",
            hole=0.62,
            template=chart_template,
            color_discrete_sequence=[
                "#22d3ee", "#818cf8", "#c084fc",
                "#f472b6", "#38bdf8", "#64748b"
            ]
        )
        fig_radius.update_layout(
            height=350,
            margin=dict(l=5, r=5, t=10, b=5),
            paper_bgcolor=chart_background,
            font=dict(color="#dbeafe"),
            legend_title_text=""
        )
        st.plotly_chart(fig_radius, use_container_width=True)

with radius_right:
    st.markdown("#### 🧪 Measurement availability")

    quality_rows = []
    for col, label in [
        ("planet_radius_earth", "Planet radius"),
        ("planet_mass_earth", "Planet mass"),
        ("orbital_period_days", "Orbital period")
    ]:
        available = int(filtered[col].notna().sum()) if col in filtered else 0
        total = len(filtered)
        quality_rows.append({
            "Measurement": label,
            "Available": available,
            "Missing": total - available,
            "Available (%)": round(available / total * 100, 1)
            if total else 0
        })

    quality = pd.DataFrame(quality_rows)
    if not quality.empty:
        fig_quality = px.bar(
            quality,
            x="Measurement",
            y="Available (%)",
            color="Measurement",
            range_y=[0, 100],
            template=chart_template,
            color_discrete_sequence=["#22d3ee", "#818cf8", "#c084fc"]
        )
        fig_quality.update_layout(
            height=350,
            margin=dict(l=5, r=5, t=10, b=5),
            paper_bgcolor=chart_background,
            plot_bgcolor=chart_background,
            showlegend=False,
            yaxis_title="Records with data (%)",
            xaxis_title="",
            font=dict(color="#dbeafe"),
            yaxis=dict(gridcolor=grid_color)
        )
        st.plotly_chart(fig_quality, use_container_width=True)
        st.dataframe(quality, hide_index=True, use_container_width=True)

# --------------------------------------------------
# SEARCHABLE PLANET EXPLORER
# --------------------------------------------------
st.markdown('<div class="section-title">04 — Planet explorer</div>',
            unsafe_allow_html=True)
st.caption("Search the catalogue and inspect individual planet measurements.")

search_text = st.text_input(
    "🔎 Search planets or host stars",
    placeholder="Try a planet name, host star, or discovery method..."
)

explorer = filtered.copy()

if search_text.strip():
    term = search_text.strip()
    match = (
        explorer["planet_name"].str.contains(term, case=False, na=False)
        | explorer["host_star_name"].str.contains(term, case=False, na=False)
        | explorer["discovery_method"].str.contains(term, case=False, na=False)
    )
    explorer = explorer[match]

display_columns = [
    "planet_name",
    "host_star_name",
    "discovery_method",
    "discovery_year",
    "planet_radius_earth",
    "planet_mass_earth",
    "orbital_period_days",
    "radius_category"
]
display_columns = [c for c in display_columns if c in explorer.columns]

st.markdown(
    f'<div class="notice">Catalogue results: <b>{len(explorer):,}</b></div>',
    unsafe_allow_html=True
)

st.dataframe(
    explorer[display_columns],
    use_container_width=True,
    hide_index=True,
    height=420
)

csv_data = explorer[display_columns].to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Download filtered catalogue as CSV",
    data=csv_data,
    file_name="cosmic_planet_explorer.csv",
    mime="text/csv"
)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.divider()
st.markdown("""
<div style="text-align:center; padding: 12px 0 4px;">
    <div style="color:#67e8f9; font-weight:800; letter-spacing:2px;">
        COSMIC DATA INTELLIGENCE
    </div>
    <div style="color:#91a4c7; font-size:0.82rem; margin-top:8px;">
        Built with Python · Pandas · Plotly · Streamlit
    </div>
    <div style="color:#64748b; font-size:0.78rem; margin-top:5px;">
        Data source: NASA Exoplanet Archive · Selected catalogue sample
    </div>
</div>
""", unsafe_allow_html=True)

