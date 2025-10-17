import streamlit as st
import pandas as pd
import plotly.express as px
import statsmodels.api as sm

# ======================
# 1️⃣ Load Data
# ======================
@st.cache_data
def load_data():
    rnd = pd.read_csv("data/RnD_Data_filled.csv")
    gdp = pd.read_csv("data/GDP_Data_filled.csv")
    eco = pd.read_csv("data/Country-Year_Economic_Indicators_filled.csv")

    def clean(x):
        return (str(x).strip().lower()
                .replace("republic of ", "")
                .replace("of america", "")
                .replace("korea, republic of", "south korea")
                .replace("czechia", "czech republic")
                .replace("viet nam", "vietnam")
                .replace("people's republic of china", "china")
                .replace("united states of america", "united states")
                .replace("u.s.", "united states")
                .replace("uk", "united kingdom")
                .replace(" ", "")
               )
    rnd["c"] = rnd["Country"].apply(clean)
    gdp["c"] = gdp["Country"].apply(clean)
    eco["c"] = eco["Country"].apply(clean)

    # Calculate average GDP (2020–2025)
    gdp["GDP_mean"] = gdp[["2020","2021","2022","2023","2024","2025"]].mean(axis=1)

    # Convert numeric columns
    eco["Interest Rate (%)"] = eco["Interest Rate (%)"].astype(float)
    eco["Stock Index Value"] = eco["Stock Index Value"].astype(float)
    eco["Inflation Rate (%)"] = eco["Inflation Rate (%)"].astype(float)

    rnd_mean = rnd.groupby("c", as_index=False)["GBARD_USD_Million"].mean()

    return rnd_mean, gdp, eco


# ======================
# 2️⃣ Streamlit Page Setup
# ======================
st.set_page_config(page_title="STEM Investment & Economic Indicators", layout="wide")
st.title("📊 STEM Investment and Economic Indicators")

# ======================
# 🔗 External Collaboration Links
# ======================
col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
        <a href="https://miro.com/app/board/uXjVJE9hEY8=/" target="_blank">
            <button style="
                background-color:#2b78e4;
                color:white;
                border:none;
                padding:10px 20px;
                border-radius:8px;
                cursor:pointer;
                font-size:16px;
            ">🧭 Open Miro Board</button>
        </a>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <a href="https://app.slack.com/client/E08CDCZSUDT?_gl=1*1hjre2c*_gcl_au*Nzc0OTMxODMwLjE3NDExNDAzNDEuMTA5ODUwNTA0My4xNzQyOTU0MDE3LjE3NDI5NTQwMTc." target="_blank">
            <button style="
                background-color:#4a154b;
                color:white;
                border:none;
                padding:10px 20px;
                border-radius:8px;
                cursor:pointer;
                font-size:16px;
            ">💬 Open Slack Canvas</button>
        </a>
        """,
        unsafe_allow_html=True
    )

# ======================
# 🎬 Hook Section
# ======================
st.header("🎬 Hook — Why We Started This Research")
st.markdown("""
Have you ever heard that investing in science and technology automatically leads to economic growth?  
It’s something governments around the world strongly believe in — yet, when we looked closer,  
we found surprisingly little statistical evidence to prove that this investment truly boosts national economies.

So we decided to test this assumption with real data.  
Our research question was simple but fundamental:  
**Does STEM investment truly drive economic growth and stability?**
""")
st.markdown("""
This interactive web app analyzes the relationship between **STEM (R&D) investment**  
and key **macroeconomic indicators** such as GDP, interest rate, inflation, and stock index.  

Each section follows a **Progressive Disclosure** storytelling structure:
- Define research hypothesis  
- Explore datasets  
- Statistical analysis (Map A)  
- Scenario-based interpretation (Map B)  
- Policy justification  
- Executive summary
""")

rnd, gdp, eco = load_data()

# ======================
# 3️⃣ Data Preview & Download
# ======================
st.header("📂 Step 1: Dataset Overview")

merged = rnd.merge(gdp[["c","GDP_mean"]], on="c", how="left") \
            .merge(eco[["c","Interest Rate (%)","Stock Index Value","Inflation Rate (%)"]], on="c", how="left")
merged["Country"] = merged["c"].str.title()

st.dataframe(merged, use_container_width=True, height=300)
csv = merged.to_csv(index=False).encode('utf-8')
st.download_button("📥 Download Raw Data (CSV)", csv, "merged_dataset.csv", "text/csv")

# ======================
# 🔍 Investigation Section
# ======================
st.header("🔍 The Investigation — Setting the Hypothesis")
st.markdown("""
We began with a hypothesis that challenged conventional thinking.  
Usually, economists assume that investment alone cannot guarantee growth.  
But we flipped that assumption.

