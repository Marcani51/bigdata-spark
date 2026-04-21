import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Retail Analytics Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS
# ============================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }
    
    .sub-header {
        color: #6c757d;
        font-size: 1rem;
        margin-top: -10px;
        margin-bottom: 30px;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 16px;
        padding: 20px 24px;
        border-left: 4px solid;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        margin: 4px 0;
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: #6c757d;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .section-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #2d3436;
        margin-top: 30px;
        margin-bottom: 15px;
        padding-bottom: 8px;
        border-bottom: 2px solid #667eea;
        display: inline-block;
    }
    
    div[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2d3436 0%, #1a1a2e 100%);
    }
    
    div[data-testid="stSidebar"] .stMarkdown {
        color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# DATA LOADING
# ============================================================
@st.cache_data
def load_data():
    """Load data dari Parquet (jika ada) atau CSV fallback."""
    parquet_path = "/output/retail_parquet"
    csv_path = "/data/retail_sales_dataset.csv"
    
    if os.path.exists(parquet_path):
        df = pd.read_parquet(parquet_path)
        source = "Parquet (Spark output)"
    elif os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        source = "CSV (raw)"
    else:
        st.error("❌ Data tidak ditemukan! Pastikan file ada di /data/")
        st.stop()
    
    # Normalize column names: underscore → spaces (match original CSV)
    col_rename = {
        "Transaction_ID": "Transaction ID",
        "Customer_ID": "Customer ID",
        "Product_Category": "Product Category",
        "Price_per_Unit": "Price per Unit",
        "Total_Amount": "Total Amount",
    }
    df.rename(columns={k: v for k, v in col_rename.items() if k in df.columns}, inplace=True)
    
    # Ensure Date is datetime
    df["Date"] = pd.to_datetime(df["Date"])
    df["Month"] = df["Date"].dt.month
    df["Month_Name"] = df["Date"].dt.strftime("%b")
    df["Quarter"] = df["Date"].dt.quarter
    df["Day_of_Week"] = df["Date"].dt.day_name()
    
    # Age groups
    bins = [17, 25, 35, 45, 55, 65]
    labels = ["18-25", "26-35", "36-45", "46-55", "56-64"]
    df["Age_Group"] = pd.cut(df["Age"], bins=bins, labels=labels)
    
    # Price tier
    df["Price_Tier"] = df["Price per Unit"].apply(
        lambda x: "Budget" if x <= 30 else ("Mid-Range" if x <= 50 else "Premium")
    )
    
    return df, source


@st.cache_data
def load_segments():
    """Load segmentasi pelanggan dari Parquet (jika ada)."""
    seg_path = "/output/customer_segments"
    if os.path.exists(seg_path):
        return pd.read_parquet(seg_path)
    return None


# Load data
df, data_source = load_data()
df_segments = load_segments()


# ============================================================
# SIDEBAR FILTERS
# ============================================================
with st.sidebar:
    st.markdown("## 🛒 Retail Analytics")
    st.markdown("---")
    
    st.markdown("### 🔍 Filter Data")
    
    # Category filter
    categories = st.multiselect(
        "Kategori Produk",
        options=df["Product Category"].unique().tolist(),
        default=df["Product Category"].unique().tolist()
    )
    
    # Gender filter
    genders = st.multiselect(
        "Gender",
        options=df["Gender"].unique().tolist(),
        default=df["Gender"].unique().tolist()
    )
    
    # Age slider
    age_range = st.slider(
        "Rentang Usia",
        min_value=int(df["Age"].min()),
        max_value=int(df["Age"].max()),
        value=(int(df["Age"].min()), int(df["Age"].max()))
    )
    
    # Month filter
    months = st.multiselect(
        "Bulan",
        options=sorted(df["Month"].unique().tolist()),
        default=sorted(df["Month"].unique().tolist()),
        format_func=lambda x: ["Jan","Feb","Mar","Apr","Mei","Jun","Jul","Agu","Sep","Okt","Nov","Des"][x-1]
    )
    
    st.markdown("---")
    st.markdown(f"📊 Sumber: `{data_source}`")
    st.markdown(f"📅 Periode: Jan 2023 – Jan 2024")


# Apply filters
mask = (
    (df["Product Category"].isin(categories)) &
    (df["Gender"].isin(genders)) &
    (df["Age"] >= age_range[0]) &
    (df["Age"] <= age_range[1]) &
    (df["Month"].isin(months))
)
df_filtered = df[mask]


# ============================================================
# HEADER
# ============================================================
st.markdown('<p class="main-header">🛒 Retail Sales Analytics Dashboard</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Analisis Perilaku Belanja Pelanggan — Powered by Apache Spark + Streamlit</p>', unsafe_allow_html=True)


# ============================================================
# KPI METRICS
# ============================================================
col1, col2, col3, col4, col5 = st.columns(5)

total_revenue = df_filtered["Total Amount"].sum()
total_transactions = len(df_filtered)
avg_transaction = df_filtered["Total Amount"].mean()
unique_customers = df_filtered["Customer ID"].nunique()
avg_quantity = df_filtered["Quantity"].mean()

with col1:
    st.markdown(f"""
    <div class="metric-card" style="border-left-color: #667eea;">
        <div class="metric-label">Total Revenue</div>
        <div class="metric-value" style="color: #667eea;">Rp{total_revenue:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card" style="border-left-color: #4ECDC4;">
        <div class="metric-label">Total Transaksi</div>
        <div class="metric-value" style="color: #4ECDC4;">{total_transactions:,}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card" style="border-left-color: #FF6B6B;">
        <div class="metric-label">Avg per Transaksi</div>
        <div class="metric-value" style="color: #FF6B6B;">Rp{avg_transaction:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card" style="border-left-color: #FFA726;">
        <div class="metric-label">Pelanggan Unik</div>
        <div class="metric-value" style="color: #FFA726;">{unique_customers:,}</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="metric-card" style="border-left-color: #a29bfe;">
        <div class="metric-label">Avg Quantity</div>
        <div class="metric-value" style="color: #a29bfe;">{avg_quantity:.1f}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ============================================================
# ROW 1: Revenue by Category + Monthly Trend
# ============================================================
st.markdown('<p class="section-title">📈 Analisis Penjualan</p>', unsafe_allow_html=True)

col_left, col_right = st.columns(2)

with col_left:
    rev_by_cat = df_filtered.groupby("Product Category").agg(
        revenue=("Total Amount", "sum"),
        count=("Total Amount", "count"),
        avg_amount=("Total Amount", "mean")
    ).reset_index().sort_values("revenue", ascending=True)
    
    fig_cat = go.Figure()
    colors = {"Beauty": "#FF6B6B", "Clothing": "#4ECDC4", "Electronics": "#667eea"}
    
    fig_cat.add_trace(go.Bar(
        y=rev_by_cat["Product Category"],
        x=rev_by_cat["revenue"],
        orientation="h",
        marker_color=[colors.get(c, "#999") for c in rev_by_cat["Product Category"]],
        text=[f'Rp{v:,.0f} ({n} txn)' for v, n in zip(rev_by_cat["revenue"], rev_by_cat["count"])],
        textposition="auto",
        textfont=dict(color="white", size=13, family="Inter"),
    ))
    
    fig_cat.update_layout(
        title=dict(text="Revenue per Kategori Produk", font=dict(size=16, family="Inter")),
        xaxis_title="Revenue",
        yaxis_title="",
        height=380,
        margin=dict(l=20, r=20, t=50, b=20),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig_cat, use_container_width=True)

with col_right:
    monthly = df_filtered.groupby("Month").agg(
        revenue=("Total Amount", "sum"),
        count=("Total Amount", "count")
    ).reset_index().sort_values("Month")
    
    month_names = ["Jan","Feb","Mar","Apr","Mei","Jun","Jul","Agu","Sep","Okt","Nov","Des"]
    monthly["Month_Label"] = monthly["Month"].apply(lambda x: month_names[x-1])
    
    fig_monthly = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig_monthly.add_trace(
        go.Scatter(
            x=monthly["Month_Label"], y=monthly["revenue"],
            mode="lines+markers",
            name="Revenue",
            line=dict(color="#667eea", width=3),
            marker=dict(size=8),
            fill="tozeroy",
            fillcolor="rgba(102, 126, 234, 0.1)"
        ), secondary_y=False
    )
    
    fig_monthly.add_trace(
        go.Bar(
            x=monthly["Month_Label"], y=monthly["count"],
            name="Jumlah Transaksi",
            marker_color="rgba(255, 167, 38, 0.4)",
        ), secondary_y=True
    )
    
    fig_monthly.update_layout(
        title=dict(text="Tren Penjualan Bulanan", font=dict(size=16, family="Inter")),
        height=380,
        margin=dict(l=20, r=20, t=50, b=20),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
    )
    fig_monthly.update_yaxes(title_text="Revenue", secondary_y=False)
    fig_monthly.update_yaxes(title_text="Transaksi", secondary_y=True)
    st.plotly_chart(fig_monthly, use_container_width=True)


# ============================================================
# ROW 2: Demographics
# ============================================================
st.markdown('<p class="section-title">👥 Analisis Demografi</p>', unsafe_allow_html=True)

col_d1, col_d2, col_d3 = st.columns(3)

with col_d1:
    gender_data = df_filtered.groupby("Gender").agg(
        count=("Total Amount", "count"),
        revenue=("Total Amount", "sum")
    ).reset_index()
    
    fig_gender = go.Figure(data=[go.Pie(
        labels=gender_data["Gender"],
        values=gender_data["revenue"],
        hole=0.55,
        marker_colors=["#667eea", "#FF6B6B"],
        textinfo="label+percent",
        textfont=dict(size=13, family="Inter"),
        hovertemplate="<b>%{label}</b><br>Revenue: Rp%{value:,.0f}<br>%{percent}<extra></extra>"
    )])
    
    fig_gender.update_layout(
        title=dict(text="Revenue by Gender", font=dict(size=16, family="Inter")),
        height=350,
        margin=dict(l=20, r=20, t=50, b=20),
        showlegend=False,
        annotations=[dict(text=f"Rp{gender_data['revenue'].sum():,.0f}", x=0.5, y=0.5, font_size=14, showarrow=False, font=dict(family="Inter", color="#2d3436"))]
    )
    st.plotly_chart(fig_gender, use_container_width=True)

with col_d2:
    fig_age = px.histogram(
        df_filtered, x="Age", nbins=25,
        color_discrete_sequence=["#4ECDC4"],
        title="Distribusi Usia Pelanggan"
    )
    fig_age.add_vline(x=df_filtered["Age"].mean(), line_dash="dash", line_color="#FF6B6B",
                      annotation_text=f"Mean: {df_filtered['Age'].mean():.0f}")
    fig_age.update_layout(
        height=350,
        margin=dict(l=20, r=20, t=50, b=20),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis_title="Usia", yaxis_title="Frekuensi",
        title_font=dict(size=16, family="Inter")
    )
    st.plotly_chart(fig_age, use_container_width=True)

with col_d3:
    age_spending = df_filtered.groupby("Age_Group", observed=True).agg(
        avg_spending=("Total Amount", "mean"),
        count=("Total Amount", "count")
    ).reset_index()
    
    fig_age_bar = go.Figure(data=[go.Bar(
        x=age_spending["Age_Group"].astype(str),
        y=age_spending["avg_spending"],
        marker_color=["#667eea", "#764ba2", "#4ECDC4", "#FFA726", "#FF6B6B"],
        text=[f'Rp{v:,.0f}' for v in age_spending["avg_spending"]],
        textposition="outside",
        textfont=dict(size=11, family="Inter"),
    )])
    
    fig_age_bar.update_layout(
        title=dict(text="Avg Spending per Usia", font=dict(size=16, family="Inter")),
        height=350,
        margin=dict(l=20, r=20, t=50, b=20),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis_title="Kelompok Usia", yaxis_title="Avg Spending",
    )
    st.plotly_chart(fig_age_bar, use_container_width=True)


# ============================================================
# ROW 3: Heatmap + Price Distribution
# ============================================================
st.markdown('<p class="section-title">🔥 Analisis Mendalam</p>', unsafe_allow_html=True)

col_h1, col_h2 = st.columns(2)

with col_h1:
    cross = df_filtered.pivot_table(
        values="Total Amount", index="Gender", 
        columns="Product Category", aggfunc="mean"
    ).round(1)
    
    fig_heat = go.Figure(data=go.Heatmap(
        z=cross.values,
        x=cross.columns.tolist(),
        y=cross.index.tolist(),
        colorscale="YlOrRd",
        text=cross.values.round(0),
        texttemplate="%{text:,.0f}",
        textfont={"size": 14, "family": "Inter"},
        hovertemplate="<b>%{y} × %{x}</b><br>Avg Spending: Rp%{z:,.0f}<extra></extra>"
    ))
    
    fig_heat.update_layout(
        title=dict(text="Heatmap: Avg Spending (Gender × Kategori)", font=dict(size=16, family="Inter")),
        height=360,
        margin=dict(l=20, r=20, t=50, b=20),
    )
    st.plotly_chart(fig_heat, use_container_width=True)

with col_h2:
    tier_data = df_filtered.groupby("Price_Tier").agg(
        count=("Total Amount", "count"),
        revenue=("Total Amount", "sum")
    ).reset_index()
    
    tier_order = {"Budget": 0, "Mid-Range": 1, "Premium": 2}
    tier_data["order"] = tier_data["Price_Tier"].map(tier_order)
    tier_data = tier_data.sort_values("order")
    
    fig_tier = go.Figure(data=[go.Bar(
        x=tier_data["Price_Tier"],
        y=tier_data["revenue"],
        marker_color=["#4ECDC4", "#FFA726", "#FF6B6B"],
        text=[f'Rp{v:,.0f}<br>({n} txn)' for v, n in zip(tier_data["revenue"], tier_data["count"])],
        textposition="auto",
        textfont=dict(color="white", size=12, family="Inter"),
    )])
    
    fig_tier.update_layout(
        title=dict(text="Revenue per Price Tier", font=dict(size=16, family="Inter")),
        height=360,
        margin=dict(l=20, r=20, t=50, b=20),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis_title="Price Tier", yaxis_title="Revenue",
    )
    st.plotly_chart(fig_tier, use_container_width=True)


# ============================================================
# ROW 4: Customer Segmentation (if available)
# ============================================================
if df_segments is not None:
    st.markdown('<p class="section-title">🎯 Segmentasi Pelanggan (K-Means)</p>', unsafe_allow_html=True)
    
    col_s1, col_s2 = st.columns([2, 1])
    
    with col_s1:
        seg_colors = {0: "#FF6B6B", 1: "#4ECDC4", 2: "#667eea"}
        
        tab1, tab2 = st.tabs(["📊 2D Scatter", "🧊 3D Scatter"])
        
        with tab1:
            fig_seg_2d = px.scatter(
                df_segments, x="frequency", y="avg_monetary",
                color="segment",
                size="total_spending",
                color_discrete_map=seg_colors,
                title="2D Scatter Plot Segmentasi",
                labels={
                    "frequency": "Frequency (Jumlah Transaksi)",
                    "avg_monetary": "Average Monetary (Avg Spending)",
                    "segment": "Segment",
                    "total_spending": "Total Spending"
                },
                hover_data=["Customer_ID", "total_spending"]
            )
            fig_seg_2d.update_layout(
                height=420,
                margin=dict(l=20, r=20, t=50, b=20),
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                title_font=dict(size=16, family="Inter"),
            )
            st.plotly_chart(fig_seg_2d, use_container_width=True)
            
        with tab2:
            fig_seg_3d = px.scatter_3d(
                df_segments, x="frequency", y="avg_monetary", z="avg_quantity",
                color="segment",
                size="total_spending",
                color_discrete_map=seg_colors,
                title="3D Scatter Plot (Fitur Lengkap K-Means)",
                labels={
                    "frequency": "Frequency",
                    "avg_monetary": "Avg Spending",
                    "avg_quantity": "Avg Quantity",
                    "segment": "Segment",
                    "total_spending": "Total Spending"
                },
                hover_data=["Customer_ID", "total_spending"]
            )
            fig_seg_3d.update_layout(
                height=420,
                margin=dict(l=0, r=0, t=50, b=0),
                scene=dict(
                    xaxis_title='Frequency',
                    yaxis_title='Avg Spending',
                    zaxis_title='Avg Quantity'
                ),
                title_font=dict(size=16, family="Inter"),
            )
            st.plotly_chart(fig_seg_3d, use_container_width=True)
    
    with col_s2:
        seg_profile = df_segments.groupby("segment").agg(
            jumlah=("Customer_ID", "count"),
            avg_spend=("avg_monetary", "mean"),
            avg_freq=("frequency", "mean"),
            avg_total=("total_spending", "mean")
        ).reset_index()
        
        st.markdown("#### Profil Segmen")
        
        for _, row in seg_profile.iterrows():
            seg_num = int(row["segment"])
            color = seg_colors.get(seg_num, "#999")
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, {color}22, {color}11); 
                        border-left: 4px solid {color}; border-radius: 12px; 
                        padding: 14px 18px; margin-bottom: 12px;">
                <b style="color: {color}; font-size: 1.1rem;">Segment {seg_num}</b><br>
                <span style="color: #555;">👥 {int(row['jumlah'])} pelanggan</span><br>
                <span style="color: #555;">💰 Avg: Rp{row['avg_spend']:,.0f}</span><br>
                <span style="color: #555;">🔄 Freq: {row['avg_freq']:.1f}x</span>
            </div>
            """, unsafe_allow_html=True)

else:
    st.markdown('<p class="section-title">🎯 Segmentasi Pelanggan</p>', unsafe_allow_html=True)
    st.info("💡 Segmentasi belum tersedia. Jalankan **notebook 06 (K-Means)** terlebih dahulu untuk melihat hasil segmentasi di sini.")


# ============================================================
# ROW 5: Raw Data Explorer
# ============================================================
st.markdown('<p class="section-title">📋 Data Explorer</p>', unsafe_allow_html=True)

with st.expander("Lihat Data Mentah", expanded=False):
    st.dataframe(
        df_filtered.head(100).style.format({
            "Total Amount": "Rp{:,.0f}",
            "Price per Unit": "Rp{:,.0f}"
        }),
        use_container_width=True,
        height=400
    )
    st.caption(f"Menampilkan 100 dari {len(df_filtered)} baris (setelah filter)")


# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #adb5bd; font-size: 0.85rem; padding: 10px;">
        🛒 Retail Analytics Dashboard | Powered by <b>Apache Spark</b> + <b>Streamlit</b> | 
        Big Data Analytics Assignment
    </div>
    """,
    unsafe_allow_html=True
)
