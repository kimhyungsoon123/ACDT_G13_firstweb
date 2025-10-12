import streamlit as st
import pandas as pd
import altair as alt

# 🌐 페이지 설정
st.set_page_config(page_title="My Data Story Website", page_icon="📊", layout="wide")

# 🎨 제목
st.title("📊 My Data Story Website")
st.subheader("Option 4: Streamlit Web App — DDDM Pitch Assignment")

st.write("""
Welcome to my interactive **data storytelling website**!  
Here, I’ll show how data can tell stories through visuals, insights, and interaction.  
Scroll down and explore 👇
""")

# --- Section 1: Sample Data
st.header("1️⃣ Data Overview")

data = {
    "Year": [2018, 2019, 2020, 2021, 2022, 2023],
    "Sales": [120, 150, 180, 210, 300, 400],
    "Profit": [30, 45, 60, 80, 110, 160],
}
df = pd.DataFrame(data)

st.dataframe(df, use_container_width=True)

# --- Section 2: Interactive Visualization
st.header("2️⃣ Interactive Chart")

chart = (
    alt.Chart(df)
    .mark_line(point=True)
    .encode(
        x="Year:O",
        y="Sales:Q",
        tooltip=["Year", "Sales", "Profit"]
    )
    .interactive()
)

st.altair_chart(chart, use_container_width=True)
st.write("💡 Try hovering over the line to see exact data values!")

# --- Section 3: Insights
st.header("3️⃣ Insights & Interpretation")
st.write("""
Between **2018 and 2023**, both sales and profit show a strong upward trend.  
The most dramatic growth occurred after **2021**, indicating possible market expansion or improved efficiency.  
""")

# --- Section 4: Upload & Analyze Your Own Data
st.header("4️⃣ Upload Your Own CSV")
uploaded_file = st.file_uploader("Upload a CSV file to visualize your own data", type=["csv"])

if uploaded_file is not None:
    user_df = pd.read_csv(uploaded_file)
    st.write("✅ Your data preview:")
    st.dataframe(user_df.head())

    st.write("📈 Try selecting numeric columns for quick plotting:")
    numeric_cols = user_df.select_dtypes(include="number").columns.tolist()
    if len(numeric_cols) >= 2:
        x_axis = st.selectbox("Select X-axis", numeric_cols)
        y_axis = st.selectbox("Select Y-axis", numeric_cols)
        chart_user = alt.Chart(user_df).mark_circle(size=80).encode(
            x=x_axis,
            y=y_axis,
            tooltip=numeric_cols
        ).interactive()
        st.altair_chart(chart_user, use_container_width=True)

# --- Section 5: Download Example Data
st.header("5️⃣ Download Example Data")
csv = df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="📥 Download Example Data (CSV)",
    data=csv,
    file_name="example_data.csv",
    mime="text/csv",
)

st.success("✅ End of Story — Thanks for exploring my data web app!")