import streamlit as st
import os
import pandas as pd

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="Sales Tech ID",
    page_icon="📊",
    layout="wide"
)

# -----------------------------
# LOGIN
# -----------------------------
def login():
    st.title("🔐 تسجيل الدخول")

    username = st.text_input("اسم المستخدم")
    password = st.text_input("كلمة المرور", type="password")

    if st.button("دخول"):
        if username == "123" and password == "123":
            st.session_state["logged_in"] = True
            st.rerun()
        else:
            st.error("بيانات الدخول غير صحيحة")

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login()
    st.stop()

# -----------------------------
# CSS - SaaS Style
# -----------------------------
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #4b5563 0%, #374151 100%);
    }

    [data-testid="stAppViewContainer"] {
        background: linear-gradient(180deg, #4b5563 0%, #374151 100%);
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    .block-container {
        max-width: 1100px;
        padding-top: 1.2rem;
        padding-bottom: 2rem;
        margin: auto;
    }

    h1, h2, h3, h4, h5, h6, p, label, div {
        direction: rtl;
        text-align: right;
    }

    .hero-box {
        background: rgba(15, 23, 42, 0.78);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 28px;
        padding: 26px 28px 22px 28px;
        margin: 0 auto 20px auto;
        max-width: 820px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.18);
        backdrop-filter: blur(8px);
    }

    .portal-title {
        font-size: 42px;
        font-weight: 800;
        color: #ffffff;
        text-align: center;
        margin-bottom: 6px;
        direction: ltr;
        letter-spacing: -0.5px;
    }

    .portal-subtitle {
        font-size: 17px;
        color: #d1d5db;
        text-align: center;
        margin-bottom: 0;
        direction: ltr;
    }

    .small-note {
        color: #cbd5e1;
        font-size: 14px;
        text-align: center;
        margin-top: 8px;
        direction: ltr;
    }

    .section-card {
        background: rgba(15, 23, 42, 0.78);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 24px;
        padding: 22px;
        margin: 0 auto 22px auto;
        max-width: 900px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.16);
        backdrop-filter: blur(8px);
    }

    .metric-card {
        background: rgba(30, 41, 59, 0.92);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 20px;
        padding: 18px 16px;
        text-align: center;
        margin-bottom: 10px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.10);
    }

    .metric-title {
        color: #cbd5e1;
        font-size: 14px;
        margin-bottom: 8px;
        text-align: center;
    }

    .metric-value {
        color: #ffffff;
        font-size: 30px;
        font-weight: 800;
        text-align: center;
    }

    .section-title {
        color: #ffffff;
        font-size: 30px;
        font-weight: 800;
        margin-bottom: 18px;
    }

    .result-card {
        background: rgba(30, 41, 59, 0.95);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 22px;
        padding: 22px;
        margin-bottom: 16px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.12);
    }

    .result-title {
        font-size: 24px;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 12px;
    }

    .result-grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 10px 22px;
    }

    .result-item {
        color: #e5e7eb;
        font-size: 16px;
        line-height: 1.8;
    }

    .result-label {
        color: #93c5fd;
        font-weight: 700;
    }

    .stButton > button {
        background: rgba(15, 23, 42, 0.95);
        color: white;
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 14px;
        font-weight: 700;
        padding: 0.60rem 1rem;
        transition: 0.2s ease;
    }

    .stButton > button:hover {
        border-color: rgba(147,197,253,0.55);
        box-shadow: 0 0 0 2px rgba(147,197,253,0.10);
    }

    [data-testid="stTextInput"] > div > div,
    [data-testid="stSelectbox"] > div > div {
        background: rgba(17, 24, 39, 0.92);
        border-radius: 14px;
        border: 1px solid rgba(255,255,255,0.08);
    }

    [data-testid="stTextInput"] input,
    [data-testid="stSelectbox"] div {
        color: white;
    }

    @media (max-width: 768px) {
        .result-grid {
            grid-template-columns: 1fr;
        }

        .hero-box,
        .section-card {
            max-width: 100%;
        }

        .portal-title {
            font-size: 34px;
        }
    }
