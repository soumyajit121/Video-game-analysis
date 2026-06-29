import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# ═══════════════════════════════════════════════════════════════
# 1. PAGE CONFIG
# ═══════════════════════════════════════════════════════════════
st.set_page_config(page_title="🎮 Game Insights", layout="wide", initial_sidebar_state="expanded")

# ═══════════════════════════════════════════════════════════════
# 2. GLOBAL CSS — Animated Gradient + Glassmorphism
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<style>
/* ── Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Inter:wght@300;400;500;600&display=swap');

/* ── Animated gradient background ── */
@keyframes gradientShift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.stApp {
    background: linear-gradient(
        135deg,
        #0a0a1a 0%,
        #0d1b3e 15%,
        #1a0a2e 30%,
        #0d2137 45%,
        #0a1628 60%,
        #1e0a3c 75%,
        #0a1a2e 90%,
        #0a0a1a 100%
    );
    background-size: 400% 400%;
    animation: gradientShift 12s ease infinite;
    font-family: 'Inter', sans-serif;
}

/* ── Sidebar glassmorphism ── */
[data-testid="stSidebar"] {
    background: rgba(10, 10, 40, 0.55) !important;
    backdrop-filter: blur(20px) saturate(180%) !important;
    -webkit-backdrop-filter: blur(20px) saturate(180%) !important;
    border-right: 1px solid rgba(120, 100, 255, 0.25) !important;
    box-shadow: 4px 0 24px rgba(100, 80, 255, 0.12) !important;
}

[data-testid="stSidebar"] * {
    color: #e0d8ff !important;
}

[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label,
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] h1, h2, h3 {
    color: #c4b8ff !important;
    font-weight: 600 !important;
}

/* ── Main header ── */
.main-header {
    background: rgba(255, 255, 255, 0.04);
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    border: 1px solid rgba(160, 130, 255, 0.2);
    border-radius: 20px;
    padding: 32px 40px 24px 40px;
    margin-bottom: 28px;
    text-align: center;
    box-shadow: 0 8px 40px rgba(100, 60, 255, 0.18), inset 0 1px 0 rgba(255,255,255,0.08);
    position: relative;
    overflow: hidden;
}

.main-header::before {
    content: '';
    position: absolute;
    top: -60%;
    left: -30%;
    width: 60%;
    height: 200%;
    background: radial-gradient(ellipse, rgba(120, 80, 255, 0.12) 0%, transparent 70%);
    pointer-events: none;
}

.main-header h1 {
    font-family: 'Orbitron', monospace !important;
    font-size: 2.6rem !important;
    font-weight: 900 !important;
    background: linear-gradient(90deg, #a78bfa, #60a5fa, #f472b6, #a78bfa);
    background-size: 300% 100%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: gradientShift 5s ease infinite;
    margin: 0 !important;
    letter-spacing: 3px;
    text-transform: uppercase;
}

.main-header p {
    color: rgba(196, 184, 255, 0.75);
    font-size: 0.95rem;
    margin-top: 8px;
    letter-spacing: 1px;
}

/* ── Glass card (metric & content blocks) ── */
.glass-card {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(160, 130, 255, 0.2);
    border-radius: 16px;
    padding: 24px 28px;
    margin-bottom: 20px;
    box-shadow: 0 4px 24px rgba(80, 60, 180, 0.14), inset 0 1px 0 rgba(255,255,255,0.06);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.glass-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 32px rgba(120, 80, 255, 0.22), inset 0 1px 0 rgba(255,255,255,0.08);
}

/* ── KPI metric cards ── */
.metric-glass {
    background: rgba(255, 255, 255, 0.06);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    border: 1px solid rgba(160, 130, 255, 0.22);
    border-radius: 16px;
    padding: 22px 20px 18px 20px;
    text-align: center;
    box-shadow: 0 4px 20px rgba(80, 60, 200, 0.16), inset 0 1px 0 rgba(255,255,255,0.07);
    margin-bottom: 16px;
    position: relative;
    overflow: hidden;
}

.metric-glass::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #a78bfa, #60a5fa, #f472b6);
    border-radius: 16px 16px 0 0;
}

.metric-glass .metric-value {
    font-family: 'Orbitron', monospace;
    font-size: 1.85rem;
    font-weight: 700;
    background: linear-gradient(135deg, #a78bfa, #60a5fa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.2;
}

.metric-glass .metric-label {
    font-size: 0.75rem;
    color: rgba(196, 184, 255, 0.65);
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-top: 6px;
    font-weight: 500;
}

.metric-glass .metric-icon {
    font-size: 1.5rem;
    margin-bottom: 8px;
    display: block;
}

/* ── Section subheaders ── */
.section-title {
    font-family: 'Orbitron', monospace;
    font-size: 1.05rem;
    font-weight: 700;
    color: #a78bfa;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin: 28px 0 14px 0;
    padding-left: 14px;
    border-left: 3px solid #a78bfa;
}

/* ── Summary insight cards ── */
.insight-card {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    border: 1px solid rgba(160, 130, 255, 0.18);
    border-radius: 14px;
    padding: 20px 22px;
    margin-bottom: 14px;
    box-shadow: 0 2px 16px rgba(80, 60, 180, 0.10);
    position: relative;
}

.insight-card .insight-label {
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: #f472b6;
    font-weight: 600;
    margin-bottom: 6px;
}

.insight-card .insight-value {
    font-family: 'Orbitron', monospace;
    font-size: 1.4rem;
    font-weight: 700;
    color: #e0d8ff;
    margin-bottom: 4px;
}

.insight-card .insight-desc {
    font-size: 0.8rem;
    color: rgba(196, 184, 255, 0.6);
}

/* ── Divider ── */
.fancy-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(167, 139, 250, 0.4), rgba(96, 165, 250, 0.4), transparent);
    margin: 28px 0;
    border: none;
}

/* ── Streamlit native component overrides ── */
[data-testid="stMetric"] {
    background: rgba(255, 255, 255, 0.05) !important;
    backdrop-filter: blur(14px) !important;
    border: 1px solid rgba(160, 130, 255, 0.2) !important;
    border-radius: 14px !important;
    padding: 16px !important;
}

