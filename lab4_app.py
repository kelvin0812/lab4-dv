import streamlit as st
import pandas as pd
import altair as alt

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Lab 4 – Data Visualization",
    page_icon="📊",
    layout="wide",
)

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Main background */
    .stApp { background-color: #0f1117; }

    /* Section cards */
    .section-card {
        background: #1a1d27;
        border: 1px solid #2e3144;
        border-radius: 12px;
        padding: 1.5rem 2rem;
        margin-bottom: 2rem;
    }

    /* Section label pill */
    .pill {
        display: inline-block;
        padding: 0.2rem 0.8rem;
        border-radius: 999px;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }
    .pill-blue  { background:#1e3a5f; color:#60a5fa; }
    .pill-green { background:#14532d; color:#4ade80; }
    .pill-purple{ background:#3b1f6e; color:#c084fc; }
    .pill-orange{ background:#431407; color:#fb923c; }

    /* Insight box */
    .insight {
        background: #12151f;
        border-left: 3px solid #3b82f6;
        border-radius: 0 8px 8px 0;
        padding: 0.75rem 1rem;
        color: #94a3b8;
        font-size: 0.88rem;
        margin-top: 0.75rem;
    }

    /* Metric cards row */
    .metric-row { display:flex; gap:1rem; margin-bottom:2rem; }
    .metric-card {
        flex:1;
        background:#1a1d27;
        border:1px solid #2e3144;
        border-radius:10px;
        padding:1rem 1.25rem;
        text-align:center;
    }
    .metric-value { font-size:1.6rem; font-weight:700; color:#f1f5f9; }
    .metric-label { font-size:0.75rem; color:#64748b; text-transform:uppercase; letter-spacing:0.06em; }

    h1 { color: #f1f5f9 !important; }
    h2, h3 { color: #e2e8f0 !important; }
    p, li { color: #94a3b8 !important; }

    footer { display:none; }
</style>
""", unsafe_allow_html=True)

# ── Data ─────────────────────────────────────────────────────────────────────
data = {
    'Age':        [23, 35, 44, 55, 31, 45, 36, 22, 32, 27, 33, 44],
    'Income':     [35000, 88000, 60000, 80000, 37000, 75000, 54000,
                   29000, 82000, 36000, 61000, 63000],
    'Education':  ['High School','Bachelors','Masters','PhD','High School','Masters',
                   'Bachelors','High School','Bachelors','High School','Bachelors','Masters'],
    'Occupation': ['Salesman','Doctor','Artist','Scientist','Teacher','Engineer',
                   'Artist','Clerk','Doctor','Teacher','Engineer','Scientist']
}
df = pd.DataFrame(data)

# Altair base theme overrides (dark)
CHART_CONFIG = {"background": "#1a1d27", "view": {"stroke": "transparent"}}

# ── Header ───────────────────────────────────────────────────────────────────
st.markdown("## 📊 TFB3133 / TEB3133 — Data Visualization")
st.markdown("### Lab 4: Exploratory vs Presentation Graphics with Streamlit & Altair")
st.markdown("---")

# ── Dataset summary metrics ───────────────────────────────────────────────────
avg_income = f"RM {int(df['Income'].mean()):,}"
age_range  = f"{df['Age'].min()} – {df['Age'].max()}"
top_edu    = df['Education'].value_counts().idxmax()
num_occ    = df['Occupation'].nunique()

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("👥 Respondents", len(df))
with col2:
    st.metric("💰 Avg Income", avg_income)
with col3:
    st.metric("🎂 Age Range", age_range)
with col4:
    st.metric("💼 Occupations", num_occ)

st.markdown("---")

# ── 1. Exploratory Scatter Plot ───────────────────────────────────────────────
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<span class="pill pill-blue">Exploratory</span>', unsafe_allow_html=True)
st.markdown("#### 1 · Interactive Scatter Plot — Age vs Income")

scatter = (
    alt.Chart(df)
    .mark_circle(size=90, opacity=0.85)
    .encode(
        x=alt.X('Age', scale=alt.Scale(zero=False),
                axis=alt.Axis(grid=False, labelColor="#94a3b8", titleColor="#94a3b8")),
        y=alt.Y('Income', axis=alt.Axis(format='$,.0f', grid=True,
                gridColor="#2e3144", labelColor="#94a3b8", titleColor="#94a3b8")),
        color=alt.Color('Education', legend=alt.Legend(
            labelColor="#94a3b8", titleColor="#94a3b8")),
        tooltip=[
            alt.Tooltip('Age'),
            alt.Tooltip('Income', format='$,.0f'),
            alt.Tooltip('Education'),
            alt.Tooltip('Occupation'),
        ]
    )
    .properties(height=380)
    .configure(**CHART_CONFIG)
    .interactive()
)

st.altair_chart(scatter, use_container_width=True)
st.markdown(
    '<div class="insight">💡 Hover over any point to inspect the individual\'s age, income, '
    'education level and occupation. Higher education levels tend to cluster at higher income ranges.</div>',
    unsafe_allow_html=True
)
st.markdown('</div>', unsafe_allow_html=True)

# ── 2. Presentation Bar Chart ────────────────────────────────────────────────
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<span class="pill pill-green">Presentation</span>', unsafe_allow_html=True)
st.markdown("#### 2 · Static Bar Chart — Total Income by Education Level")

bar = (
    alt.Chart(df)
    .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
    .encode(
        x=alt.X('Education', sort='-y',
                axis=alt.Axis(labelColor="#94a3b8", titleColor="#94a3b8")),
        y=alt.Y('sum(Income)', title='Total Income',
                axis=alt.Axis(format='$,.0f', grid=True, gridColor="#2e3144",
                              labelColor="#94a3b8", titleColor="#94a3b8")),
        color=alt.Color('Education', legend=None),
        tooltip=[
            alt.Tooltip('Education'),
            alt.Tooltip('sum(Income)', title='Total Income', format='$,.0f'),
        ]
    )
    .properties(height=360)
    .configure(**CHART_CONFIG)
)

st.altair_chart(bar, use_container_width=True)
st.markdown(
    '<div class="insight">💡 Bachelor\'s degree holders contribute the highest combined income '
    'in this dataset. This static chart is designed for reporting — clear message, no interaction needed.</div>',
    unsafe_allow_html=True
)
st.markdown('</div>', unsafe_allow_html=True)

# ── 3. Linked Highlighting ───────────────────────────────────────────────────
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<span class="pill pill-purple">Linked</span>', unsafe_allow_html=True)
st.markdown("#### 3 · Linked Highlighting — Scatter + Bar (hover to link)")

highlight = alt.selection_single(on='mouseover', fields=['Education'], nearest=True)

scatter_linked = (
    alt.Chart(df)
    .mark_circle(size=90, opacity=0.85)
    .encode(
        x=alt.X('Age', scale=alt.Scale(zero=False),
                axis=alt.Axis(grid=False, labelColor="#94a3b8", titleColor="#94a3b8")),
        y=alt.Y('Income', axis=alt.Axis(format='$,.0f', grid=True,
                gridColor="#2e3144", labelColor="#94a3b8", titleColor="#94a3b8")),
        color=alt.condition(highlight, alt.Color('Education',
                legend=alt.Legend(labelColor="#94a3b8", titleColor="#94a3b8")),
                alt.value('#2e3144')),
        tooltip=[
            alt.Tooltip('Age'),
            alt.Tooltip('Income', format='$,.0f'),
            alt.Tooltip('Education'),
            alt.Tooltip('Occupation'),
        ]
    )
    .add_selection(highlight)
    .properties(height=340, title=alt.TitleParams(
        "Scatter: Age vs Income", color="#94a3b8"))
)

bar_linked = (
    alt.Chart(df)
    .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
    .encode(
        x=alt.X('Education', sort='-y',
                axis=alt.Axis(labelColor="#94a3b8", titleColor="#94a3b8")),
        y=alt.Y('sum(Income)', title='Total Income',
                axis=alt.Axis(format='$,.0f', grid=True, gridColor="#2e3144",
                              labelColor="#94a3b8", titleColor="#94a3b8")),
        color=alt.condition(highlight, alt.Color('Education', legend=None),
                alt.value('#2e3144')),
        tooltip=[
            alt.Tooltip('Education'),
            alt.Tooltip('sum(Income)', title='Total Income', format='$,.0f'),
        ]
    )
    .properties(height=340, title=alt.TitleParams(
        "Bar: Total Income by Education", color="#94a3b8"))
)

linked = (scatter_linked | bar_linked).configure(**CHART_CONFIG)
st.altair_chart(linked, use_container_width=True)
st.markdown(
    '<div class="insight">💡 Hover over a data point or bar to cross-highlight the matching '
    'education group across both charts simultaneously — this is linked multivariate exploration.</div>',
    unsafe_allow_html=True
)
st.markdown('</div>', unsafe_allow_html=True)

# ── 4. Occupation Bar Chart ──────────────────────────────────────────────────
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<span class="pill pill-orange">Multivariate</span>', unsafe_allow_html=True)
st.markdown("#### 4 · Occupation Count — Stacked by Education Level")

occ_bar = (
    alt.Chart(df)
    .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
    .encode(
        x=alt.X('Occupation', sort='-y',
                axis=alt.Axis(labelAngle=-30, labelColor="#94a3b8", titleColor="#94a3b8")),
        y=alt.Y('count()', title='Count',
                axis=alt.Axis(grid=True, gridColor="#2e3144",
                              labelColor="#94a3b8", titleColor="#94a3b8")),
        color=alt.Color('Education', legend=alt.Legend(
            labelColor="#94a3b8", titleColor="#94a3b8")),
        tooltip=[
            alt.Tooltip('Occupation'),
            alt.Tooltip('Education'),
            alt.Tooltip('count()', title='Count'),
        ]
    )
    .properties(height=360)
    .configure(**CHART_CONFIG)
    .interactive()
)

st.altair_chart(occ_bar, use_container_width=True)
st.markdown(
    '<div class="insight">💡 Doctors and Engineers each appear twice. The stacked color shows '
    'which education level each occupation belongs to — useful for spotting education-occupation patterns.</div>',
    unsafe_allow_html=True
)
st.markdown('</div>', unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#334155; font-size:0.8rem;'>"
    "TFB3133/TEB3133 Data Visualization · Lab 4 · Sept 2026</p>",
    unsafe_allow_html=True
)