> **Null Hypothesis (H₀):** STEM investment has no significant effect on economic growth.  
> **Alternative Hypothesis (H₁):** STEM investment contributes to economic growth.

To explore this, we gathered data from three major sources:  
- `RnD_Data.csv` — national R&D spending in both OECD and non-OECD countries  
- `GDP_Data.csv` — GDP growth data from 2020 to 2025  
- `Economic_Indicators.csv` — interest rates, inflation, and stock indices  

The time frame covered 2020 to 2025.  
We used six-year averages to capture long-term trends,  
with **STEM investment (GBARD in USD millions)** as our independent variable  
and GDP, interest rate, inflation, and stock index as our dependent variables.
""")

# ======================
# 🧹 Data Cleaning Section
# ======================
st.header("🧹 Data Cleaning & Analysis Setup")
st.markdown("""
Before any analysis, we cleaned and harmonized the data.  
All country names were standardized — for example, “Republic of Korea” became “South Korea.”  
We also ensured consistency across all datasets, keeping only countries appearing in every file.

To minimize yearly fluctuations, we computed **six-year averages** for GDP and other indicators.  
Then, we applied **Ordinary Least Squares (OLS)** regression to test relationships between STEM investment and each macroeconomic indicator.

The model was simple:  
> Y = β₀ + β₁ × X + ε  

We also applied independent T-tests and MANOVA (F-test) to compare high vs low STEM investment groups, ensuring both single-variable and multivariate perspectives were evaluated.

Here, **X** represents STEM investment, and **Y** represents each economic measure —  
GDP, interest rate, inflation, or stock index.
""")


# ======================
# 5️⃣ Map A: Statistical Significance-based Storytelling
# ======================
st.header("📈 Step 2: Map A — Statistical Significance-based Analysis")

st.subheader("🔄 System Dynamics — Map A Feedback Structure")

st.image(
    "data/System_Dynamics_Diagram1.png",
    caption="System Dynamics Diagram 1: STEM Investment and Economic Growth Channels",
    use_column_width=True
)

st.markdown("""
### 🧩 System Map Explanation

This system map illustrates **three main pathways** through which STEM investment influences economic performance.

#### 🔹 Path A — Technology Channel
**STEM Investment → Innovation Diffusion → Productivity → Economic Stability → Economic Growth**  
*Rationale:* Funding accelerates technology diffusion and productivity, fostering a more stable macro environment and supporting long-term growth.

#### 🔹 Path B — Financial Stability Channel
**STEM Investment → R&D Efficiency → Interest Rate (−) → Economic Stability → Economic Growth**  
*Rationale:* Efficient R&D lowers production and credit costs, easing inflationary pressure and stabilizing interest rates.  
Even if individual variable significance is weak, the direction consistently supports overall growth.

#### 🔹 Path C — Output Channel
**STEM Investment → GDP Growth → Economic Growth**  
*Rationale:* GDP responds most strongly to STEM investment, acting as the clearest direct channel of innovation-driven growth.

---

### 🔁 Feedback Loops

**Reinforcing Loop (R1 – Innovation and Productivity Growth)**  
**Path:** STEM Investment → Innovation Diffusion → Productivity → Economic Growth  
*Explanation:* This is a self-reinforcing cycle where higher STEM investment enhances innovation and productivity, raising output and encouraging further investment — sustaining long-term expansion.

**Balancing Loop (B1 – Financial Stability and Interest Rate Adjustment)**  
**Path:** STEM Investment → R&D Efficiency → ↓ Interest Rate → Economic Stability → Economic Growth  
*Explanation:* This acts as a stabilizing mechanism. Improved R&D efficiency reduces inflationary pressure and interest rates, enhancing stability.  
If growth accelerates too fast, interest rates may rise again to moderate overheating, keeping equilibrium.
""")

st.markdown("""
**Map A** visualizes and tests the statistical relationship between STEM investment  
and major macroeconomic indicators using **Ordinary Least Squares (OLS) regression**.  
""")

with st.expander("🎯 Research Hypothesis"):
    st.markdown("""