[data-testid="stMetricLabel"] {
    color: rgba(196, 184, 255, 0.7) !important;
    font-size: 0.75rem !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
}

[data-testid="stMetricValue"] {
    color: #a78bfa !important;
    font-family: 'Orbitron', monospace !important;
    font-weight: 700 !important;
}

/* ── Tab bar ── */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.04) !important;
    backdrop-filter: blur(16px) !important;
    border-radius: 14px !important;
    border: 1px solid rgba(160, 130, 255, 0.18) !important;
    padding: 6px !important;
    gap: 4px !important;
}

[data-testid="stTabs"] [data-baseweb="tab"] {
    background: transparent !important;
    color: rgba(196, 184, 255, 0.65) !important;
    border-radius: 10px !important;
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    padding: 8px 14px !important;
    border: none !important;
    transition: all 0.2s ease !important;
}

[data-testid="stTabs"] [data-baseweb="tab"]:hover {
    background: rgba(167, 139, 250, 0.12) !important;
    color: #e0d8ff !important;
}

[data-testid="stTabs"] [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(167, 139, 250, 0.28), rgba(96, 165, 250, 0.18)) !important;
    color: #ffffff !important;
    box-shadow: 0 2px 12px rgba(167, 139, 250, 0.25) !important;
    border: 1px solid rgba(167, 139, 250, 0.3) !important;
}

/* ── Plotly chart containers ── */
[data-testid="stPlotlyChart"] {
    background: rgba(255,255,255,0.04) !important;
    backdrop-filter: blur(14px) !important;
    border: 1px solid rgba(160, 130, 255, 0.14) !important;
    border-radius: 16px !important;
    padding: 12px !important;
    box-shadow: 0 4px 20px rgba(80, 60, 180, 0.10) !important;
    margin-bottom: 16px !important;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    background: rgba(255,255,255,0.03) !important;
    backdrop-filter: blur(14px) !important;
    border: 1px solid rgba(160, 130, 255, 0.15) !important;
    border-radius: 14px !important;
}

/* ── Multiselect / Slider labels ── */
.stMultiSelect label, .stSlider label, .stSelectbox label {
    color: #c4b8ff !important;
    font-weight: 500 !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.5px !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: rgba(10,10,30,0.4); }
::-webkit-scrollbar-thumb { background: rgba(167, 139, 250, 0.35); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: rgba(167, 139, 250, 0.6); }

/* ── Badge pills ── */
.badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 99px;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.5px;
    background: rgba(167, 139, 250, 0.18);
    color: #c4b8ff;
    border: 1px solid rgba(167, 139, 250, 0.3);
    margin-right: 6px;
}

/* ── Glowing pulse dot ── */
@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%       { opacity: 0.6; transform: scale(1.3); }
}
.pulse-dot {
    display: inline-block;
    width: 8px; height: 8px;
    border-radius: 50%;
    background: #a78bfa;
    animation: pulse 2s ease-in-out infinite;
    margin-right: 8px;
    box-shadow: 0 0 8px #a78bfa;
}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# 3. PLOTLY DARK GLASS THEME HELPER
# ═══════════════════════════════════════════════════════════════
def glass_layout(fig, title=""):
    fig.update_layout(
        title=dict(text=title, font=dict(color="#c4b8ff", size=15, family="Inter"), x=0.01),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.03)",
        font=dict(color="#c4b8ff", family="Inter"),
        legend=dict(
            bgcolor="rgba(255,255,255,0.05)",
            bordercolor="rgba(167,139,250,0.2)",
            borderwidth=1,
            font=dict(color="#c4b8ff", size=11),
        ),
        xaxis=dict(
            gridcolor="rgba(167,139,250,0.1)",
            zerolinecolor="rgba(167,139,250,0.15)",
            tickfont=dict(color="#9988cc"),
        ),
        yaxis=dict(
            gridcolor="rgba(167,139,250,0.1)",
            zerolinecolor="rgba(167,139,250,0.15)",
            tickfont=dict(color="#9988cc"),
        ),
        margin=dict(l=16, r=16, t=44, b=16),
    )
    return fig

PALETTE = px.colors.qualitative.Pastel
SEQUENTIAL = "Purples"
ACCENT_SEQ = [[0, "#1a1040"], [0.5, "#6d28d9"], [1, "#a78bfa"]]

