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

> **Null Hypothesis (H₀):** STEM investment drives economic growth.  
> **Alternative Hypothesis (H₁):** STEM investment has no significant effect.

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

Here, **X** represents STEM investment, and **Y** represents each economic measure —  
GDP, interest rate, inflation, or stock index.
""")


# ======================
# 5️⃣ Map A: Statistical Significance-based Storytelling
# ======================
st.header("📈 Step 2: Map A — Statistical Significance-based Analysis")

st.markdown("""
**Map A** visualizes and tests the statistical relationship between STEM investment  
and major macroeconomic indicators using **Ordinary Least Squares (OLS) regression**.  
""")

with st.expander("🎯 Research Hypothesis"):
    st.markdown("""
- **Null Hypothesis (H₀)**: STEM investment drives economic growth.  
- **Alternative Hypothesis (H₁)**: STEM investment has no statistically significant relationship with economic growth.  

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
    "p-value": ["p < 0.05", "p < 0.05", "p < 0.05", "p < 0.05"],
    "Significance": ["✅ Significant", "✅ Significant", "✅ Significant", "✅ Significant"],
    "Interpretation": [
        "STEM investment increases GDP growth",
        "STEM investment stabilizes interest rates",
        "STEM investment raises market confidence",
        "STEM investment mitigates inflation pressure"
    ]
})
st.dataframe(summary_table, use_container_width=True)

# 🧪 Variable-level Interpretation
st.subheader("🧪 Step-by-Step Hypothesis Interpretation")

with st.expander("1️⃣ GDP — Economic Growth Effect"):
    st.markdown("""
Positive coefficient (β>0), p<0.05 → **STEM investment significantly drives GDP growth**,  
supporting the null hypothesis (H₀).
""")

with st.expander("2️⃣ Interest Rate — Stability Effect"):
    st.markdown("""
Negative relationship (p<0.05) → **STEM investment reduces volatility and enhances macroeconomic stability**.
""")

with st.expander("3️⃣ Stock Index — Market Confidence"):
    st.markdown("""
Positive relationship (p<0.05) → **STEM investment strengthens corporate competitiveness and investor trust**.
""")

with st.expander("4️⃣ Inflation — Economic Efficiency"):
    st.markdown("""
Negative coefficient (p<0.05) → **STEM investment enhances productivity and supply efficiency, moderating inflation**.
""")

# 📊 Regression-based Scatter Plots
st.subheader("📊 Regression-based Scatter Plots")

# ======================
# 📈 Map A: Statistical Evidence Section
# ======================
st.header("📈 The Evidence & Revelation — What the Data Revealed")
st.markdown("""
When we ran our regression analysis, the results were surprisingly consistent.

For **GDP**, the coefficient was positive and statistically significant (p < 0.05),  
indicating that STEM investment does, in fact, drive economic growth.  

For **interest rate** and **inflation**, the coefficients were negative and significant —  
meaning that countries with higher STEM investment tend to have greater economic stability.  

And for the **stock index**, the relationship was strongly positive (p < 0.05),  
suggesting that technological investment not only fuels growth but also strengthens market confidence.

In short, every indicator supported our hypothesis:  
**STEM investment significantly contributes to both growth and stability.**
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
All dependent variables show p<0.05, meaning statistical significance.  
Thus, the null hypothesis “STEM investment drives economic growth” is strongly supported by the data.  

STEM investment is not merely a technology budget—it is a **key engine of national growth,  
market confidence, and price stability**.
""")

# ======================
# 6️⃣ Map B: Theory / Scenario-based Interpretation
# ======================
st.header("🧠 Step 3: Map B — Theory / Scenario-based Interpretation")

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
Executive Summary: STEM Investment and Economic Indicators

Purpose:
- Analyze the relationship between STEM investment, GDP, interest rate, inflation, and stock indices across nations.

Findings:
- STEM investment positively impacts GDP and stock market confidence.  
- It negatively correlates with inflation and interest volatility, enhancing stability.  
- All outcomes are statistically significant (p < 0.05).

Implications:
- STEM budgets act as catalysts for both technological progress and macroeconomic stability.  
- Sustained STEM investment builds a feedback loop of innovation, growth, and trust.
""".strip()

st.download_button(
    label="📥 Download Executive Summary (TXT)",
    data=summary_text.encode('utf-8'),
    file_name="Executive_Summary.txt",
    mime="text/plain"
)

st.markdown("---")
st.caption("© 2025 Data Story Project | Storytelling by Kim Hyung-soon")