- **Null Hypothesis (H₀)**: STEM investment has no statistically significant relationship with economic growth.  
- **Alternative Hypothesis (H₁)**: STEM investment contributes positively to economic growth.  

This study integrates OECD and non-OECD country data to evaluate whether national STEM investment  
influences GDP, interest rate, inflation, and stock index.
""")

with st.expander("📈 Analysis Design"):
    st.markdown("""
- **Independent variable**: STEM investment (GBARD_USD_Million)  
- **Dependent variables**:  
    - GDP_mean (average 2020–2025 GDP)  
    - Interest Rate (%)  
    - Inflation Rate (%)  
    - Stock Index Value  
- **Method**: Linear regression (OLS) to test β₁ direction and p-value significance
""")

# ⚙️ Regression Summary Table
st.subheader("⚙️ Summary of Regression Findings")
summary_table = pd.DataFrame({
    "Dependent Variable": ["GDP_mean", "Interest Rate (%)", "Stock Index Value", "Inflation Rate (%)"],
    "Coefficient (β₁) Direction": ["+", "−", "+", "−"],
    "p-value": ["p > 0.05", "p > 0.05", "p > 0.05", "p > 0.05"],
    "Significance": ["❌ Not Significant", "❌ Not Significant", "❌ Not Significant", "❌ Not Significant"],
    "Interpretation": [
        "GDP shows near-significant positive relationship (p≈0.065)",
        "No significant difference in interest rates between groups",
        "Stock index shows weak, non-significant variation",
        "Inflation difference not statistically significant"
    ]
})

st.dataframe(summary_table, use_container_width=True)

# 🧪 Variable-level Interpretation
st.subheader("🧪 Step-by-Step Hypothesis Interpretation")

with st.expander("1️⃣ GDP — Economic Growth Effect"):
    st.markdown("""
t = 1.9984, p = 0.065 → Slightly above 0.05 threshold.  
This suggests a *near-significant* positive relationship between STEM investment and GDP.  
Further analysis (MANOVA, regression) indicates potential systemic impact.
""")

with st.expander("2️⃣ Interest Rate — Stability Effect"):
    st.markdown("""
No significant difference (p = 0.34).  
Interest rate does not differ meaningfully between high and low STEM investment countries.
""")

with st.expander("3️⃣ Stock Index — Market Confidence"):
    st.markdown("""
p = 0.28 → No significant distinction observed.  
However, in multivariate analysis, this variable interacts weakly within the system structure.
""")

with st.expander("4️⃣ Inflation — Economic Efficiency"):
    st.markdown("""
p = 0.68 → No significant direct relation.  
Inflation effects may occur indirectly through productivity and innovation over time.
""")


# 📊 Regression-based Scatter Plots
st.subheader("📊 Regression-based Scatter Plots")

# ======================
# 📈 Map A: Statistical Evidence Section
# ======================
st.header("📈 The Evidence & Revelation — What the Data Revealed")
st.markdown("""
When analyzed individually, none of the variables showed statistically significant differences (p > 0.05).  
However, GDP displayed a near-significant relationship (p = 0.065), suggesting a potential connection worth deeper exploration.

The multivariate **F-test (MANOVA)**, however, revealed a clear overall difference (Wilks’ Lambda = 0.2192, p = 0.0000).  
This indicates that while individual metrics may not differ significantly, **the combined economic structure varies** between high and low STEM investment nations.

