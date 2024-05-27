import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv('car_prices.csv')

# Page header
st.header("Insights of Make")
st.markdown("Make: The manufacturer of the car (e.g., Ford, Kia, Chevrolet)")

# Drop NaN values
df.dropna(inplace=True)

# Convert 'saledate' to datetime with UTC and extract month and day
if 'saledate' in df.columns:
    try:
        df['saledate'] = pd.to_datetime(df['saledate'], utc=True)
        df['month'] = df['saledate'].dt.month
        df['day'] = df['saledate'].dt.day
    except Exception as e:
        st.error(f"Error converting 'saledate' to datetime with UTC: {e}")

# Dropdown for selecting interest option
interest_options = ['year', 'condition', 'odometer', 'mmr', 'sellingprice']
if 'month' in df.columns and 'day' in df.columns:
    interest_options += ['month', 'day']

interest = st.selectbox('Select Your Option', interest_options)

# Group by 'make' and selected interest
if interest in df.columns:
    if interest == 'year':
        grouped_df = df.groupby('make')[interest].agg(lambda x: x.mode()[0]).reset_index()
    else:
        grouped_df = df.groupby('make')[interest].mean().reset_index()

    # Display grouped data
    st.dataframe(grouped_df.head(10))

    # Bar chart for top 10
    top_10_df = grouped_df.nlargest(10, interest)
    st.plotly_chart(px.bar(top_10_df, x='make', y=interest, title=f'Top 10 {interest}', color='make'), use_container_width=True)

    # Histogram (count plot) for 'make'
    st.header("Histogram of Make")
    fig_hist = px.histogram(df, x='make', title='Distribution of Car Makes', color='make')
    st.plotly_chart(fig_hist, use_container_width=True)

    # Line chart
    st.header(f"Line Chart of Make vs. {interest}")
    fig_line = px.line(grouped_df, x='make', y=interest, title=f'Line Chart of Make vs. {interest}')
    st.plotly_chart(fig_line, use_container_width=True)

    # Bar chart
    st.header(f"Bar Chart of Make vs. {interest}")
    fig_bar = px.bar(grouped_df, x='make', y=interest, title=f'Bar Chart of Make vs. {interest}', color='make')
    st.plotly_chart(fig_bar, use_container_width=True)

    # Pie Chart (assuming categorical Y-axis)
    if df[interest].dtype == "object":
        st.header(f"Distribution of Cars by {interest}")
        fig_pie = px.pie(grouped_df, names='make', values=interest, title=f'Distribution of Cars by {interest}', color='make')
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.write(f"Pie chart not suitable for continuous Y-axis ({interest}).")

    # Metrics
    max_value = grouped_df[interest].max()
    min_value = grouped_df[interest].min()
    avg_value = round(grouped_df[interest].mean(), 1)

    col1, col2, col3 = st.columns(3)
    col1.metric(label=f'Max {interest}', value=max_value)
    col2.metric(label=f'Min {interest}', value=min_value)
    col3.metric(label=f'Avg {interest}', value=avg_value)

    # Top 10 table
    col1.markdown(f'<h2 style="text-align: center; color: #191970;">Top 10 {interest}</h2>', unsafe_allow_html=True)
    col1.dataframe(top_10_df)

    # Bottom 10 table
    bottom_10_df = grouped_df.nsmallest(10, interest)
    col2.markdown(f'<h2 style="text-align: center; color: #191970;">Bottom 10 {interest}</h2>', unsafe_allow_html=True)
    col2.dataframe(bottom_10_df)
else:
    st.error(f"Selected interest '{interest}' is not in the dataframe columns.")
