
from datetime import date

import pandas as pd
import plotly.express as px
import requests
import streamlit as st


st.set_page_config(
    page_title="NASA Crop Rotation Advisor",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "lang" not in st.session_state:
    st.session_state.lang = "en"
if "farm_lat" not in st.session_state:
    st.session_state.farm_lat = 30.58
if "farm_lon" not in st.session_state:
    st.session_state.farm_lon = 31.01
if "farm_location" not in st.session_state:
    st.session_state.farm_location = "nile_delta"
period_end_year = date.today().year - 1
period_start_year = period_end_year - 2

FARM_LOCATIONS = {
    "nile_delta": (30.58, 31.01),
    "central_valley": (36.74, -119.77),
    "punjab": (31.52, 74.36),
}


TEXTS = {
    "en": {
        "eyebrow": "NASA POWER · AGRICULTURE INTELLIGENCE",
        "title": "Crop Rotation Advisor",
        "description": "Satellite-informed insights to help you plan resilient seasons and healthier soil.",
        "sidebar_header": "Farm profile",
        "sidebar_hint": "Set your farm location and growing priorities.",
        "section_location": "Farm location",
        "section_crops": "Soil & crop",
        "location_preset": "Quick location",
        "locations": {
            "custom": "Custom coordinates",
            "nile_delta": "Nile Delta · Egypt",
            "central_valley": "Central Valley · USA",
            "punjab": "Punjab · Pakistan",
        },
        "coordinate_hint": "Choose a region or enter precise farm coordinates.",
        "profile_status": "Farm profile ready",
        "profile_status_hint": "Location and crop preferences are set",
        "priority_hint": "Recommendations will be ordered around your top goal.",
        "sidebar_footer": "Climate insights for better growing decisions",
        "latitude": "Latitude",
        "longitude": "Longitude",
        "soil": "Dominant soil type",
        "crop": "Current main crop",
        "priority": "Your top priority",
        "soil_types": ["Clay", "Sandy", "Loamy"],
        "crops": [
            "Wheat",
            "Maize",
            "Faba bean / Legumes",
            "Clover / Cover crop",
            "Sorghum",
            "Sunflower",
        ],
        "priorities": [
            "Water conservation & drought resistance",
            "Soil health & fertilizer reduction",
            "Income diversification",
        ],
        "analyze": "Refresh farm analysis",
        "loading": "Retrieving monthly observations from NASA POWER…",
        "dashboard": "Farm intelligence",
        "period": "Historical monthly observations · {}–{}",
        "avg_temp": "Mean air temperature",
        "soil_moisture": "Surface soil moisture",
        "evap": "Evapotranspiration",
        "rain": "Mean precipitation",
        "statistics_title": "Statistical summary",
        "observations": "Monthly observations",
        "heat_months": "Hot months (>30 °C)",
        "rain_variability": "Precipitation variability (CV)",
        "temperature_trend": "Mean temperature · latest 12 months",
        "vs_previous_year": "°C vs previous 12 months",
        "risk_title": "Climate signals",
        "heat_risk": "Heat signal",
        "moisture_risk": "Moisture signal",
        "heat_high": "Elevated",
        "heat_moderate": "Moderate",
        "moisture_low": "Low",
        "moisture_ok": "Watch",
        "risk_note": "Screening indicators only — interpret with local conditions.",
        "charts_title": "Seasonal climate patterns",
        "tab_climate": "Temperature & moisture",
        "tab_water": "Water balance",
        "tab_seasonal": "Monthly averages",
        "temperature_chart": "Monthly temperature and soil moisture",
        "water_chart": "Precipitation and evapotranspiration",
        "seasonal_chart": "Typical conditions by calendar month",
        "temperature": "Temperature (°C)",
        "moisture": "Soil moisture",
        "precipitation": "Precipitation (mm/day)",
        "evap_axis": "Evapotranspiration (mm/day)",
        "month": "Month",
        "strategies_title": "Rotation strategies",
        "strategies_hint": "Options are ordered around your selected priority; validate locally before planting.",
        "recommended": "Priority match",
        "benchmark": "Baseline",
        "sequence": "Crop sequence",
        "rationale": "Why it may fit",
        "evidence": "Climate context",
        "benefits": "Potential benefits",
        "risks": "Considerations",
        "gaps": "Before implementation",
        "current_title": "Current practice benchmark",
        "fallow": "fallow",
        "current_why": "A baseline for comparing the alternative rotation approaches.",
        "current_benefits": "Uses familiar crops and existing farm routines.",
        "current_risks": "Repeated crops can increase pest pressure and nutrient depletion.",
        "current_gaps": "Review fertilizer use, pest history, and local yields.",
        "water_title": "Water & heat resilience",
        "water_sequence": "Sorghum → faba bean → sunflower",
        "water_why": "A diversified sequence intended to balance water demand and seasonal exposure.",
        "water_benefits": "Adds crop diversity and may help manage dry-season risk.",
        "water_risks": "Water savings and market returns depend on local varieties and practice.",
        "water_gaps": "Confirm irrigation needs, planting windows, and market access locally.",
        "soil_title": "Soil renewal & cover",
        "soil_sequence": "Wheat → clover cover → maize",
        "soil_why": "Includes a legume cover crop to reduce bare-soil periods and support soil structure.",
        "soil_benefits": "Legumes can contribute nitrogen when properly managed.",
        "soil_risks": "Cover crops still need water and careful termination timing.",
        "soil_gaps": "Use a soil test and local advice to plan nutrient management.",
        "history_title": "Observation data",
        "history_hint": "Review or export the monthly NASA POWER observations used in this dashboard.",
        "download": "Download observations (CSV)",
        "table_date": "Month",
        "table_temp": "Temperature (°C)",
        "table_rain": "Precipitation (mm/day)",
        "table_moisture": "Soil moisture",
        "table_evap": "Evapotranspiration (mm/day)",
        "data_source": "Source: NASA POWER monthly point data · Coordinates",
        "disclaimer": "Decision support, not a planting prescription. Confirm recommendations with local agronomists, field observations, and soil tests.",
        "language_button": "العربية",
        "no_data": "No usable observations were returned for this location. Check the coordinates and try again.",
        "range_error": "Latitude must be between −90 and 90; longitude must be between −180 and 180.",
        "request_error": "NASA POWER request failed. Check your connection and try again.",
        "months": [
            "Jan", "Feb", "Mar", "Apr", "May", "Jun",
            "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
        ],
    },
    "ar": {
        "eyebrow": "ناسا باور · ذكاء زراعي",
        "title": "مستشار الدورة الزراعية",
        "description": "رؤى مستندة إلى رصد الأقمار الصناعية لمساعدتك في تخطيط مواسم أكثر مرونة وتربة أكثر صحة.",
        "sidebar_header": "ملف المزرعة",
        "sidebar_hint": "حدد موقع مزرعتك وأولوياتك الزراعية.",
        "section_location": "موقع المزرعة",
        "section_crops": "التربة والمحصول",
        "location_preset": "مواقع سريعة",
        "locations": {
            "custom": "إحداثيات مخصصة",
            "nile_delta": "دلتا النيل · مصر",
            "central_valley": "الوادي الأوسط · أمريكا",
            "punjab": "البنجاب · باكستان",
        },
        "coordinate_hint": "اختر منطقة أو أدخل إحداثيات المزرعة بدقة.",
        "profile_status": "ملف المزرعة جاهز",
        "profile_status_hint": "تم تحديد الموقع وتفضيلات المحاصيل",
        "priority_hint": "ستُرتب التوصيات وفق هدفك الأساسي.",
        "sidebar_footer": "رؤى مناخية لقرارات زراعية أفضل",
        "latitude": "خط العرض",
        "longitude": "خط الطول",
        "soil": "نوع التربة الغالب",
        "crop": "المحصول الرئيسي الحالي",
        "priority": "أولويتك القصوى",
        "soil_types": ["طينية", "رملية", "طميية"],
        "crops": [
            "قمح",
            "ذرة شامية",
            "فول بلدي / بقوليات",
            "برسيم / محصول غطاء",
            "ذرة رفيعة",
            "عباد الشمس",
        ],
        "priorities": [
            "ترشيد المياه ومقاومة الجفاف",
            "تحسين التربة وتقليل الأسمدة",
            "تنويع الدخل",
        ],
        "analyze": "تحديث تحليل المزرعة",
        "loading": "جارٍ استرجاع الرصد الشهري من ناسا باور…",
        "dashboard": "ذكاء المزرعة",
        "period": "رصد شهري تاريخي · {}–{}",
        "avg_temp": "متوسط حرارة الهواء",
        "soil_moisture": "رطوبة سطح التربة",
        "evap": "البخر-نتح",
        "rain": "متوسط الهطول",
        "statistics_title": "ملخص إحصائي",
        "observations": "عدد الرصدات الشهرية",
        "heat_months": "أشهر حارة (>30 °م)",
        "rain_variability": "تذبذب الهطول (معامل الاختلاف)",
        "temperature_trend": "متوسط الحرارة · آخر 12 شهراً",
        "vs_previous_year": "°م مقارنة بالـ12 شهراً السابقة",
        "risk_title": "مؤشرات المناخ",
        "heat_risk": "مؤشر الحرارة",
        "moisture_risk": "مؤشر الرطوبة",
        "heat_high": "مرتفع",
        "heat_moderate": "معتدل",
        "moisture_low": "منخفض",
        "moisture_ok": "يحتاج متابعة",
        "risk_note": "مؤشرات استرشادية فقط — تُفسر وفق الظروف المحلية.",
        "charts_title": "الأنماط المناخية الموسمية",
        "tab_climate": "الحرارة والرطوبة",
        "tab_water": "التوازن المائي",
        "tab_seasonal": "المتوسطات الشهرية",
        "temperature_chart": "الحرارة ورطوبة التربة شهرياً",
        "water_chart": "الهطول والبخر-نتح",
        "seasonal_chart": "الظروف المعتادة حسب الشهر",
        "temperature": "الحرارة (°م)",
        "moisture": "رطوبة التربة",
        "precipitation": "الهطول (مم/يوم)",
        "evap_axis": "البخر-نتح (مم/يوم)",
        "month": "الشهر",
        "strategies_title": "استراتيجيات الدورة الزراعية",
        "strategies_hint": "رتبت الخيارات وفق أولويتك؛ تحقق من ملاءمتها محلياً قبل الزراعة.",
        "recommended": "الأقرب لأولويتك",
        "benchmark": "خط أساس",
        "sequence": "تتابع المحاصيل",
        "rationale": "لماذا قد تناسبك",
        "evidence": "السياق المناخي",
        "benefits": "فوائد محتملة",
        "risks": "اعتبارات",
        "gaps": "قبل التنفيذ",
        "current_title": "مقارنة بالممارسة الحالية",
        "fallow": "بور",
        "current_why": "خط أساس لمقارنة أساليب الدورة الزراعية البديلة.",
        "current_benefits": "تعتمد على محاصيل مألوفة وإجراءات المزرعة الحالية.",
        "current_risks": "قد يزيد تكرار المحاصيل من ضغط الآفات واستنزاف العناصر الغذائية.",
        "current_gaps": "راجع استخدام الأسمدة وتاريخ الآفات والمحصول المحلي.",
        "water_title": "المرونة أمام الجفاف والحرارة",
        "water_sequence": "ذرة رفيعة ← فول بلدي ← عباد الشمس",
        "water_why": "تتابع متنوع يستهدف موازنة الطلب على المياه والتعرض الموسمي.",
        "water_benefits": "يعزز تنوع المحاصيل وقد يساعد في إدارة مخاطر الجفاف.",
        "water_risks": "يتوقف توفير المياه والعائد على الأصناف والممارسات المحلية.",
        "water_gaps": "تحقق محلياً من احتياجات الري ومواعيد الزراعة وفرص التسويق.",
        "soil_title": "تجديد التربة والغطاء النباتي",
        "soil_sequence": "قمح ← غطاء برسيم ← ذرة شامية",
        "soil_why": "يضيف محصول غطاء بقولي لتقليل فترات انكشاف التربة ودعم بنيتها.",
        "soil_benefits": "قد تسهم البقوليات في إضافة النيتروجين عند إدارتها بشكل سليم.",
        "soil_risks": "تحتاج محاصيل الغطاء إلى الماء وتوقيت مناسب لإنهائها.",
        "soil_gaps": "استخدم تحليل التربة واستشارة محلية لتخطيط إدارة العناصر الغذائية.",
        "history_title": "بيانات الرصد",
        "history_hint": "راجع أو نزّل بيانات الرصد الشهرية من ناسا باور المستخدمة في لوحة المعلومات.",
        "download": "تنزيل بيانات الرصد (CSV)",
        "table_date": "الشهر",
        "table_temp": "الحرارة (°م)",
        "table_rain": "الهطول (مم/يوم)",
        "table_moisture": "رطوبة التربة",
        "table_evap": "البخر-نتح (مم/يوم)",
        "data_source": "المصدر: بيانات ناسا باور الشهرية للنقطة · الإحداثيات",
        "disclaimer": "أداة لدعم القرار وليست وصفة زراعية. تحقق من التوصيات مع المهندسين الزراعيين المحليين والمشاهدة الحقلية وتحليل التربة.",
        "language_button": "English",
        "no_data": "لم يتم استرجاع بيانات رصد صالحة لهذا الموقع. تحقق من الإحداثيات وحاول مجدداً.",
        "range_error": "يجب أن يكون خط العرض بين ‎−90 و90 وخط الطول بين ‎−180 و180.",
        "request_error": "تعذر الاتصال بناسا باور. تحقق من الاتصال وحاول مجدداً.",
        "months": [
            "يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو",
            "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر",
        ],
    },
}

t = TEXTS[st.session_state.lang]
is_arabic = st.session_state.lang == "ar"
direction = "rtl" if is_arabic else "ltr"
alignment = "right" if is_arabic else "left"
theme = {
    "background": "#0b1220",
    "surface": "#111c2e",
    "surface_alt": "#17243a",
    "text": "#e6edf7",
    "muted": "#9baac0",
    "border": "#25344a",
    "accent": "#36c99a",
    "plot": "#111c2e",
    "grid": "#25344a",
}

st.markdown(
    f"""
    <style>
    :root {{
        color-scheme: dark;
    }}
    .stApp {{
        background: {theme["background"]};
        color: {theme["text"]};
    }}
    [data-testid="stHeader"] {{ background: transparent; }}
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #101b2c 0%, {theme["surface"]} 42%, #0e1929 100%);
        border-inline-end: 1px solid {theme["border"]};
    }}
    [data-testid="stSidebar"] > div:first-child {{
        padding: 1.2rem 1rem 1.4rem;
    }}
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {{
        line-height: 1.55;
    }}
    .sidebar-brand {{
        display: flex;
        align-items: center;
        gap: 0.8rem;
        padding: 1rem;
        margin: 0.2rem 0 1rem;
        border: 1px solid {theme["border"]};
        border-radius: 18px;
        background: linear-gradient(140deg, #193145, {theme["surface"]} 72%);
        box-shadow: 0 10px 24px rgba(0, 0, 0, 0.14);
    }}
    .sidebar-brand-icon {{
        display: grid;
        place-items: center;
        width: 42px;
        height: 42px;
        flex: 0 0 42px;
        border-radius: 13px;
        background: linear-gradient(145deg, #1d7b69, #145248);
        font-size: 1.35rem;
        box-shadow: inset 0 0 0 1px rgba(115, 235, 198, 0.2);
    }}
    .sidebar-brand-title {{
        color: {theme["text"]};
        font-size: 1rem;
        font-weight: 750;
    }}
    .sidebar-brand-caption {{
        color: {theme["muted"]};
        font-size: 0.74rem;
        margin-top: 0.12rem;
    }}
    .sidebar-section {{
        color: {theme["text"]};
        font-size: 0.91rem;
        font-weight: 700;
        margin: 1rem 0 0.3rem;
        padding-bottom: 0.45rem;
        border-bottom: 1px solid {theme["border"]};
    }}
    .sidebar-status {{
        border: 1px solid #236253;
        border-radius: 13px;
        background: linear-gradient(120deg, #14332f, #122a2b);
        padding: 0.75rem 0.85rem;
        margin: 0.75rem 0 0.9rem;
    }}
    .sidebar-status-title {{
        color: #84e2bd;
        font-size: 0.82rem;
        font-weight: 750;
    }}
    .sidebar-status-hint {{
        color: #a4cabb;
        font-size: 0.72rem;
        margin-top: 0.15rem;
    }}
    .sidebar-help {{
        color: {theme["muted"]};
        font-size: 0.74rem;
        margin: -0.3rem 0 0.45rem;
    }}
    .sidebar-footer {{
        border-top: 1px solid {theme["border"]};
        color: {theme["muted"]};
        font-size: 0.72rem;
        line-height: 1.5;
        padding-top: 0.75rem;
        margin-top: 0.6rem;
    }}
    [data-testid="stSidebar"] [data-testid="stNumberInput"] input {{
        border-radius: 11px;
        min-height: 2.65rem;
        background: #0c1726;
        border-color: {theme["border"]};
    }}
    [data-testid="stSidebar"] [data-testid="stSelectbox"] [data-baseweb="select"] > div {{
        border-radius: 11px;
        min-height: 2.65rem;
        background: #0c1726;
        border-color: {theme["border"]};
    }}
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {{
        color: #b7c5d8;
        font-size: 0.78rem;
        font-weight: 600;
        margin-bottom: 0.25rem;
    }}
    [data-testid="stSidebar"] [data-testid="stRadio"] > div {{
        gap: 0.42rem;
    }}
    [data-testid="stSidebar"] [data-testid="stRadio"] label {{
        padding: 0.58rem 0.7rem;
        border: 1px solid {theme["border"]};
        border-radius: 11px;
        background: rgba(23, 36, 58, 0.72);
        transition: border-color 120ms ease, background 120ms ease;
    }}
    [data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {{
        border-color: {theme["accent"]};
        background: linear-gradient(110deg, #153b35, #172b39);
        box-shadow: inset 0 0 0 1px rgba(54, 201, 154, 0.12);
    }}
    [data-testid="stSidebar"] .stButton > button {{
        border-radius: 12px;
        min-height: 2.85rem;
        font-weight: 700;
    }}
    [data-testid="stSidebar"] [data-testid="stButton"]:first-of-type button[kind="primary"] {{
        box-shadow: 0 7px 18px rgba(54, 201, 154, 0.15);
    }}
    [data-testid="stSidebar"] [data-testid="stHorizontalBlock"] {{
        gap: 0.65rem;
    }}
    [data-testid="stAppViewContainer"] .main .block-container {{
        max-width: 1500px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }}
    html, body, [class*="css"], [data-testid="stMarkdownContainer"] {{
        direction: {direction};
        text-align: {alignment};
    }}
    h1, h2, h3, p, label {{ text-align: {alignment}; }}
    h1, h2, h3 {{ color: {theme["text"]}; letter-spacing: -0.025em; }}
    [data-testid="stMetric"] {{
        background: {theme["surface"]};
        border: 1px solid {theme["border"]};
        border-radius: 16px;
        padding: 1.15rem 1.2rem;
        min-height: 126px;
    }}
    [data-testid="stMetricLabel"] p {{
        color: {theme["muted"]};
        font-size: 0.88rem;
        font-weight: 600;
    }}
    [data-testid="stMetricValue"] {{
        color: {theme["text"]};
        font-size: clamp(1.45rem, 2vw, 2rem);
    }}
    .hero {{
        background: linear-gradient(120deg, {theme["surface"]}, {theme["surface_alt"]});
        border: 1px solid {theme["border"]};
        border-radius: 22px;
        padding: 1.8rem 2rem;
        margin: 0.5rem 0 1.6rem;
    }}
    .eyebrow {{
        color: {theme["accent"]};
        font-size: 0.76rem;
        font-weight: 800;
        letter-spacing: 0.12em;
        margin-bottom: 0.5rem;
    }}
    .hero h1 {{ margin: 0; font-size: clamp(2rem, 4vw, 3.2rem); }}
    .hero p {{ color: {theme["muted"]}; margin: 0.65rem 0 0; font-size: 1.05rem; }}
    .section-note {{ color: {theme["muted"]}; margin-top: -0.45rem; }}
    .risk-card {{
        border: 1px solid {theme["border"]};
        border-radius: 16px;
        background: {theme["surface"]};
        padding: 1.1rem 1.2rem;
        min-height: 112px;
    }}
    .risk-label {{ color: {theme["muted"]}; font-size: 0.88rem; }}
    .risk-value {{ color: {theme["text"]}; font-size: 1.45rem; font-weight: 750; margin-top: 0.45rem; }}
    .risk-footnote {{ color: {theme["muted"]}; font-size: 0.8rem; margin-top: 0.7rem; }}
    .strategy-tag {{
        color: {theme["accent"]};
        border: 1px solid {theme["accent"]};
        border-radius: 999px;
        display: inline-block;
        font-size: 0.72rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        padding: 0.2rem 0.55rem;
    }}
    [data-testid="stVerticalBlockBorderWrapper"] {{
        border-color: {theme["border"]};
        border-radius: 16px;
        background: {theme["surface"]};
    }}
    .stButton > button, .stDownloadButton > button {{
        border-radius: 10px;
        font-weight: 650;
        min-height: 2.7rem;
    }}
    div[data-baseweb="tab-list"] {{ gap: 0.5rem; }}
    button[data-baseweb="tab"] {{ border-radius: 10px; }}
    hr {{ border-color: {theme["border"]}; }}
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data(ttl=3600)
def fetch_nasa_power_data(lat: float, lon: float, start_year: int, end_year: int):
    url = "https://power.larc.nasa.gov/api/temporal/monthly/point"
    params = {
        "parameters": "T2M,PRECTOTCORR,GWETTOP,EVPTRNS",
        "community": "AG",
        "longitude": lon,
        "latitude": lat,
        "start": start_year,
        "end": end_year,
        "format": "JSON",
    }

    response = requests.get(url, params=params, timeout=20)
    response.raise_for_status()
    properties = response.json()["properties"]["parameter"]
    records = []
    for date_key, temperature in properties["T2M"].items():
        if date_key.endswith("13"):
            continue
        month = int(date_key[4:])
        records.append(
            {
                "Date": f"{date_key[:4]}-{month:02d}",
                "Month": month,
                "Temp_C": temperature,
                "Rain_mm": properties["PRECTOTCORR"][date_key],
                "Soil_Moisture": properties["GWETTOP"][date_key],
                "Evap_mm": properties["EVPTRNS"][date_key],
            }
        )
    df = pd.DataFrame(records)
    if df.empty:
        return df
    numeric_columns = ["Temp_C", "Rain_mm", "Soil_Moisture", "Evap_mm"]
    df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors="coerce")
    return df[df["Temp_C"] > -100].dropna(subset=numeric_columns).sort_values("Date")


def chart_layout(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor=theme["plot"],
        plot_bgcolor=theme["plot"],
        font={"color": theme["text"], "family": "Arial, sans-serif"},
        title={"x": 0.02, "xanchor": "left", "font": {"size": 16}},
        margin={"l": 18, "r": 18, "t": 58, "b": 18},
        legend={"orientation": "h", "yanchor": "bottom", "y": 1.02, "x": 0},
        hovermode="x unified",
    )
    fig.update_xaxes(showgrid=False, linecolor=theme["border"])
    fig.update_yaxes(gridcolor=theme["grid"], zerolinecolor=theme["grid"])
    return fig


def apply_location_preset():
    coordinates = FARM_LOCATIONS.get(st.session_state.farm_location)
    if coordinates is not None:
        st.session_state.farm_lat, st.session_state.farm_lon = coordinates


def mark_location_custom():
    st.session_state.farm_location = "custom"


with st.sidebar:
    st.markdown(
        f"""
        <div class="sidebar-brand">
            <div class="sidebar-brand-icon">🌱</div>
            <div>
                <div class="sidebar-brand-title">{t["sidebar_header"]}</div>
                <div class="sidebar-brand-caption">NASA POWER · FARM PROFILE</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption(t["sidebar_hint"])
    st.markdown(f'<div class="sidebar-section">📍 {t["section_location"]}</div>', unsafe_allow_html=True)
    st.selectbox(
        t["location_preset"],
        options=["nile_delta", "central_valley", "punjab", "custom"],
        format_func=lambda location: t["locations"][location],
        key="farm_location",
        on_change=apply_location_preset,
    )
    st.markdown(f'<div class="sidebar-help">{t["coordinate_hint"]}</div>', unsafe_allow_html=True)
    coordinate_cols = st.columns(2)
    with coordinate_cols[0]:
        lat = st.number_input(
            t["latitude"],
            min_value=-90.0,
            max_value=90.0,
            step=0.01,
            format="%.4f",
            key="farm_lat",
            on_change=mark_location_custom,
        )
    with coordinate_cols[1]:
        lon = st.number_input(
            t["longitude"],
            min_value=-180.0,
            max_value=180.0,
            step=0.01,
            format="%.4f",
            key="farm_lon",
            on_change=mark_location_custom,
        )
    st.markdown(f'<div class="sidebar-section">🌾 {t["section_crops"]}</div>', unsafe_allow_html=True)
    soil_type = st.selectbox(t["soil"], t["soil_types"])
    current_crop = st.selectbox(t["crop"], t["crops"])
    priority = st.radio(t["priority"], t["priorities"])
    st.markdown(f'<div class="sidebar-help">{t["priority_hint"]}</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="sidebar-status">
            <div class="sidebar-status-title">● {t["profile_status"]}</div>
            <div class="sidebar-status-hint">{t["profile_status_hint"]}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    analyze_btn = st.button(t["analyze"], type="primary", use_container_width=True)
    st.divider()
    if st.button(t["language_button"], use_container_width=True):
        st.session_state.lang = "ar" if not is_arabic else "en"
        st.rerun()
    st.markdown(
        f'<div class="sidebar-footer">🛰️ {t["sidebar_footer"]}</div>',
        unsafe_allow_html=True,
    )

st.markdown(
    f"""
    <div class="hero">
        <div class="eyebrow">{t["eyebrow"]}</div>
        <h1>🛰️ {t["title"]}</h1>
        <p>{t["description"]}</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.subheader(t["dashboard"])
st.caption(t["period"].format(period_start_year, period_end_year))

analysis_key = (round(lat, 4), round(lon, 4))
if analyze_btn or st.session_state.get("analysis_key") != analysis_key:
    with st.spinner(t["loading"]):
        try:
            st.session_state.nasa_df = fetch_nasa_power_data(
                lat, lon, period_start_year, period_end_year
            )
            st.session_state.analysis_error = None
        except requests.RequestException:
            st.session_state.nasa_df = None
            st.session_state.analysis_error = "request"
        except (KeyError, TypeError, ValueError):
            st.session_state.nasa_df = None
            st.session_state.analysis_error = "data"
    st.session_state.analysis_key = analysis_key

if lat < -90 or lat > 90 or lon < -180 or lon > 180:
    st.error(t["range_error"])
elif st.session_state.get("analysis_error") == "request":
    st.error(t["request_error"])
elif st.session_state.get("analysis_error") == "data":
    st.error(t["no_data"])
elif st.session_state.get("nasa_df") is None:
    st.error(t["no_data"])
else:
    df_nasa = st.session_state.nasa_df
    if df_nasa.empty:
        st.warning(t["no_data"])
    else:
        avg_temp = df_nasa["Temp_C"].mean()
        avg_moisture = df_nasa["Soil_Moisture"].mean()
        avg_evap = df_nasa["Evap_mm"].mean()
        avg_rain = df_nasa["Rain_mm"].mean()
        heat_status = t["heat_high"] if avg_temp > 25 else t["heat_moderate"]
        moisture_status = t["moisture_low"] if avg_moisture < 0.45 else t["moisture_ok"]

        metric_cols = st.columns(4)
        metric_cols[0].metric(t["avg_temp"], f"{avg_temp:.1f} °C")
        metric_cols[1].metric(t["soil_moisture"], f"{avg_moisture:.2f}")
        metric_cols[2].metric(t["evap"], f"{avg_evap:.2f} mm/day")
        metric_cols[3].metric(t["rain"], f"{avg_rain:.2f} mm/day")

        st.markdown(f"### {t['statistics_title']}")
        recent_temp = df_nasa["Temp_C"].tail(12).mean()
        previous_temp = df_nasa["Temp_C"].iloc[-24:-12].mean()
        temperature_delta = recent_temp - previous_temp if len(df_nasa) >= 24 else None
        rainfall_mean = df_nasa["Rain_mm"].mean()
        rainfall_cv = (
            df_nasa["Rain_mm"].std(ddof=0) / rainfall_mean * 100
            if rainfall_mean > 0
            else None
        )
        stats_cols = st.columns(4)
        stats_cols[0].metric(t["observations"], f"{len(df_nasa):,}")
        stats_cols[1].metric(t["heat_months"], f"{int((df_nasa['Temp_C'] > 30).sum())}")
        stats_cols[2].metric(
            t["rain_variability"],
            f"{rainfall_cv:.0f}%" if rainfall_cv is not None else "—",
        )
        stats_cols[3].metric(
            t["temperature_trend"],
            f"{recent_temp:.1f} °C",
            delta=(
                f"{temperature_delta:+.1f} {t['vs_previous_year']}"
                if temperature_delta is not None
                else None
            ),
        )

        st.markdown(f"### {t['risk_title']}")
        risk_cols = st.columns(2)
        for col, label, value in (
            (risk_cols[0], t["heat_risk"], heat_status),
            (risk_cols[1], t["moisture_risk"], moisture_status),
        ):
            col.markdown(
                f"""
                <div class="risk-card">
                    <div class="risk-label">{label}</div>
                    <div class="risk-value">{value}</div>
                    <div class="risk-footnote">{t["risk_note"]}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown(f"### {t['charts_title']}")
        chart_tabs = st.tabs([t["tab_climate"], t["tab_water"], t["tab_seasonal"]])
        with chart_tabs[0]:
            climate_fig = px.line(
                df_nasa,
                x="Date",
                y="Temp_C",
                markers=True,
                title=t["temperature_chart"],
                labels={"Date": t["table_date"], "Temp_C": t["temperature"]},
                color_discrete_sequence=["#19a974"],
            )
            climate_fig.add_scatter(
                x=df_nasa["Date"],
                y=df_nasa["Soil_Moisture"],
                name=t["moisture"],
                mode="lines",
                yaxis="y2",
                line={"color": "#4c8bf5", "width": 2},
            )
            climate_fig.update_layout(
                yaxis={"title": t["temperature"]},
                yaxis2={
                    "title": t["moisture"],
                    "overlaying": "y",
                    "side": "right",
                    "showgrid": False,
                },
            )
            st.plotly_chart(chart_layout(climate_fig), use_container_width=True)
        with chart_tabs[1]:
            water_fig = px.bar(
                df_nasa,
                x="Date",
                y=["Rain_mm", "Evap_mm"],
                barmode="group",
                title=t["water_chart"],
                labels={
                    "Date": t["table_date"],
                    "value": t["precipitation"],
                    "variable": t["precipitation"],
                    "Rain_mm": t["precipitation"],
                    "Evap_mm": t["evap_axis"],
                },
                color_discrete_sequence=["#4c8bf5", "#f0a64a"],
            )
            st.plotly_chart(chart_layout(water_fig), use_container_width=True)
        with chart_tabs[2]:
            monthly = df_nasa.groupby("Month", as_index=False).agg(
                Temp_C=("Temp_C", "mean"),
                Rain_mm=("Rain_mm", "mean"),
                Soil_Moisture=("Soil_Moisture", "mean"),
            )
            monthly["Month_name"] = monthly["Month"].map(lambda month: t["months"][month - 1])
            seasonal_fig = px.line(
                monthly,
                x="Month_name",
                y=["Temp_C", "Soil_Moisture"],
                markers=True,
                title=t["seasonal_chart"],
                labels={
                    "Month_name": t["month"],
                    "value": t["temperature"],
                    "variable": t["temperature"],
                    "Temp_C": t["temperature"],
                    "Soil_Moisture": t["moisture"],
                },
                color_discrete_sequence=["#19a974", "#4c8bf5"],
            )
            st.plotly_chart(chart_layout(seasonal_fig), use_container_width=True)

        st.markdown(f"### {t['strategies_title']}")
        st.markdown(f'<p class="section-note">{t["strategies_hint"]}</p>', unsafe_allow_html=True)
        strategies = [
            {
                "key": "water",
                "title": t["water_title"],
                "sequence": t["water_sequence"],
                "why": t["water_why"],
                "evidence": f"{t['soil_moisture']}: {avg_moisture:.2f} · {t['avg_temp']}: {avg_temp:.1f} °C",
                "benefits": t["water_benefits"],
                "risks": t["water_risks"],
                "gaps": t["water_gaps"],
            },
            {
                "key": "soil",
                "title": t["soil_title"],
                "sequence": t["soil_sequence"],
                "why": t["soil_why"],
                "evidence": f"{t['rain']}: {avg_rain:.2f} · {t['evap']}: {avg_evap:.2f}",
                "benefits": t["soil_benefits"],
                "risks": t["soil_risks"],
                "gaps": t["soil_gaps"],
            },
            {
                "key": "baseline",
                "title": t["current_title"],
                "sequence": f"{current_crop} → {current_crop} → {t['fallow']}",
                "why": t["current_why"],
                "evidence": f"{t['soil']}: {soil_type} · {t['avg_temp']}: {avg_temp:.1f} °C",
                "benefits": t["current_benefits"],
                "risks": t["current_risks"],
                "gaps": t["current_gaps"],
            },
        ]
        preferred_key = "water" if priority in (t["priorities"][0], t["priorities"][2]) else "soil"
        strategies.sort(key=lambda strategy: strategy["key"] != preferred_key)
        strategy_cols = st.columns(3)
        for index, strategy in enumerate(strategies):
            with strategy_cols[index]:
                with st.container(border=True):
                    tag = t["recommended"] if index == 0 else (
                        t["benchmark"] if strategy["key"] == "baseline" else ""
                    )
                    if tag:
                        st.markdown(f'<span class="strategy-tag">{tag}</span>', unsafe_allow_html=True)
                    st.markdown(f"#### {strategy['title']}")
                    st.markdown(f"**{t['sequence']}:**  \n{strategy['sequence']}")
                    st.markdown(f"**{t['rationale']}:** {strategy['why']}")
                    st.caption(f"🛰️ {strategy['evidence']}")
                    st.markdown(f"**{t['benefits']}:** {strategy['benefits']}")
                    st.markdown(f"**{t['risks']}:** {strategy['risks']}")
                    st.caption(f"**{t['gaps']}:** {strategy['gaps']}")

        st.markdown(f"### {t['history_title']}")
        st.caption(t["history_hint"])
        export_df = df_nasa.rename(
            columns={
                "Date": t["table_date"],
                "Temp_C": t["table_temp"],
                "Rain_mm": t["table_rain"],
                "Soil_Moisture": t["table_moisture"],
                "Evap_mm": t["table_evap"],
            }
        )
        st.download_button(
            t["download"],
            data=export_df.to_csv(index=False).encode("utf-8-sig"),
            file_name=f"nasa_power_farm_{lat:.4f}_{lon:.4f}.csv",
            mime="text/csv",
        )
        with st.expander(t["history_title"]):
            st.dataframe(export_df, use_container_width=True, hide_index=True)

        st.caption(f"{t['data_source']}: {lat:.4f}, {lon:.4f}")
        st.info(t["disclaimer"], icon="ℹ️")