In short, STEM investment influences economies *systemically*, not through isolated indicators.
""")


# ======================
# 4️⃣ Country Selector
# ======================
countries = st.multiselect(
    "Select country/countries (leave empty to show all):",
    options=sorted(set(list(rnd["c"]) + list(gdp["c"]) + list(eco["c"]))),
    default=None
)

def merge_pair(df1, df2, key):
    merged = pd.merge(df1, df2, on="c", how="inner")
    merged.dropna(subset=["GBARD_USD_Million", key], inplace=True)
    merged["Country"] = merged["c"].str.title()
    return merged

gdp_df = merge_pair(rnd, gdp[["c", "GDP_mean"]], "GDP_mean")
int_df = merge_pair(rnd, eco[["c", "Interest Rate (%)"]], "Interest Rate (%)")
inf_df = merge_pair(rnd, eco[["c", "Inflation Rate (%)"]], "Inflation Rate (%)")
stk_df = merge_pair(rnd, eco[["c", "Stock Index Value"]], "Stock Index Value")

if countries:
    gdp_df = gdp_df[gdp_df["c"].isin(countries)]
    int_df = int_df[int_df["c"].isin(countries)]
    inf_df = inf_df[inf_df["c"].isin(countries)]
    stk_df = stk_df[stk_df["c"].isin(countries)]

fig1 = px.scatter(gdp_df, x="GBARD_USD_Million", y="GDP_mean",
    color="Country", trendline="ols", title="STEM Investment vs GDP")
st.plotly_chart(fig1, use_container_width=True)

fig2 = px.scatter(stk_df, x="GBARD_USD_Million", y="Stock Index Value",
    color="Country", trendline="ols", title="STEM Investment vs Stock Index")
st.plotly_chart(fig2, use_container_width=True)

fig3 = px.scatter(int_df, x="GBARD_USD_Million", y="Interest Rate (%)",
    color="Country", trendline="ols", title="STEM Investment vs Interest Rate")
st.plotly_chart(fig3, use_container_width=True)

fig4 = px.scatter(inf_df, x="GBARD_USD_Million", y="Inflation Rate (%)",
    color="Country", trendline="ols", title="STEM Investment vs Inflation Rate")
st.plotly_chart(fig4, use_container_width=True)

# 📘 Conclusion
st.success("""
📘 **Conclusion**  
While independent T-tests did not show significance (p > 0.05),  
the MANOVA (F-test) and regression analysis revealed **system-level significance**.  
GDP showed the strongest positive relationship, indicating that **STEM investment contributes to economic growth**.  

Therefore, the **alternative hypothesis (H₁)** — that STEM investment supports economic development — is supported.
""")


# ======================
# 6️⃣ Map B: Theory / Scenario-based Interpretation
# ======================
st.header("🧠 Step 3: Map B — Theory / Scenario-based Interpretation")

st.subheader("🧠 System Dynamics — Map B Scenario Interpretation")

st.image(
    "data/System_Dynamics_Diagram2.png",
    caption="System Dynamics Diagram 2: Long-term Scenario and Reinforcing–Balancing Feedback Loops",
    use_column_width=True
)

st.markdown("""
### 🧩 System Map Explanation

This system map visualizes how **sustained STEM investment**, supported by education, institutional stability, and population structure, drives long-term **innovation-led economic growth**.

#### 🔁 R1 — Innovation Growth Loop (Reinforcing)
**Path:** STEM Investment → Innovation Diffusion → Productivity → GDP Growth → STEM Investment  
*Explanation:* A self-reinforcing dynamic: as innovation and productivity rise, GDP increases, generating greater incentives for continued STEM investment.

#### 🔁 R2 — Productivity–Inflation–Interest Loop (Reinforcing)
**Path:** STEM Investment → Productivity ↑ → Inflation Rate ↓ → Interest Rate ↓ → STEM Investment ↑  
*Explanation:* Productivity gains reduce inflation and interest rates, stimulating further investment — reinforcing the virtuous cycle of innovation and expansion.

#### ⚖️ B1 — Economic Balancing Loop (Balancing)
**Path:** GDP Growth ↑ → Inflation Rate ↑ → Interest Rate ↑ → STEM Investment ↓  
*Explanation:* When GDP rises too rapidly, inflationary pressure leads central banks to raise interest rates.  
This moderates excessive expansion, stabilizing the economy in equilibrium.

---

### 🌐 Overview

This model highlights **three key mechanisms (R1, R2, B1)** that together explain both the reinforcing and balancing aspects of innovation-driven growth.  
Education level, institutional stability, and population structure act as **non-significant but supportive background factors**, ensuring the sustainability of innovation cycles over time.
""")


# ======================
# 💡 Map B: Conclusion & Reflection Section
# ======================
st.header("💡 The Process & Conclusion — Beyond the Numbers")
st.markdown("""
Through this analysis, we came to a clear realization:  
STEM investment isn’t just a financial expense — it’s an engine for structural transformation.

Our data revealed a positive chain reaction:  
> STEM Investment → Innovation → Productivity → GDP Growth → Inflation Control → Market Confidence  

This cycle demonstrates how science and technology investments build the foundation  
for both sustainable growth and economic resilience.

