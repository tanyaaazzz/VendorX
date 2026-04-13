# ==========================================
# 1. IMPORTS
# ==========================================
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="VendorX Dashboard", layout="wide")

# ==========================================
# 2. LOAD DATA
# ==========================================
@st.cache_data
def load_data():
    return pd.read_csv("data/vendor_data_big.csv")

df = load_data()

# ==========================================
# 3. AUTO DETECT COLUMNS
# ==========================================
cat_cols = df.select_dtypes(include='object').columns.tolist()
num_cols = df.select_dtypes(include=['int64','float64']).columns.tolist()

cat = st.sidebar.selectbox("Select Category", cat_cols)
num = st.sidebar.selectbox("Select Metric", num_cols)

# ==========================================
# 4. FILTERS
# ==========================================
top_categories = df[cat].value_counts().nlargest(10).index
df_filtered = df[df[cat].isin(top_categories)]

# ==========================================
# 5. TITLE
# ==========================================
st.title("🚀 VendorX Analytics Dashboard")
st.caption("Clean • Interactive • Insightful")

# ==========================================
# 6. KPI CARDS
# ==========================================
c1, c2, c3 = st.columns(3)

c1.metric("📦 Records", len(df_filtered))
c2.metric("📊 Avg", f"{df_filtered[num].mean():.2f}")
c3.metric("📈 Max", f"{df_filtered[num].max():.2f}")

# ==========================================
# 7. TOP PERFORMERS (🔥 CLEAN BAR)
# ==========================================
st.subheader("🏆 Top Performers")

grouped = (
    df_filtered.groupby(cat)[num]
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)

fig_bar = px.bar(
    grouped,
    x=num,
    y=cat,
    orientation='h',
    color=num,
    color_continuous_scale='viridis',
    title=f"Top {cat} by {num}"
)

fig_bar.update_layout(yaxis={'categoryorder':'total ascending'})
st.plotly_chart(fig_bar, use_container_width=True)

# ==========================================
# 8. DISTRIBUTION (SMOOTH)
# ==========================================
st.subheader("📊 Distribution")

fig_hist = px.histogram(
    df_filtered,
    x=num,
    nbins=30,
    marginal="box",
    color_discrete_sequence=["#00ADB5"]
)

st.plotly_chart(fig_hist, use_container_width=True)

# ==========================================
# 9. SCATTER (RELATIONSHIP)
# ==========================================
if len(num_cols) >= 2:
    st.subheader("🔍 Relationship Analysis")

    fig_scatter = px.scatter(
        df_filtered,
        x=num_cols[0],
        y=num_cols[1],
        color=cat,
        size=num_cols[0],
        hover_data=[cat],
        title="Feature Relationship"
    )

    st.plotly_chart(fig_scatter, use_container_width=True)

# ==========================================
# 10. PIE (CLEAN SHARE VIEW)
# ==========================================
st.subheader("🥧 Contribution Share")

fig_pie = px.pie(
    df_filtered,
    names=cat,
    values=num,
    hole=0.4
)

st.plotly_chart(fig_pie, use_container_width=True)

# ==========================================
# 11. CORRELATION HEATMAP (CLEAN)
# ==========================================
st.subheader("🔥 Correlation")

corr = df[num_cols].corr()

fig_heat = px.imshow(
    corr,
    text_auto=True,
    color_continuous_scale="RdBu_r"
)

st.plotly_chart(fig_heat, use_container_width=True)

# ==========================================
# 12. INSIGHTS
# ==========================================
st.subheader("🧠 Insights")

best = grouped.iloc[0][cat]
worst = grouped.iloc[-1][cat]

st.success(f"🏆 Best {cat}: {best}")
st.error(f"⚠️ Lowest {cat}: {worst}")
st.info(f"📊 Average {num}: {df[num].mean():.2f}")

# ==========================================
# 13. DATA VIEW
# ==========================================
with st.expander("📂 View Data"):
    st.dataframe(df_filtered.head(100))