</style>
""", unsafe_allow_html=True)

.logo-img {
    max-width: 140px;
    filter: brightness(1.1);
}


# -----------------------------
# Months map
# -----------------------------
month_map = {
    "1": "كانون الثاني",
    "2": "شباط",
    "3": "آذار",
    "4": "نيسان",
    "5": "أيار",
    "6": "حزيران",
    "7": "تموز",
    "8": "آب",
    "9": "أيلول",
    "10": "تشرين الأول",
    "11": "تشرين الثاني",
    "12": "كانون الأول"
}

# -----------------------------
# Data loading
# -----------------------------
@st.cache_data
def load_data(file_path, modified_time):
    df = pd.read_excel(file_path)
    df = df.fillna("")
    df.columns = df.columns.str.strip()

    expected_cols = [
        "Year", "MonthNum", "Product", "Governorate",
        "Department", "ReportType", "ReportName", "TeamsLink"
    ]

    for col in expected_cols:
        if col not in df.columns:
            df[col] = ""

    text_cols = ["Product", "Governorate", "Department", "ReportType", "ReportName", "TeamsLink"]
    for col in text_cols:
        df[col] = df[col].astype(str).str.strip()

    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df["MonthNum"] = pd.to_numeric(df["MonthNum"], errors="coerce")

    df["Year"] = df["Year"].apply(lambda x: str(int(x)) if pd.notnull(x) else "")
    df["MonthNum"] = df["MonthNum"].apply(lambda x: str(int(x)) if pd.notnull(x) else "")

    df = df[
        ~(
            (df["Year"] == "") &
            (df["MonthNum"] == "") &
            (df["Product"] == "") &
            (df["Governorate"] == "") &
            (df["Department"] == "") &
            (df["ReportType"] == "") &
            (df["ReportName"] == "") &
            (df["TeamsLink"] == "")
        )
    ].copy()

    return df

# -----------------------------
# File check
# -----------------------------
file_path = "reports.xlsx"

if not os.path.exists(file_path):
    st.error("ملف reports.xlsx غير موجود داخل مجلد المشروع.")
    st.stop()

modified_time = os.path.getmtime(file_path)
df = load_data(file_path, modified_time)

# -----------------------------
# Top actions
# -----------------------------
top_col1, top_col2, top_col3 = st.columns([1, 1, 6])

with top_col1:
    if st.button("🔄 تحديث"):
        st.cache_data.clear()
        st.rerun()

with top_col2:
    if st.button("🧹 تصفير"):
        st.rerun()

# -----------------------------
# Hero section
# -----------------------------
st.markdown('<div class="hero-box">', unsafe_allow_html=True)

if os.path.exists("logo.png"):
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("logo.png", width=170)

st.markdown('<div class="portal-title">Sales Tech ID</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="portal-subtitle">Sales Analytics & Reporting Portal</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="small-note">Internal system for quick access to sales and operational reports</div>',
    unsafe_allow_html=True
)

st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Metrics
# -----------------------------
total_reports = len(df)
total_products = df["Product"].nunique() if "Product" in df.columns else 0
total_governorates = df["Governorate"].nunique() if "Governorate" in df.columns else 0
total_types = df["ReportType"].nunique() if "ReportType" in df.columns else 0

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">عدد التقارير</div>
            <div class="metric-value">{total_reports}</div>
        </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">عدد المستحضرات</div>
            <div class="metric-value">{total_products}</div>
        </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">عدد المحافظات</div>
            <div class="metric-value">{total_governorates}</div>
        </div>
    """, unsafe_allow_html=True)