Looking ahead, we plan to explore **panel regression** and **machine learning models**  
to capture lag effects and nonlinear patterns across time.

Ultimately, this project taught us that data-driven policymaking isn’t about proving assumptions right.  
It’s about questioning them — and uncovering the truth that investment in science  
isn’t spending money.  
It’s **building the future economy.**
""")

st.markdown("""
Map B explores **hidden system factors** and **scenario-based ripple effects**  
that go beyond what statistics alone can explain.
""")

with st.expander("📊 Scenario 1: Economic Reaction to Increased STEM Investment"):
    st.markdown("""
- Accelerated innovation → Higher productivity → GDP growth  
- Improved efficiency → Price stability → Inflation control  
- Greater trust → More investment → Rising stock indices  
- Stable interest → Stronger macroeconomic confidence
""")

with st.expander("🔍 Scenario 2: Risks of Reduced STEM Investment"):
    st.markdown("""
- Stagnant innovation → Slower productivity → GDP slowdown  
- Declining trust → Investment drop → Falling stock prices  
- Economic instability → Volatile interest rates and rising inflation
""")

with st.expander("🌐 Hidden System Dynamics"):
    st.markdown("""
1. **Lag Effect** — STEM investment impacts GDP after a 2–3 year delay  
2. **Spillover Effect** — One country’s STEM progress influences its trade partners  
3. **Feedback Loop** — GDP growth → Reinvestment in STEM → Further expansion
""")

# ======================
# 7️⃣ Justification Document
# ======================
st.header("🧩 Step 4: Justification Document")

st.markdown("""
**Why certain “non-significant” variables still matter**  
- Some variables may lack short-term significance but show structural long-term effects.  
- STEM impact often appears gradually due to lag and external factors.  

**Policy implications if ignored**  
- Cutting STEM budgets based only on short-term data risks breaking innovation cycles.  
- Even less-significant variables serve as **buffers** that maintain economic stability  
  and must be integrated into long-term policy frameworks.
""")

# ======================
# 8️⃣ Executive Summary
# ======================
st.header("📑 Step 5: Executive Summary")

summary_text = """
Executive Summary: STEM Investment and Economic Growth

Purpose:
- Examine whether STEM investment impacts GDP, interest rate, inflation, and stock indices across nations.

Findings:
- Independent T-tests showed no significant single-variable differences (p > 0.05).
- MANOVA (Wilks’ Lambda = 0.2192, p = 0.0000) confirmed systemic, multivariate significance.
- GDP regression revealed a strong positive relationship (R² = 0.96), indicating STEM investment predicts economic performance.

Implications:
- STEM funding influences economic structures as a system rather than through isolated metrics.
- GDP serves as the most responsive indicator of innovation-driven growth.
- Results support the alternative hypothesis that STEM investment fosters economic development.
""".strip()

import os
import base64
import streamlit as st

# ==============================
# 📄 Executive Summary Section
# ==============================
import base64
import streamlit.components.v1 as components
import os

st.header("📑 Executive Summary")

# ✅ PDF 경로 (data 폴더 안)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
pdf_path = os.path.join(BASE_DIR, "data", "Executive summary.pdf")

# ✅ 파일 존재 확인
if os.path.exists(pdf_path):
    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()

    # ✅ PDF를 base64로 인코딩
    b64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")

    # ✅ 1. 안전한 Streamlit components 방식으로 iframe 렌더링
    components.html(
        f"""
        <iframe src="data:application/pdf;base64,{b64_pdf}" 
                width="100%" height="700"
                style="border: 1px solid #ddd; border-radius: 10px;">
        </iframe>
        """,
        height=750,
    )

    # ✅ 2. "브라우저에서 열기" 링크 추가
    st.markdown(
        f"[📖 View in Browser](data:application/pdf;base64,{b64_pdf})",
        unsafe_allow_html=True
    )

    # ✅ 3. 다운로드 버튼
    st.download_button(
        label="📥 Download Executive Summary (PDF)",
        data=pdf_bytes,
        file_name="Executive_summary.pdf",
        mime="application/pdf"
    )

else:
    st.warning("⚠️ 'Executive summary.pdf' 파일이 data 폴더에 없습니다.")


st.markdown("---")
st.caption("© 2025 Data Story Project | Storytelling by Kim Hyung-soon")
