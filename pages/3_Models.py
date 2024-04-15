import streamlit as st
import pandas as pd
import plotly.express as px


df = pd.read_csv('car_prices.csv')

st.header("Insights of Model")
st.markdown("Model:The specific car model (e.g., Sorento, F-150, Camry)")

has_models_column = "model" in df.columns


interest_options = ["year", "condition", "odometer", "mmr", "sellingprice"]
interest = st.selectbox("Select Your option", interest_options)


if has_models_column:
    mydf = df.nlargest(10, interest)
    st.plotly_chart(px.bar(mydf, x="model", y=interest, title=f"Top 10 {interest}" , color = 'model'), use_container_width=True)
else:

    st.write("The 'models' column is not available in the dataset.")
feature_options = df.columns.tolist()
feature_options.remove('model')


st.header(f"Line scatter of {interest}")
fig_scatter = px.scatter(df, x='model', y=interest , color = 'model')
st.plotly_chart(fig_scatter, use_container_width=True)


if df[interest].dtype == "object":
  st.header(f"Distribution of Cars by {interest}")
  fig_pie = px.pie(df, names=interest, values=df.groupby(interest)['model'].count().reset_index()['model'])  # Count cars by interest category
  st.plotly_chart(fig_pie, use_container_width=True)
else:
  st.write(f"Pie chart not suitable for continuous Y-axis ({interest}).")

max_value = df[interest].max()
min_value = df[interest].min()
avg_value = round(df[interest].mean(), 1)

col1, col2, col3 = st.columns(3)
col1.metric(label=f"Max {interest}", value=max_value)
col2.metric(label=f"Min {interest}", value=min_value)
col3.metric(label=f"Avg {interest}", value=avg_value)


col1.markdown(f'<h2 style="text-align: center; color: #191970 ;">Top 10 {interest}</h2>', unsafe_allow_html=True)
top_df = df.nlargest(10, interest)
col1.dataframe(top_df)

col2.markdown(f'<h2 style="text-align: center; color: #191970 ;">Bottom 10 {interest}</h2>', unsafe_allow_html=True)
bottom_df = df.nsmallest(10, interest)
col2.dataframe(bottom_df)
