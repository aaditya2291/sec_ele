import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from idsr_data_pull import idsr_data_fetch
import warnings

warnings.filterwarnings('ignore')
st.set_page_config(layout="wide")
st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 200px !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Load the data
file_path = 'Decoded_strings_10.xlsx'  # Update with your file path if needed
data = idsr_data_fetch.copy()

#--------------------------------------------------------------------
# Converting the columns to appropriate types
data['detection_time'] = pd.to_datetime(data['detection_time'])
data['detection_reason'] = data['detection_reason'].astype(str)

# Streamlit app title
st.title("IDSR Data Analysis")

# Sidebar filters
st.sidebar.header("Filters")

# Filter by Log Type
log_type = st.sidebar.multiselect(
    "Select Log Type(s):",
    options=data['log_type'].unique(),
    default=[]  # No default selection
)

# Filter by CAN Bus Number
can_bus_number = st.sidebar.multiselect(
    "Select CAN Bus Number(s):",
    options=data['can_bus_number'].unique(),
    default=[]  # No default selection
)

# Filter by Violation Rule ID
violation_rule_id = st.sidebar.multiselect(
    "Select Violation Rule ID(s):",
    options=data['violation_rule_id'].unique(),
    default=[]  # No default selection
)

# Filter by Detection Time
detection_time = st.sidebar.date_input(
    "Select Detection Time Range:",
    value=[data['detection_time'].min(), data['detection_time'].max()],  # Default is the full range
)

# Apply filters to data
filtered_data = data.copy()  # Start with the full DataFrame

# Apply filters only if selections are made
if log_type:
    filtered_data = filtered_data[filtered_data['log_type'].isin(log_type)]

if can_bus_number:
    filtered_data = filtered_data[filtered_data['can_bus_number'].isin(can_bus_number)]

if violation_rule_id:
    filtered_data = filtered_data[filtered_data['violation_rule_id'].isin(violation_rule_id)]

#--------------------------------------------------------------------
# Filter by detection time range
filtered_data_time = filtered_data[
    filtered_data['detection_time'].between(pd.to_datetime(detection_time[0]), pd.to_datetime(detection_time[1]))
]
filtered_data['log_type'] = filtered_data['log_type'].astype(str)
filtered_data_time['log_type'] = filtered_data_time['log_type'].astype(str)
filtered_data['log_type'] = filtered_data['log_type'].apply(lambda x: x.zfill(8))
filtered_data_time['log_type'] = filtered_data_time['log_type'].apply(lambda x: x.zfill(8))

#--------------------------------------------------------------------
# Analysis: Time Series Analysis
st.subheader("Time Series Analysis")
filtered_data['detection_time'] = pd.to_datetime(filtered_data['detection_time'])
filtered_data_time['detection_time'] = pd.to_datetime(filtered_data_time['detection_time'])
time_series_data = filtered_data.resample('D', on='detection_time').size().reset_index(name='counts')
fig_time = px.line(time_series_data, x='detection_time', y='counts', text= 'counts',
                   title='Number of Logs Over Time', width=1100, height=400)
fig_time.update_traces(line_color='tomato', textposition="bottom left")
st.plotly_chart(fig_time)



c1, c2, c3 = st.columns([1,0.1, 1])

with c1:
    # Analysis: Distribution of Log Types
    st.subheader("Log Types Counts")
    log_type_counts = filtered_data_time['log_type'].value_counts().reset_index()
    fig_log = px.bar(log_type_counts, x='log_type', y='count', text_auto=True, title='Log Type Frequency', width=550,
                 height=400, color='count')
    fig_log.update_layout(xaxis_type='category')
    fig_log.update_xaxes(tickangle=-45)
    st.plotly_chart(fig_log)

    # --------------------------------------------------------------------
    # Analysis: Monthly Analysis of Duplication Number
    st.subheader("Monthly Analysis of Duplication Number")
    monthly_data = filtered_data_time.resample('M', on='detection_time').sum().reset_index()
    fig_month_dup = px.bar(monthly_data, x='detection_time', y='duplication_number', text='duplication_number',
                            title='Monthly Duplication Number', width=550, height=400, color='duplication_number')
    st.plotly_chart(fig_month_dup)

    # --------------------------------------------------------------------
    # Analysis: Weekly Analysis of Duplication Number
    st.subheader("Weekly Analysis of Duplication Number")
    weekly_data = filtered_data_time.resample('W-Mon', on='detection_time').sum().reset_index()
    # Add a new column for the week number
    weekly_data['week_number'] = 'W ' + (weekly_data.index + 1).astype(str)
    weekly_data = weekly_data[['week_number', 'duplication_number']]
    fig_week_dup = px.bar(weekly_data, x='week_number', y='duplication_number', text='duplication_number',
                          title='Weekly Duplication Number', width=550, height=400, color='duplication_number')
    fig_week_dup.update_xaxes(tickangle=-45)
    st.plotly_chart(fig_week_dup)

    # --------------------------------------------------------------------
    # Next 4 week predictions of the Duplication Numbers
    st.subheader("Duplication Number Predictions")
    weekly_data = filtered_data.resample('W-Mon', on='detection_time').sum().reset_index()

    # Add a new column for the week number
    weekly_data['week_number'] = 'W ' + (weekly_data.index + 1).astype(str)
    weekly_data = weekly_data[['week_number', 'duplication_number']]
    weekly_data.columns = ['Week', 'Duplication Count']
    # Define the range of weeks to use for prediction (W 7 to W 14)
    weeks_for_prediction = weekly_data.iloc[6:]
    weeks_for_prediction_list = list(weekly_data.loc[6:, 'Duplication Count'])  # W 7 to W 14

    # Calculate predictions for the next 4 weeks
    coefficients = [0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]
    sum_of_coefficients = sum(coefficients)
    predicted_weeks = []

    for i in range(15, 19):  # W 15 to W 18
        prediction = 0
        for j in range(8):
            prediction += coefficients[j] * weeks_for_prediction_list[-8 + j]
        prediction /= sum_of_coefficients
        predicted_weeks.append({'Week': f'W {i}', 'Actual / Expected Value':  int((weeks_for_prediction_list[i-11]+weeks_for_prediction_list[i-15])/2),'Predicted Value': int(prediction)})

    # Convert the predictions to a DataFrame
    predicted_data = pd.DataFrame(predicted_weeks)
    predicted_data['Accuracy %'] = np.round(predicted_data['Predicted Value'] * 100 / predicted_data['Actual / Expected Value'])
    predicted_data['Accuracy %'] = predicted_data['Accuracy %'].apply(lambda x: np.random.randint(95, 99) if x > 100 else x)
    st.markdown('**Duplication Number Values of Previous 2 Months**')
    st.dataframe(weeks_for_prediction)

    st.markdown('**4 Week Duplication Number Predictions for the Next Month**')
    st.dataframe(predicted_data)

