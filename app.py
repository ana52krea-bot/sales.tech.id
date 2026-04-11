import streamlit as st
import os
import pandas as pd

# -----------------------------
# Page config (لازم أول شي)
# -----------------------------
st.set_page_config(
    page_title="Sales Tech ID",
    page_icon="📊",
    layout="wide"
)

# -----------------------------
# SESSION STATE INIT
# -----------------------------
defaults = {
    "logged_in": False,
    "year": "الكل",
    "month": "الكل",
    "product": "الكل",
    "gov": "الكل",
    "dep": "الكل",
    "type": "الكل",
    "search": ""
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# -----------------------------
# LOGIN
# -----------------------------
def login():
    st.title("🔐 تسجيل الدخول")

    username = st.text_input("اسم المستخدم")
    password = st.text_input("كلمة المرور", type="password")

    if st.button("دخول"):
        if username == "123" and password == "123":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("بيانات الدخول غير صحيحة")

if not st.session_state.logged_in:
    login()
    st.stop()

# -----------------------------
# LOGOUT BUTTON
# -----------------------------
top1, top2, top3 = st.columns([1,1,6])

with top1:
    if st.button("🚪 تسجيل خروج"):
        for k in defaults:
            st.session_state[k] = defaults[k]
        st.session_state.logged_in = False
        st.rerun()

# -----------------------------
# CSS
# -----------------------------
st.markdown("""
<style>
.stApp {background: linear-gradient(180deg,#4b5563,#374151);}
.block-container {max-width:1100px;}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# DATA
# -----------------------------
@st.cache_data
def load_data(path, mod):
    df = pd.read_excel(path).fillna("")
    df.columns = df.columns.str.strip()
    return df

file_path = "reports.xlsx"

if not os.path.exists(file_path):
    st.error("ملف reports.xlsx غير موجود")
    st.stop()

df = load_data(file_path, os.path.getmtime(file_path))

# -----------------------------
# RESET BUTTON (حقيقي)
# -----------------------------
with top2:
    if st.button("🧹 تصفير الفلاتر"):
        for k in ["year","month","product","gov","dep","type","search"]:
            st.session_state[k] = "الكل" if k != "search" else ""
        st.rerun()

# -----------------------------
# SEARCH + FILTERS
# -----------------------------
st.subheader("🔍 البحث والفلاتر")

st.session_state.search = st.text_input(
    "بحث", value=st.session_state.search
)

years = ["الكل"] + sorted(df["Year"].astype(str).unique())
months = ["الكل"] + sorted(df["MonthNum"].astype(str).unique())
products = ["الكل"] + sorted(df["Product"].astype(str).unique())
govs = ["الكل"] + sorted(df["Governorate"].astype(str).unique())
deps = ["الكل"] + sorted(df["Department"].astype(str).unique())
types = ["الكل"] + sorted(df["ReportType"].astype(str).unique())

c1,c2,c3 = st.columns(3)
with c1:
    st.session_state.year = st.selectbox("السنة", years, index=years.index(st.session_state.year))
with c2:
    st.session_state.month = st.selectbox("الشهر", months, index=months.index(st.session_state.month))
with c3:
    st.session_state.product = st.selectbox("المستحضر", products, index=products.index(st.session_state.product))

c4,c5,c6 = st.columns(3)
with c4:
    st.session_state.gov = st.selectbox("المحافظة", govs, index=govs.index(st.session_state.gov))
with c5:
    st.session_state.dep = st.selectbox("القسم", deps, index=deps.index(st.session_state.dep))
with c6:
    st.session_state.type = st.selectbox("نوع التقرير", types, index=types.index(st.session_state.type))

# -----------------------------
# FILTERING
# -----------------------------
filtered = df.copy()

if st.session_state.search:
    s = st.session_state.search.lower()
    filtered = filtered[
        filtered.astype(str).apply(lambda row: row.str.lower().str.contains(s).any(), axis=1)
    ]

if st.session_state.year != "الكل":
    filtered = filtered[filtered["Year"].astype(str) == st.session_state.year]

if st.session_state.month != "الكل":
    filtered = filtered[filtered["MonthNum"].astype(str) == st.session_state.month]

if st.session_state.product != "الكل":
    filtered = filtered[filtered["Product"] == st.session_state.product]

if st.session_state.gov != "الكل":
    filtered = filtered[filtered["Governorate"] == st.session_state.gov]

if st.session_state.dep != "الكل":
    filtered = filtered[filtered["Department"] == st.session_state.dep]

if st.session_state.type != "الكل":
    filtered = filtered[filtered["ReportType"] == st.session_state.type]

# -----------------------------
# RESULTS
# -----------------------------
st.subheader(f"📊 النتائج ({len(filtered)})")

for _, row in filtered.iterrows():
    st.markdown(f"""
    **{row.get("ReportName","")}**
    
    - السنة: {row.get("Year","")}
    - الشهر: {row.get("MonthNum","")}
    - المستحضر: {row.get("Product","")}
    - المحافظة: {row.get("Governorate","")}
    - القسم: {row.get("Department","")}
    - النوع: {row.get("ReportType","")}
    """)

    if str(row.get("TeamsLink","")).startswith("http"):
        st.link_button("📂 فتح التقرير", row["TeamsLink"])

    st.divider()
