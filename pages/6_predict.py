import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

# Load the dataset
df = pd.read_csv('car_prices.csv')

# Drop NA values
df.dropna(inplace=True)

# Convert 'saledate' to datetime with specified format
try:
    df['saledate'] = pd.to_datetime(df['saledate'], format='%Y-%m-%d', utc=True)
    df['month'] = df['saledate'].dt.month
    df['day'] = df['saledate'].dt.day
except Exception as e:
    st.error(f"Error converting 'saledate' to datetime with UTC: {e}")

# Function to get user input
def user_input_features():
    st.header('User Input Features')
    year = st.selectbox('Year', sorted(df['year'].unique()))
    make = st.selectbox('Make', df['make'].unique())
    model = st.selectbox('Model', df['model'].unique())
    trim = st.selectbox('Trim', df['trim'].unique())
    body = st.selectbox('Body', df['body'].unique())
    transmission = st.selectbox('Transmission', df['transmission'].unique())
    state = st.selectbox('State', df['state'].unique())
    condition = st.slider('Condition', min_value=int(df['condition'].min()), max_value=int(df['condition'].max()), value=int(df['condition'].median()))
    odometer = st.number_input('Odometer', value=int(df['odometer'].median()))
    color = st.selectbox('Color', df['color'].unique())
    interior = st.selectbox('Interior', df['interior'].unique())
    
    data = {
        'year': year,
        'make': make,
        'model': model,
        'trim': trim,
        'body': body,
        'transmission': transmission,
        'state': state,
        'condition': condition,
        'odometer': odometer,
        'color': color,
        'interior': interior,
        'month': pd.to_datetime('now').month,
        'day': pd.to_datetime('now').day,
    }
    features = pd.DataFrame(data, index=[0])
    return features

input_df = user_input_features()

# Combine user input features with a small subset of the entire dataset to manage memory usage
df = pd.concat([input_df, df.head(1000)], axis=0)

# Encode categorical features
df = pd.get_dummies(df, drop_first=True)

# Separate the input features and target variable
X = df.drop(columns=['sellingprice', 'saledate'])
y = df['sellingprice'].values

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a RandomForestRegressor
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Make predictions on the test set and calculate the error
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)

# Make predictions on the user input
input_features = df.iloc[:1, :-1]
prediction = model.predict(input_features)

# Display results
st.header('Heatmap of Numerical Features')
numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
plt.figure(figsize=(10, 8))
sns.heatmap(df[numeric_cols].corr(), annot=True, cmap='coolwarm')
st.pyplot(plt)

st.subheader('User Input Features')
st.write(input_df)

st.subheader('Prediction Results')
st.write(f"Predicted Selling Price: ${prediction[0]:,.2f}")
st.write(f"Model Mean Absolute Error: ${mae:,.2f}")