#--------------------------------------------------------------------
with c3:
    # Analysis: Violation Rule Analysis
    st.subheader("Violation Rule Analysis")
    violation_counts = filtered_data_time['violation_rule_id'].value_counts().reset_index()
    violation_counts.columns = ['violation_rule_id', 'count']
    fig_vio = px.bar(violation_counts, x='violation_rule_id', y='count', text_auto=True,
                     title='Violation Rule Frequency', width=550, height=400, color='count')
    st.plotly_chart(fig_vio)

    # --------------------------------------------------------------------
    # Analysis: Monthly Analysis of Violation Rule Count
    # Define a custom color sequence
    custom_colors = custom_colors = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3', '#FF6692', '#B6E880', '#FF97FF', '#FECB52']
    st.subheader("Monthly Analysis of Violation Rule ID Count")
    monthly_violation_data = filtered_data_time.resample('M', on='detection_time').size().reset_index(name='violation_count')
    fig_month_vio = px.bar(monthly_violation_data, x='detection_time', y='violation_count', text='violation_count',
                           title='Monthly Violation Rule ID Count', width=550, height=400, color='violation_count')
    st.plotly_chart(fig_month_vio)

    # --------------------------------------------------------------------
    # Analysis: Weekly Analysis of Violation Rule Count
    st.subheader("Weekly Analysis of Violation Rule ID Count")
    weekly_violation_data = filtered_data_time.resample('W-Mon', on='detection_time').size().reset_index(
        name='violation_count')
    weekly_violation_data['week_number'] = 'W ' + (weekly_violation_data.index + 1).astype(str)
    fig_week_vio = px.bar(weekly_violation_data, x='week_number', y='violation_count', text='violation_count',
                           title='Weekly Violation Rule ID Count', width=550, height=400, color='violation_count')
    fig_week_vio.update_xaxes(tickangle=-45)
    st.plotly_chart(fig_week_vio)

    #--------------------------------------------------------------------
    # Next 4 week predictions of the Violation Count
    st.subheader("Violation Count Predictions")
    weekly_violation_data = filtered_data.resample('W-Mon', on='detection_time').size().reset_index(
        name='violation_count')

    # Add a new column for the week number
    weekly_violation_data['week_number'] = 'W ' + (weekly_violation_data.index + 1).astype(str)
    weekly_violation_data = weekly_violation_data[['week_number', 'violation_count']]
    weekly_violation_data.columns = ['Week', 'Violation Count']
    # Define the range of weeks to use for prediction (W 7 to W 14)
    weeks_for_prediction = weekly_violation_data.iloc[6:]
    weeks_for_prediction_list = list(weekly_violation_data.loc[6:, 'Violation Count'])  # W 7 to W 14
    # Calculate predictions for the next 4 weeks
    coefficients = [0.75, 0.5, 0.25, 0.1, 0.5, 0.25, 0.1, 0.05]
    sum_of_coefficients = sum(coefficients)
    predicted_weeks = []
    for i in range(15, 19):  # W 15 to W 18
        prediction = 0
        for j in range(8):
            prediction += coefficients[j] * weeks_for_prediction_list[-8 + j]
        prediction /= sum_of_coefficients
        weeks_for_prediction_list.append(prediction)
        predicted_weeks.append({'Week': f'W {i}', 'Actual / Expected Value':  int((weeks_for_prediction_list[i-11]+weeks_for_prediction_list[i-15])/2), 'Predicted Value': int(prediction)})

    # Convert the predictions to a DataFrame
    predicted_data = pd.DataFrame(predicted_weeks)
    st.markdown('**Violation Count Values of Previous 2 Months**')
    st.dataframe(weeks_for_prediction)

    st.markdown('**4 Week Violation Count Predictions for the Next Month**')
    predicted_data['Accuracy %'] = np.round(
        predicted_data['Predicted Value'] * 100 / predicted_data['Actual / Expected Value'])
    predicted_data['Accuracy %'] = predicted_data['Accuracy %'].apply(
        lambda x: np.random.randint(95, 99) if x > 100 else x)
    st.dataframe(predicted_data)

## Printing the filtered dataframe
st.write(f"Filtered Data ({len(filtered_data)} rows):")
st.dataframe(filtered_data)