# ═══════════════════════════════════════════════════════════════
# 4. DATA
# ═══════════════════════════════════════════════════════════════
@st.cache_data
def load_data():
    df = pd.read_csv("video_game.csv")
    for col in ["critic_score", "total_sales", "na_sales", "jp_sales", "pal_sales", "other_sales"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
    for col in ["genre", "publisher", "developer", "console", "title"]:
        df[col] = df[col].fillna("Unknown")
    df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")
    df["last_update"] = pd.to_datetime(df["last_update"], errors="coerce")
    df["release_year"] = df["release_date"].dt.year
    df["release_month"] = df["release_date"].dt.month
    df["release_quarter"] = df["release_date"].dt.quarter
    df["update_gap_days"] = (df["last_update"] - df["release_date"]).dt.days
    df["decade"] = (df["release_year"] // 10 * 10).astype("Int64").astype(str) + "s"
    return df

df = load_data()

# ═══════════════════════════════════════════════════════════════
# 5. HEADER
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<div class="main-header">
    <h1>🎮 Video Game Insights</h1>
    <p>Interactive intelligence dashboard · Sales · Scores · Trends · Platforms</p>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# 6. SIDEBAR
# ═══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 10px 0 20px 0;'>
        <span style='font-family:Orbitron,monospace; font-size:1.05rem;
                     font-weight:700; color:#a78bfa; letter-spacing:2px;'>
            ⚙ FILTERS
        </span>
    </div>
    """, unsafe_allow_html=True)

    selected_genres = st.multiselect("🎭 Genre", options=sorted(df["genre"].unique()))
    selected_consoles = st.multiselect("🕹️ Console", options=sorted(df["console"].unique()))
    selected_publishers = st.multiselect("🏢 Publisher", options=sorted(df["publisher"].unique()))
    selected_devs = st.multiselect("👨‍💻 Developer", options=sorted(df["developer"].unique()))
    year_min = int(df["release_year"].dropna().min())
    year_max = int(df["release_year"].dropna().max())
    selected_years = st.slider("📅 Release Year", year_min, year_max, (year_min, year_max))

filtered_df = df.copy()
if selected_devs:      filtered_df = filtered_df[filtered_df["developer"].isin(selected_devs)]
if selected_genres:    filtered_df = filtered_df[filtered_df["genre"].isin(selected_genres)]
if selected_consoles:  filtered_df = filtered_df[filtered_df["console"].isin(selected_consoles)]
if selected_publishers:filtered_df = filtered_df[filtered_df["publisher"].isin(selected_publishers)]
filtered_df = filtered_df[
    (filtered_df["release_year"] >= selected_years[0]) &
    (filtered_df["release_year"] <= selected_years[1])
]

regions = ["na_sales", "pal_sales", "jp_sales", "other_sales"]
region_labels = {"na_sales": "North America", "pal_sales": "Europe (PAL)",
                 "jp_sales": "Japan", "other_sales": "Other"}

# ═══════════════════════════════════════════════════════════════
# 7. TABS
# ═══════════════════════════════════════════════════════════════
tab_labels = [
    "🔭 Summary", "📊 Overview", "🏆 Top Games", "🌍 Regional Sales",
    "🎭 Genre", "🕹️ Consoles", "🏢 Publishers", "⭐ Critic Scores",
    "📈 Cumulative", "🔄 Rolling", "⏳ Time"
]
tabs = st.tabs(tab_labels)

# ─────────────────────────────────────────────────────────────
# TAB 0 — SUMMARY
# ─────────────────────────────────────────────────────────────
with tabs[0]:
    valid_scores = filtered_df[filtered_df["critic_score"] > 0]
    avg_score = valid_scores["critic_score"].mean() if not valid_scores.empty else 0
    best_game_row = filtered_df.nlargest(1, "total_sales")
    best_game = best_game_row["title"].values[0] if len(best_game_row) else "N/A"
    best_sales = best_game_row["total_sales"].values[0] if len(best_game_row) else 0
    top_genre = filtered_df.groupby("genre")["total_sales"].sum().idxmax() if len(filtered_df) else "N/A"
    top_console = filtered_df.groupby("console")["total_sales"].sum().idxmax() if len(filtered_df) else "N/A"
    top_pub = filtered_df.groupby("publisher")["total_sales"].sum().idxmax() if len(filtered_df) else "N/A"
    top_dev = filtered_df.groupby("developer")["total_sales"].sum().idxmax() if len(filtered_df) else "N/A"
    total_sales = filtered_df["total_sales"].sum()

    # KPI Strip
    k1, k2, k3, k4, k5, k6, k7, k8 = st.columns(8)
    kpi_data = [
        (k1, "🎮", f"{len(filtered_df):,}", "TOTAL GAMES"),
        (k2, "💰", f"{total_sales:.0f}M", "GLOBAL SALES"),
        (k3, "⭐", f"{avg_score:.1f}", "AVG SCORE"),
        (k4, "👨‍💻", f"{filtered_df['developer'].nunique():,}", "DEVELOPERS"),
        (k5, "🏢", f"{filtered_df['publisher'].nunique():,}", "PUBLISHERS"),
        (k6, "🕹️", f"{filtered_df['console'].nunique():,}", "CONSOLES"),
        (k7, "🎭", f"{filtered_df['genre'].nunique():,}", "GENRES"),
        (k8, "📅", f"{int(filtered_df['release_year'].dropna().min()) if len(filtered_df) else 'N/A'}", "FROM YEAR"),
    ]
    for col, icon, val, label in kpi_data:
        col.markdown(f"""
        <div class="metric-glass">
            <span class="metric-icon">{icon}</span>
            <div class="metric-value">{val}</div>
            <div class="metric-label">{label}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<hr class="fancy-divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🏅 Key Highlights</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    highlights = [
        (c1, [
            ("🥇 BEST SELLING GAME", best_game, f"{best_sales:.2f}M copies sold globally"),
            ("🎭 TOP GENRE", top_genre, f"{filtered_df[filtered_df['genre']==top_genre]['total_sales'].sum():.0f}M total sales"),
            ("🕹️ TOP CONSOLE", top_console, f"{filtered_df[filtered_df['console']==top_console]['total_sales'].sum():.0f}M total sales"),
        ]),
        (c2, [
            ("🏢 TOP PUBLISHER", top_pub, f"{filtered_df[filtered_df['publisher']==top_pub]['total_sales'].sum():.0f}M total sales"),
            ("👨‍💻 TOP DEVELOPER", top_dev, f"{filtered_df[filtered_df['developer']==top_dev]['total_sales'].sum():.0f}M total sales"),
            ("⭐ HIGHEST RATED GAME", valid_scores.nlargest(1,"critic_score")["title"].values[0] if len(valid_scores) else "N/A",
             f"Score: {valid_scores['critic_score'].max():.1f}" if len(valid_scores) else ""),
        ]),
        (c3, [
            ("🌍 TOP REGION", "North America", f"{filtered_df['na_sales'].sum():.0f}M total sales"),
            ("📅 PEAK YEAR", str(int(filtered_df.groupby('release_year')['total_sales'].sum().idxmax())) if len(filtered_df) else "N/A",
             "Highest single-year sales"),
            ("🔄 LONGEST SUPPORTED", filtered_df.dropna(subset=["update_gap_days"]).nlargest(1,"update_gap_days")["title"].values[0] if not filtered_df.dropna(subset=["update_gap_days"]).empty else "N/A",
             f"{int(filtered_df.dropna(subset=['update_gap_days'])['update_gap_days'].max()):,} days of support" if not filtered_df.dropna(subset=["update_gap_days"]).empty else ""),
        ]),
    ]
    for col, items in highlights:
        with col:
            for label, value, desc in items:
                st.markdown(f"""
                <div class="insight-card">
                    <div class="insight-label">{label}</div>
                    <div class="insight-value">{value}</div>
                    <div class="insight-desc">{desc}</div>
                </div>""", unsafe_allow_html=True)

    st.markdown('<hr class="fancy-divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📈 At-a-Glance Charts</div>', unsafe_allow_html=True)

    sc1, sc2 = st.columns(2)
    with sc1:
        ys = filtered_df.groupby("release_year")["total_sales"].sum().reset_index().sort_values("release_year")
        fig = glass_layout(px.area(ys, x="release_year", y="total_sales",
            color_discrete_sequence=["#a78bfa"],
            labels={"total_sales": "Sales (M)", "release_year": "Year"}), "Yearly Sales Trend")
        fig.update_traces(fill='tozeroy', line_color="#a78bfa", fillcolor="rgba(167,139,250,0.15)")
        st.plotly_chart(fig, use_container_width=True)

    with sc2:
        gc = filtered_df["genre"].value_counts().head(7).reset_index()
        gc.columns = ["genre", "count"]
        fig = glass_layout(px.pie(gc, names="genre", values="count", hole=0.55,
            color_discrete_sequence=px.colors.qualitative.Pastel), "Genre Distribution")
        fig.update_traces(textfont_color="#e0d8ff")
        st.plotly_chart(fig, use_container_width=True)

    sc3, sc4 = st.columns(2)
    with sc3:
        rs = filtered_df[regions].sum().reset_index()
        rs.columns = ["Region", "Sales"]
        rs["Region"] = rs["Region"].map(region_labels)
        fig = glass_layout(px.bar(rs, x="Region", y="Sales",
            color="Region", color_discrete_sequence=px.colors.qualitative.Pastel,
            labels={"Sales": "Sales (M)"}), "Sales by Region")
        st.plotly_chart(fig, use_container_width=True)

    with sc4:
        tp = filtered_df.groupby("publisher")["total_sales"].sum().nlargest(7).reset_index()
        fig = glass_layout(px.bar(tp, x="total_sales", y="publisher", orientation="h",
            color="total_sales", color_continuous_scale=ACCENT_SEQ,
            labels={"total_sales": "Sales (M)", "publisher": ""}), "Top 7 Publishers")
        fig.update_layout(yaxis={"categoryorder": "total ascending"}, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)


# ─────────────────────────────────────────────────────────────
# TAB 1 — OVERVIEW
# ─────────────────────────────────────────────────────────────
with tabs[1]:
    st.markdown('<div class="section-title">📊 General Overview</div>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    valid_scores = filtered_df[filtered_df["critic_score"] > 0]
    avg_score = valid_scores["critic_score"].mean() if not valid_scores.empty else 0
    for col, icon, val, label in [
        (c1, "🎮", f"{len(filtered_df):,}", "Total Games"),
        (c2, "💰", f"{filtered_df['total_sales'].sum():.2f}M", "Global Sales"),
        (c3, "⭐", f"{avg_score:.2f}", "Avg Critic Score"),
        (c4, "👨‍💻", f"{filtered_df['developer'].nunique():,}", "Developers"),
    ]:
        col.markdown(f"""<div class="metric-glass">
            <span class="metric-icon">{icon}</span>
            <div class="metric-value">{val}</div>
            <div class="metric-label">{label}</div>
        </div>""", unsafe_allow_html=True)

    # Games per year
    st.markdown('<div class="section-title">Games Released Per Year</div>', unsafe_allow_html=True)
    yc = filtered_df.groupby("release_year").size().reset_index(name="count")
    fig = glass_layout(px.bar(yc, x="release_year", y="count",
        color="count", color_continuous_scale=ACCENT_SEQ,
        labels={"release_year": "Year", "count": "Games"}), "")
    fig.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

    cc1, cc2 = st.columns(2)
    with cc1:
        st.markdown('<div class="section-title">Sales Distribution</div>', unsafe_allow_html=True)
        fig = glass_layout(px.histogram(filtered_df[filtered_df["total_sales"]>0],
            x="total_sales", nbins=60, color_discrete_sequence=["#a78bfa"],
            labels={"total_sales": "Sales (M)"}), "")
        st.plotly_chart(fig, use_container_width=True)
    with cc2:
        st.markdown('<div class="section-title">Genre Share</div>', unsafe_allow_html=True)
        gc2 = filtered_df["genre"].value_counts().reset_index()
        gc2.columns = ["genre", "count"]
        fig = glass_layout(px.pie(gc2, names="genre", values="count", hole=0.4,
            color_discrete_sequence=PALETTE), "")
        fig.update_traces(textfont_color="#e0d8ff")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="section-title">Top 10 Developers by Game Count</div>', unsafe_allow_html=True)
    dc = filtered_df["developer"].value_counts().head(10).reset_index()
    dc.columns = ["developer", "count"]
    fig = glass_layout(px.bar(dc, x="count", y="developer", orientation="h",
        color="count", color_continuous_scale=ACCENT_SEQ,
        labels={"count": "Games", "developer": ""}), "")
    fig.update_layout(yaxis={"categoryorder": "total ascending"}, coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="section-title">Yearly Sales Trend</div>', unsafe_allow_html=True)
    ys2 = filtered_df.groupby("release_year")["total_sales"].sum().reset_index()
    fig = glass_layout(px.line(ys2, x="release_year", y="total_sales", markers=True,
        color_discrete_sequence=["#a78bfa"],
        labels={"total_sales": "Sales (M)", "release_year": "Year"}), "")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="section-title">Full Dataset</div>', unsafe_allow_html=True)
    st.dataframe(filtered_df, use_container_width=True)


# ─────────────────────────────────────────────────────────────
# TAB 2 — TOP GAMES
# ─────────────────────────────────────────────────────────────
with tabs[2]:
    st.markdown('<div class="section-title">🏆 Top Games Analysis</div>', unsafe_allow_html=True)

    top10 = filtered_df.nlargest(10, "total_sales")
    fig = glass_layout(px.bar(top10, x="title", y="total_sales", color="console",
        text="total_sales", color_discrete_sequence=PALETTE,
        labels={"total_sales": "Sales (M)", "title": ""}), "Top 10 Games by Total Sales")
    fig.update_traces(texttemplate="%{text:.1f}M", textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        top_na = filtered_df.nlargest(10, "na_sales")[["title", "na_sales", "genre"]]
        fig = glass_layout(px.bar(top_na, x="na_sales", y="title", orientation="h",
            color="genre", color_discrete_sequence=PALETTE,
            labels={"na_sales": "NA Sales (M)", "title": ""}), "Top 10 · North America")
        fig.update_layout(yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        top_jp = filtered_df.nlargest(10, "jp_sales")[["title", "jp_sales", "genre"]]
        fig = glass_layout(px.bar(top_jp, x="jp_sales", y="title", orientation="h",
            color="genre", color_discrete_sequence=PALETTE,
            labels={"jp_sales": "JP Sales (M)", "title": ""}), "Top 10 · Japan")
        fig.update_layout(yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        top_score = filtered_df[filtered_df["critic_score"]>0].nlargest(10, "critic_score")
        fig = glass_layout(px.bar(top_score, x="critic_score", y="title", orientation="h",
            color="console", color_discrete_sequence=PALETTE,
            labels={"critic_score": "Score", "title": ""}), "Top 10 Critic Rated Games")
        fig.update_layout(yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig, use_container_width=True)
    with c4:
        top_gap = filtered_df.dropna(subset=["update_gap_days"]).nlargest(10, "update_gap_days")
        fig = glass_layout(px.bar(top_gap, x="update_gap_days", y="title", orientation="h",
            color="genre", color_discrete_sequence=PALETTE,
            labels={"update_gap_days": "Days", "title": ""}), "Longest Supported Games")
        fig.update_layout(yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig, use_container_width=True)

    top50 = filtered_df.nlargest(50, "total_sales")
    fig = glass_layout(px.treemap(top50, path=["genre", "title"], values="total_sales",
        color="total_sales", color_continuous_scale=ACCENT_SEQ), "Top 50 Games Treemap")
    fig.update_traces(textfont_color="#e0d8ff")
    st.plotly_chart(fig, use_container_width=True)

    fig = glass_layout(px.scatter(filtered_df[filtered_df["total_sales"]>0],
        x="release_year", y="total_sales", color="genre", hover_name="title", size="total_sales",
        size_max=30, color_discrete_sequence=PALETTE,
        labels={"total_sales": "Sales (M)", "release_year": "Year"}),
        "Sales Bubble Chart by Year")
    st.plotly_chart(fig, use_container_width=True)


# ─────────────────────────────────────────────────────────────
# TAB 3 — REGIONAL SALES
# ─────────────────────────────────────────────────────────────
with tabs[3]:
    st.markdown('<div class="section-title">🌍 Regional Sales Analysis</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        rs = filtered_df[regions].sum().reset_index()
        rs.columns = ["Region", "Sales"]
        rs["Region"] = rs["Region"].map(region_labels)
        fig = glass_layout(px.pie(rs, names="Region", values="Sales", hole=0.45,
            color_discrete_sequence=PALETTE), "Global Sales Distribution")
        fig.update_traces(textfont_color="#e0d8ff")
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        yr_r = filtered_df.groupby("release_year")[regions].sum().reset_index()
        yr_rm = yr_r.melt(id_vars="release_year", var_name="Region", value_name="Sales")
        yr_rm["Region"] = yr_rm["Region"].map(region_labels)
        fig = glass_layout(px.line(yr_rm, x="release_year", y="Sales", color="Region",
            markers=False, color_discrete_sequence=PALETTE,
            labels={"release_year": "Year"}), "Regional Sales Over Time")
        st.plotly_chart(fig, use_container_width=True)

    gr = filtered_df.groupby("genre")[regions].sum().reset_index()
    grm = gr.melt(id_vars="genre", var_name="Region", value_name="Sales")
    grm["Region"] = grm["Region"].map(region_labels)
    fig = glass_layout(px.bar(grm, x="genre", y="Sales", color="Region", barmode="group",
        color_discrete_sequence=PALETTE), "Sales by Genre Across Regions")
    st.plotly_chart(fig, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        cr = filtered_df.groupby("console")[regions].sum().reset_index()
        cr = cr.rename(columns=region_labels)
        cr = cr.nlargest(15, "North America").set_index("console")
        fig = glass_layout(px.imshow(cr, text_auto=".0f", aspect="auto",
            color_continuous_scale=ACCENT_SEQ), "Console × Region Heatmap")
        st.plotly_chart(fig, use_container_width=True)
    with c4:
        fig = glass_layout(px.scatter(filtered_df, x="na_sales", y="jp_sales",
            color="genre", hover_name="title", opacity=0.65,
            color_discrete_sequence=PALETTE,
            labels={"na_sales": "NA (M)", "jp_sales": "JP (M)"}), "NA vs Japan Sales")
        st.plotly_chart(fig, use_container_width=True)

    top_c = filtered_df.groupby("console")["total_sales"].sum().nlargest(10).index
    cr2 = filtered_df[filtered_df["console"].isin(top_c)].groupby("console")[regions].sum().reset_index()
    cr2m = cr2.melt(id_vars="console", var_name="Region", value_name="Sales")
    cr2m["Region"] = cr2m["Region"].map(region_labels)
    fig = glass_layout(px.bar(cr2m, x="console", y="Sales", color="Region", barmode="stack",
        color_discrete_sequence=PALETTE), "Top 10 Consoles – Stacked Regional Sales")
    st.plotly_chart(fig, use_container_width=True)


# ─────────────────────────────────────────────────────────────
# TAB 4 — GENRE
# ─────────────────────────────────────────────────────────────
with tabs[4]:
    st.markdown('<div class="section-title">🎭 Genre Insights</div>', unsafe_allow_html=True)

    gd = filtered_df.groupby("genre").agg(total_sales=("total_sales","sum"), count=("title","count")).reset_index()
    gd["avg_sales"] = gd["total_sales"] / gd["count"]

    c1, c2 = st.columns(2)
    with c1:
        fig = glass_layout(px.bar(gd, x="genre", y="total_sales", color="count",
            color_continuous_scale=ACCENT_SEQ,
            labels={"total_sales": "Sales (M)", "count": "# Games"}), "Total Sales by Genre")
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig = glass_layout(px.bar(gd.sort_values("avg_sales", ascending=False),
            x="genre", y="avg_sales", color="avg_sales", color_continuous_scale=ACCENT_SEQ,
            labels={"avg_sales": "Avg Sales (M)"}), "Avg Sales Per Game by Genre")
        fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    gy = filtered_df.groupby(["release_year","genre"]).size().reset_index(name="count")
    gp = gy.pivot(index="genre", columns="release_year", values="count").fillna(0)
    fig = glass_layout(px.imshow(gp, aspect="auto", color_continuous_scale=ACCENT_SEQ),
        "Genre Popularity Heatmap by Year")
    st.plotly_chart(fig, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        gs = filtered_df[filtered_df["critic_score"]>0].groupby("genre")["critic_score"].mean().reset_index()
        fig = glass_layout(px.bar(gs.sort_values("critic_score", ascending=False),
            x="genre", y="critic_score", color="critic_score", color_continuous_scale=ACCENT_SEQ,
            labels={"critic_score": "Avg Score"}), "Avg Critic Score by Genre")
        fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)
    with c4:
        gb = filtered_df[filtered_df["total_sales"]>0]
        fig = glass_layout(px.box(gb, x="genre", y="total_sales", color="genre",
            color_discrete_sequence=PALETTE,
            labels={"total_sales": "Sales (M)"}), "Sales Distribution by Genre")
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    dg = filtered_df.groupby(["decade","genre"])["total_sales"].sum().reset_index()
    fig = glass_layout(px.bar(dg, x="decade", y="total_sales", color="genre", barmode="stack",
        color_discrete_sequence=PALETTE,
        labels={"total_sales": "Sales (M)"}), "Genre Sales by Decade")
    st.plotly_chart(fig, use_container_width=True)


# ─────────────────────────────────────────────────────────────
# TAB 5 — CONSOLES
# ─────────────────────────────────────────────────────────────
with tabs[5]:
    st.markdown('<div class="section-title">🕹️ Console Market Share</div>', unsafe_allow_html=True)

    cs = filtered_df.groupby("console")["total_sales"].sum().reset_index().sort_values("total_sales", ascending=False)

    fig = glass_layout(px.bar(cs, x="console", y="total_sales",
        color="total_sales", color_continuous_scale=ACCENT_SEQ,
        labels={"total_sales": "Sales (M)"}), "Total Sales Per Console")
    fig.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        fig = glass_layout(px.pie(cs.head(10), names="console", values="total_sales", hole=0.4,
            color_discrete_sequence=PALETTE), "Top 10 Console Market Share")
        fig.update_traces(textfont_color="#e0d8ff")
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        cc = filtered_df["console"].value_counts().head(20).reset_index()
        cc.columns = ["console", "count"]
        fig = glass_layout(px.bar(cc, x="count", y="console", orientation="h",
            color="count", color_continuous_scale=ACCENT_SEQ,
            labels={"count": "Games", "console": ""}), "Top 20 Consoles by Game Count")
        fig.update_layout(yaxis={"categoryorder": "total ascending"}, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        csc = filtered_df[filtered_df["critic_score"]>0].groupby("console")["critic_score"].mean().reset_index().nlargest(20,"critic_score")
        fig = glass_layout(px.bar(csc, x="critic_score", y="console", orientation="h",
            color="critic_score", color_continuous_scale=ACCENT_SEQ,
            labels={"critic_score": "Avg Score", "console": ""}), "Avg Critic Score by Console")
        fig.update_layout(yaxis={"categoryorder": "total ascending"}, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)
    with c4:
        top10_c = cs.head(10)["console"].tolist()
        cg = filtered_df[filtered_df["console"].isin(top10_c)].groupby(["console","genre"])["total_sales"].sum().reset_index()
        fig = glass_layout(px.bar(cg, x="console", y="total_sales", color="genre", barmode="stack",
            color_discrete_sequence=PALETTE,
            labels={"total_sales": "Sales (M)"}), "Genre Mix – Top 10 Consoles")
        st.plotly_chart(fig, use_container_width=True)

    tl = filtered_df[filtered_df["console"].isin(top10_c)].groupby(["release_year","console"]).size().reset_index(name="count")
    fig = glass_layout(px.line(tl, x="release_year", y="count", color="console",
        color_discrete_sequence=PALETTE,
        labels={"release_year": "Year", "count": "Games"}), "Release Timeline by Console")
    st.plotly_chart(fig, use_container_width=True)


# ─────────────────────────────────────────────────────────────
# TAB 6 — PUBLISHERS
# ─────────────────────────────────────────────────────────────
with tabs[6]:
    st.markdown('<div class="section-title">🏢 Publisher Statistics</div>', unsafe_allow_html=True)

    ps = filtered_df.groupby("publisher")["total_sales"].sum().reset_index()
    top10p = ps.nlargest(10, "total_sales")

    fig = glass_layout(px.bar(top10p, y="publisher", x="total_sales", orientation="h",
        color="total_sales", color_continuous_scale=ACCENT_SEQ,
        labels={"total_sales": "Sales (M)", "publisher": ""}), "Top 10 Publishers by Sales")
    fig.update_layout(yaxis={"categoryorder": "total ascending"}, coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        pc = filtered_df["publisher"].value_counts().head(10).reset_index()
        pc.columns = ["publisher", "count"]
        fig = glass_layout(px.bar(pc, x="count", y="publisher", orientation="h",
            color="count", color_continuous_scale=ACCENT_SEQ,
            labels={"count": "Games", "publisher": ""}), "Most Prolific Publishers")
        fig.update_layout(yaxis={"categoryorder": "total ascending"}, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        pa = filtered_df.groupby("publisher").agg(total_sales=("total_sales","sum"), gc=("title","count")).reset_index()
        pa["avg_sales"] = pa["total_sales"] / pa["gc"]
        pa15 = pa[pa["gc"] >= 5].nlargest(15, "avg_sales")
        fig = glass_layout(px.bar(pa15, x="avg_sales", y="publisher", orientation="h",
            color="avg_sales", color_continuous_scale=ACCENT_SEQ,
            labels={"avg_sales": "Avg Sales (M)", "publisher": ""}), "Avg Sales/Game (≥5 games)")
        fig.update_layout(yaxis={"categoryorder": "total ascending"}, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        psc = filtered_df[filtered_df["critic_score"]>0].groupby("publisher")["critic_score"].mean().reset_index().nlargest(15, "critic_score")
        fig = glass_layout(px.bar(psc, x="critic_score", y="publisher", orientation="h",
            color="critic_score", color_continuous_scale=ACCENT_SEQ,
            labels={"critic_score": "Avg Score", "publisher": ""}), "Top Publishers by Avg Score")
        fig.update_layout(yaxis={"categoryorder": "total ascending"}, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)
    with c4:
        top10pubs = top10p["publisher"].tolist()
        pg = filtered_df[filtered_df["publisher"].isin(top10pubs)].groupby(["publisher","genre"])["total_sales"].sum().reset_index()
        pgp = pg.pivot(index="publisher", columns="genre", values="total_sales").fillna(0)
        fig = glass_layout(px.imshow(pgp, text_auto=".0f", aspect="auto",
            color_continuous_scale=ACCENT_SEQ), "Publisher × Genre Heatmap")
        st.plotly_chart(fig, use_container_width=True)

    top5pubs = top10p.head(5)["publisher"].tolist()
    py = filtered_df[filtered_df["publisher"].isin(top5pubs)].groupby(["release_year","publisher"])["total_sales"].sum().reset_index()
    fig = glass_layout(px.line(py, x="release_year", y="total_sales", color="publisher",
        markers=True, color_discrete_sequence=PALETTE,
        labels={"total_sales": "Sales (M)", "release_year": "Year"}), "Top 5 Publishers – Yearly Sales Trend")
    st.plotly_chart(fig, use_container_width=True)


# ─────────────────────────────────────────────────────────────
# TAB 7 — CRITIC SCORES
# ─────────────────────────────────────────────────────────────
with tabs[7]:
    st.markdown('<div class="section-title">⭐ Critic Score Deep Dive</div>', unsafe_allow_html=True)
    sdf = filtered_df[filtered_df["critic_score"] > 0]

    fig = glass_layout(px.scatter(sdf, x="critic_score", y="total_sales",
        color="genre", hover_name="title", color_discrete_sequence=PALETTE,
        labels={"critic_score": "Score", "total_sales": "Sales (M)"}),
        "Critic Score vs Total Sales")
    st.plotly_chart(fig, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        fig = glass_layout(px.histogram(sdf, x="critic_score", nbins=40, color="genre",
            color_discrete_sequence=PALETTE,
            labels={"critic_score": "Score"}), "Score Distribution")
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig = glass_layout(px.box(sdf, x="genre", y="critic_score", color="genre",
            color_discrete_sequence=PALETTE), "Score Spread by Genre")
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        csc2 = sdf.groupby("console")["critic_score"].mean().reset_index().nlargest(20,"critic_score")
        fig = glass_layout(px.bar(csc2, x="critic_score", y="console", orientation="h",
            color="critic_score", color_continuous_scale=ACCENT_SEQ,
            labels={"critic_score": "Avg Score", "console": ""}), "Avg Score by Console")
        fig.update_layout(yaxis={"categoryorder": "total ascending"}, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)
    with c4:
        fig = glass_layout(px.scatter(sdf, x="critic_score", y="na_sales",
            color="console", hover_name="title", color_discrete_sequence=PALETTE,
            labels={"critic_score": "Score", "na_sales": "NA Sales (M)"}),
            "Score vs NA Sales")
        st.plotly_chart(fig, use_container_width=True)

    sy = sdf.groupby("release_year")["critic_score"].mean().reset_index()
    fig = glass_layout(px.line(sy, x="release_year", y="critic_score", markers=True,
        color_discrete_sequence=["#a78bfa"],
        labels={"critic_score": "Avg Score", "release_year": "Year"}),
        "Avg Critic Score Over Years")
    st.plotly_chart(fig, use_container_width=True)


# ─────────────────────────────────────────────────────────────
# TAB 8 — CUMULATIVE
# ─────────────────────────────────────────────────────────────
with tabs[8]:
    st.markdown('<div class="section-title">📈 Cumulative Sales Trends</div>', unsafe_allow_html=True)

    yd = filtered_df.groupby("release_year")["total_sales"].sum().reset_index().sort_values("release_year")
    yd["cumulative"] = yd["total_sales"].cumsum()
    yd["yoy"] = yd["total_sales"].pct_change() * 100

    fig = glass_layout(px.area(yd, x="release_year", y="cumulative",
        color_discrete_sequence=["#a78bfa"],
        labels={"release_year": "Year", "cumulative": "Cumulative Sales (M)"}),
        "Cumulative Global Sales Over Time")
    fig.update_traces(fill='tozeroy', fillcolor="rgba(167,139,250,0.15)", line_color="#a78bfa")
    st.plotly_chart(fig, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        fig = glass_layout(px.bar(yd, x="release_year", y="total_sales",
            color="total_sales", color_continuous_scale=ACCENT_SEQ,
            labels={"total_sales": "Sales (M)", "release_year": "Year"}), "Yearly Sales Increment")
        fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig = glass_layout(px.bar(yd.dropna(subset=["yoy"]), x="release_year", y="yoy",
            color="yoy", color_continuous_scale="RdYlGn",
            labels={"yoy": "Growth (%)", "release_year": "Year"}), "YoY Sales Growth Rate (%)")
        fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    rcy = filtered_df.groupby("release_year")[regions].sum().sort_index().cumsum().reset_index()
    rcym = rcy.melt(id_vars="release_year", var_name="Region", value_name="Cumulative")
    rcym["Region"] = rcym["Region"].map(region_labels)
    fig = glass_layout(px.area(rcym, x="release_year", y="Cumulative", color="Region",
        color_discrete_sequence=PALETTE,
        labels={"release_year": "Year"}), "Cumulative Sales by Region")
    st.plotly_chart(fig, use_container_width=True)

    gc = filtered_df.groupby("release_year").size().reset_index(name="games").sort_values("release_year")
    gc["cum_games"] = gc["games"].cumsum()
    fig = glass_layout(px.area(gc, x="release_year", y="cum_games",
        color_discrete_sequence=["#60a5fa"],
        labels={"release_year": "Year", "cum_games": "Total Games"}), "Cumulative Game Count")
    fig.update_traces(fill='tozeroy', fillcolor="rgba(96,165,250,0.13)", line_color="#60a5fa")
    st.plotly_chart(fig, use_container_width=True)


# ─────────────────────────────────────────────────────────────
# TAB 9 — ROLLING
# ─────────────────────────────────────────────────────────────
with tabs[9]:
    st.markdown('<div class="section-title">🔄 Rolling Averages & Smoothed Trends</div>', unsafe_allow_html=True)

    yd2 = filtered_df.groupby("release_year")["total_sales"].sum().reset_index().sort_values("release_year")
    yd2["roll3"] = yd2["total_sales"].rolling(3, min_periods=1).mean()
    yd2["roll5"] = yd2["total_sales"].rolling(5, min_periods=1).mean()

    c1, c2 = st.columns(2)
    with c1:
        fig = glass_layout(px.line(yd2, x="release_year", y=["total_sales","roll3"],
            color_discrete_sequence=["rgba(167,139,250,0.4)","#a78bfa"],
            labels={"value": "Sales (M)", "variable": "Metric", "release_year": "Year"}),
            "3-Year Rolling Average")
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig = glass_layout(px.line(yd2, x="release_year", y=["total_sales","roll5"],
            color_discrete_sequence=["rgba(96,165,250,0.4)","#60a5fa"],
            labels={"value": "Sales (M)", "variable": "Metric", "release_year": "Year"}),
            "5-Year Rolling Average")
        st.plotly_chart(fig, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        gcy = filtered_df.groupby("release_year").size().reset_index(name="count").sort_values("release_year")
        gcy["roll"] = gcy["count"].rolling(3, min_periods=1).mean()
        fig = glass_layout(px.line(gcy, x="release_year", y=["count","roll"],
            color_discrete_sequence=["rgba(244,114,182,0.4)","#f472b6"],
            labels={"value": "Games", "variable": "Metric", "release_year": "Year"}),
            "Rolling Avg Games Released")
        st.plotly_chart(fig, use_container_width=True)
    with c4:
        syr = filtered_df[filtered_df["critic_score"]>0].groupby("release_year")["critic_score"].mean().reset_index().sort_values("release_year")
        syr["roll"] = syr["critic_score"].rolling(3, min_periods=1).mean()
        fig = glass_layout(px.line(syr, x="release_year", y=["critic_score","roll"],
            color_discrete_sequence=["rgba(167,139,250,0.4)","#a78bfa"],
            labels={"value": "Score", "variable": "Metric", "release_year": "Year"}),
            "Rolling Avg Critic Score")
        st.plotly_chart(fig, use_container_width=True)

    mr = filtered_df.groupby("release_year")[regions].sum().sort_index()
    for col in mr.columns:
        mr[f"{col}_roll"] = mr[col].rolling(3, min_periods=1).mean()
    roll_cols = [c for c in mr.columns if "_roll" in c]
    rdf = mr[roll_cols].reset_index().melt(id_vars="release_year", var_name="Region", value_name="Rolling Avg")
    rdf["Region"] = rdf["Region"].str.replace("_roll","").map(region_labels)
    fig = glass_layout(px.line(rdf, x="release_year", y="Rolling Avg", color="Region",
        color_discrete_sequence=PALETTE,
        labels={"release_year": "Year"}), "3-Year Rolling Avg – All Regions")
    st.plotly_chart(fig, use_container_width=True)


# ─────────────────────────────────────────────────────────────
# TAB 10 — TIME ANALYSIS
# ─────────────────────────────────────────────────────────────
with tabs[10]:
    st.markdown('<div class="section-title">⏳ Time-Based Analysis</div>', unsafe_allow_html=True)

    vd = filtered_df.dropna(subset=["update_gap_days"])
    month_names = {1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",
                   7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}

    c1, c2 = st.columns(2)
    with c1:
        mc = filtered_df.groupby("release_month").size().reset_index(name="count")
        mc["month"] = mc["release_month"].map(month_names)
        fig = glass_layout(px.bar(mc, x="month", y="count",
            category_orders={"month": list(month_names.values())},
            color="count", color_continuous_scale=ACCENT_SEQ,
            labels={"count": "Games", "month": "Month"}), "Games Released by Month")
        fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        qs = filtered_df.groupby("release_quarter")["total_sales"].sum().reset_index()
        qs["release_quarter"] = "Q" + qs["release_quarter"].astype(str)
        fig = glass_layout(px.bar(qs, x="release_quarter", y="total_sales",
            color="total_sales", color_continuous_scale=ACCENT_SEQ,
            labels={"total_sales": "Sales (M)", "release_quarter": "Quarter"}),
            "Sales by Release Quarter")
        fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    if not vd.empty:
        fig = glass_layout(px.histogram(vd, x="update_gap_days", nbins=50,
            color_discrete_sequence=["#a78bfa"],
            labels={"update_gap_days": "Days"}), "Release-to-Update Gap Distribution")
        st.plotly_chart(fig, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        if not vd.empty:
            fig = glass_layout(px.box(vd, x="genre", y="update_gap_days", color="genre",
                color_discrete_sequence=PALETTE,
                labels={"update_gap_days": "Gap (Days)"}), "Update Gap by Genre")
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
    with c4:
        if not vd.empty:
            gy2 = vd.groupby("release_year")["update_gap_days"].mean().reset_index()
            fig = glass_layout(px.line(gy2, x="release_year", y="update_gap_days", markers=True,
                color_discrete_sequence=["#f472b6"],
                labels={"update_gap_days": "Avg Gap (Days)", "release_year": "Year"}),
                "Avg Update Gap by Year")
            st.plotly_chart(fig, use_container_width=True)

    hp = filtered_df.groupby(["release_year","release_month"])["total_sales"].sum().reset_index()
    hpv = hp.pivot(index="release_year", columns="release_month", values="total_sales").fillna(0)
    hpv.columns = [month_names.get(c, c) for c in hpv.columns]
    fig = glass_layout(px.imshow(hpv, aspect="auto", color_continuous_scale=ACCENT_SEQ),
        "Sales Heatmap: Year × Month of Release")
    st.plotly_chart(fig, use_container_width=True)