with m4:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">أنواع التقارير</div>
            <div class="metric-value">{total_types}</div>
        </div>
    """, unsafe_allow_html=True)

# -----------------------------
# Filters + Search
# -----------------------------
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">الفلاتر والبحث</div>', unsafe_allow_html=True)

search_text = st.text_input("البحث السريع", placeholder="اكتب اسم تقرير أو مستحضر أو محافظة...")

years = ["الكل"] + sorted([x for x in df["Year"].unique().tolist() if x != ""])
months = ["الكل"] + sorted([x for x in df["MonthNum"].unique().tolist() if x != ""], key=lambda x: int(x))
products = ["الكل"] + sorted([x for x in df["Product"].unique().tolist() if x != ""])
governorates = ["الكل"] + sorted([x for x in df["Governorate"].unique().tolist() if x != ""])
departments = ["الكل"] + sorted([x for x in df["Department"].unique().tolist() if x != ""])
report_types = ["الكل"] + sorted([x for x in df["ReportType"].unique().tolist() if x != ""])

c1, c2, c3 = st.columns(3)
with c1:
    selected_year = st.selectbox("السنة", years)
with c2:
    selected_month = st.selectbox(
        "الشهر",
        months,
        format_func=lambda x: month_map.get(x, x) if x != "الكل" else x
    )
with c3:
    selected_product = st.selectbox("المستحضر", products)

c4, c5, c6 = st.columns(3)
with c4:
    selected_governorate = st.selectbox("المحافظة", governorates)
with c5:
    selected_department = st.selectbox("القسم", departments)
with c6:
    selected_report_type = st.selectbox("نوع التقرير", report_types)

st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Filtering
# -----------------------------
filtered_df = df.copy()

if search_text.strip():
    search_value = search_text.strip().lower()
    filtered_df = filtered_df[
        filtered_df["ReportName"].str.lower().str.contains(search_value, na=False) |
        filtered_df["Product"].str.lower().str.contains(search_value, na=False) |
        filtered_df["Governorate"].str.lower().str.contains(search_value, na=False) |
        filtered_df["Department"].str.lower().str.contains(search_value, na=False) |
        filtered_df["ReportType"].str.lower().str.contains(search_value, na=False)
    ]

if selected_year != "الكل":
    filtered_df = filtered_df[filtered_df["Year"] == selected_year]

if selected_month != "الكل":
    filtered_df = filtered_df[filtered_df["MonthNum"] == selected_month]

if selected_product != "الكل":
    filtered_df = filtered_df[filtered_df["Product"] == selected_product]

if selected_governorate != "الكل":
    filtered_df = filtered_df[filtered_df["Governorate"] == selected_governorate]

if selected_department != "الكل":
    filtered_df = filtered_df[filtered_df["Department"] == selected_department]

if selected_report_type != "الكل":
    filtered_df = filtered_df[filtered_df["ReportType"] == selected_report_type]

filtered_df["YearSort"] = pd.to_numeric(filtered_df["Year"], errors="coerce")
filtered_df["MonthSort"] = pd.to_numeric(filtered_df["MonthNum"], errors="coerce")

filtered_df = filtered_df.sort_values(
    by=["YearSort", "MonthSort", "ReportName"],
    ascending=[False, False, True]
).drop(columns=["YearSort", "MonthSort"], errors="ignore")

# -----------------------------
# Results
# -----------------------------
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">النتائج</div>', unsafe_allow_html=True)
st.caption(f"عدد النتائج الحالية: {len(filtered_df)}")

if not filtered_df.empty:
    for _, row in filtered_df.iterrows():
        month_display = month_map.get(row["MonthNum"], row["MonthNum"])

        st.markdown(f"""
            <div class="result-card">
                <div class="result-title">{row['ReportName']}</div>
                <div class="result-grid">
                    <div class="result-item"><span class="result-label">السنة:</span> {row['Year']}</div>
                    <div class="result-item"><span class="result-label">الشهر:</span> {month_display}</div>
                    <div class="result-item"><span class="result-label">المستحضر:</span> {row['Product']}</div>
                    <div class="result-item"><span class="result-label">المحافظة:</span> {row['Governorate']}</div>
                    <div class="result-item"><span class="result-label">القسم:</span> {row['Department']}</div>
                    <div class="result-item"><span class="result-label">نوع التقرير:</span> {row['ReportType']}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        if str(row["TeamsLink"]).strip().startswith("http"):
            st.link_button("📂 فتح التقرير", row["TeamsLink"], use_container_width=False)

        st.write("")
else:
    st.warning("لا يوجد تقرير مطابق للاختيارات الحالية.")

st.markdown('</div>', unsafe_allow_html=True)
