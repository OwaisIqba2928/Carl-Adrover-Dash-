import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np

# Create Dataset
data = {
    "DATE": ["2025-02-22", "2025-02-23"],
    "DAY": ["Saturday", "Sunday"],
    "TOTAL_VISITORS": [8500, 12000],
    "MALE_PERCENTAGE": [18, 22],
    "FEMALE_PERCENTAGE": [82, 78],
    "AVERAGE_AGE": ["10-30", "10-30"]
}

df = pd.DataFrame(data)
df['DATE'] = pd.to_datetime(df['DATE'])

# Generate Random Age Data (Focused on 20-30 Age Range)
np.random.seed(42)  # For reproducibility

# Simulate 1000 visitors on Saturday and 1500 on Sunday
num_saturday = 1000
num_sunday = 1500

# Generate age data with most values in the 20-30 range
age_data = {
    "DAY": ["Saturday"] * num_saturday + ["Sunday"] * num_sunday,
    "AGE": np.concatenate([
        np.random.normal(25, 5, num_saturday).clip(0, 100),  # Saturday: Ages centered around 25
        np.random.normal(27, 5, num_sunday).clip(0, 100)     # Sunday: Ages centered around 27
    ])
}

age_df = pd.DataFrame(age_data)

# Generate 24-Hour Time-Wise Visitor Data (More Realistic)
hours = [f"{hour % 12 or 12} {'AM' if hour < 12 else 'PM'}" for hour in range(24)]  # 12-hour AM/PM format

# Define realistic visitor patterns (peaks in the morning, afternoon, and evening)
def generate_realistic_visitors(day):
    if day == "Saturday":
        # Saturday pattern: Peak in the afternoon and evening
        base_visitors = np.array([50, 30, 20, 10, 10, 20, 50, 100, 200, 300, 400, 500, 
                                  600, 700, 800, 900, 1000, 1200, 1100, 900, 700, 500, 300, 150])
    else:
        # Sunday pattern: Peak in the morning and afternoon
        base_visitors = np.array([100, 150, 200, 300, 400, 600, 800, 1000, 1200, 1100, 
                                  900, 700, 600, 500, 400, 300, 200, 150, 100, 80, 60, 50, 40, 30])
    
    # Add some randomness to make it more realistic
    noise = np.random.normal(0, 50, 24).clip(-100, 100)
    visitors = (base_visitors + noise).clip(0, None)
    return visitors.astype(int)

time_data = {
    "DAY": ["Saturday"] * 24 + ["Sunday"] * 24,
    "TIME": hours * 2,
    "VISITORS": np.concatenate([generate_realistic_visitors("Saturday"), generate_realistic_visitors("Sunday")])
}

time_df = pd.DataFrame(time_data)

# Filter time data to only include 1 PM to 9 PM for Sunday and 4 PM to 8:30 PM for Saturday
time_df_saturday = time_df[(time_df['DAY'] == "Saturday") & (time_df['TIME'].isin(['4 PM', '5 PM', '6 PM', '7 PM', '8 PM']))]
time_df_sunday = time_df[(time_df['DAY'] == "Sunday") & (time_df['TIME'].isin(['1 PM', '2 PM', '3 PM', '4 PM', '5 PM', '6 PM', '7 PM', '8 PM', '9 PM']))]
time_df = pd.concat([time_df_saturday, time_df_sunday])

# Streamlit Page Configuration
st.set_page_config(page_title="📊 Visitor Analytics Dashboard", page_icon="📊", layout="wide")

# Custom CSS for Enhanced Styling and Responsiveness
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
    
    body {
        font-family: 'Poppins', sans-serif;
        background: #ffffff;
        color: #333;
    }

    :root {
        --background-color: #ffffff;
        --text-color: #333;
        --card-background: #ffffff;
        --card-text-color: #333;
        --chart-background: #ffffff;
        --chart-text-color: #333;
    }

    @media (prefers-color-scheme: dark) {
        :root {
            --background-color: #1e1e1e;
            --text-color: #ffffff;
            --card-background: #2d2d2d;
            --card-text-color: #ffffff;
            --chart-background: #2d2d2d;
            --chart-text-color: #ffffff;
        }
    }

    .stApp {
        background: var(--background-color);
        color: var(--text-color);
    }

    .title-bar {
        background: #ADD8E6;  /* Light Blue */
        padding: 20px;
        border-radius: 14px;
        text-align: center;
        color: #00008B;  /* Dark Blue */
        font-size: 28px;
        font-weight: bold;
        box-shadow: 0px 8px 20px rgba(0, 0, 0, 0.2);
        margin-bottom: 20px;
    }

    .kpi-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
        gap: 10px;
        margin: 20px 0;
    }

    .kpi-card {
        flex: 1 1 calc(25% - 20px);
        background: #00008B;  /* Dark Blue */
        padding: 20px;
        border-radius: 14px;
        box-shadow: 0px 6px 14px rgba(0, 0, 0, 0.2);
        text-align: center;
        font-size: 18px;
        font-weight: bold;
        color: white;
        transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
    }

    .kpi-card:hover {
        transform: scale(1.05);
        box-shadow: 0px 10px 20px rgba(0, 0, 0, 0.3);
    }

    .sidebar-box {
        background: #ADD8E6;  /* Light Blue */
        padding: 15px;
        border-radius: 12px;
        color: #00008B;  /* Dark Blue */
        font-weight: bold;
        text-align: center;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
        margin-bottom: 15px;
        transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
    }

    .sidebar-box:hover {
        transform: scale(1.02);
        box-shadow: 0px 6px 15px rgba(0, 0, 0, 0.3);
    }

    .chart-container {
        background: var(--chart-background);
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0px 6px 16px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease-in-out;
        margin-bottom: 20px;
    }

    .chart-container:hover {
        transform: scale(1.02);
    }

    .chart-title {
        font-family: 'Poppins', sans-serif;
        font-size: 24px;
        font-weight: bold;
        text-align: center;
        color: var(--text-color);
        margin-bottom: 10px;
    }

    @media (max-width: 768px) {
        .title-bar {
            font-size: 24px;
            padding: 15px;
        }

        .kpi-card {
            flex: 1 1 calc(50% - 10px);
            font-size: 16px;
            padding: 15px;
        }

        .sidebar-box {
            padding: 10px;
            font-size: 14px;
        }

        .chart-container {
            padding: 10px;
        }
    }

    @media (max-width: 480px) {
        .title-bar {
            font-size: 20px;
            padding: 10px;
        }

        .kpi-card {
            flex: 1 1 100%;
            font-size: 14px;
            padding: 10px;
        }

        .sidebar-box {
            padding: 8px;
            font-size: 12px;
        }

        .chart-container {
            padding: 8px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Dashboard Title
st.markdown("<div class='title-bar'>📊 Visitor Analytics Dashboard</div>", unsafe_allow_html=True)

# Sidebar Filters
with st.sidebar:
    st.markdown("<div class='sidebar-box'>📅 Select Day</div>", unsafe_allow_html=True)
    day_filter = st.selectbox("", options=df['DAY'].unique())

# Filter Data
filtered_data = df[df['DAY'] == day_filter]
filtered_age_data = age_df[age_df['DAY'] == day_filter]
filtered_time_data = time_df[time_df['DAY'] == day_filter]

# KPI Metrics
total_visitors = filtered_data['TOTAL_VISITORS'].values[0]
male_percentage = filtered_data['MALE_PERCENTAGE'].values[0]
female_percentage = filtered_data['FEMALE_PERCENTAGE'].values[0]
average_age = filtered_data['AVERAGE_AGE'].values[0]

# KPI Cards
st.markdown(
    f"""
    <div class="kpi-container">
        <div class="kpi-card"><span>👥 Total Visitors <br> {total_visitors}</span></div>
        <div class="kpi-card"><span>👨 Male Percentage <br> {male_percentage}%</span></div>
        <div class="kpi-card"><span>👩 Female Percentage <br> {female_percentage}%</span></div>
        <div class="kpi-card"><span>📊 Average Age <br> {average_age}</span></div>
    </div>
    """,
    unsafe_allow_html=True
)

# Gender Distribution Pie Chart
gender_data = {
    "Gender": ["Male", "Female"],
    "Count": [male_percentage, female_percentage]
}
gender_df = pd.DataFrame(gender_data)

# Use light blue and dark blue colors for the pie chart
fig_gender_pie = px.pie(
    gender_df, names="Gender", values="Count", 
    color_discrete_sequence=['#ADD8E6', '#00008B'],  # Light Blue and Dark Blue
    hole=0.3  # Sleek modern donut effect
)

fig_gender_pie.update_traces(
    textinfo='label+percent',
    texttemplate="<b>%{label}:</b> %{percent:.0%}",
    marker=dict(line=dict(color='black', width=2)),
    hoverinfo="label+percent+value",
)

fig_gender_pie.update_layout(
    showlegend=True,
    height=420,  
    paper_bgcolor="var(--chart-background)",  
    plot_bgcolor="var(--chart-background)",  
    margin=dict(t=50, b=10, l=10, r=10),
    legend=dict(
        title="🧑‍🤝‍🧑 Gender Distribution",
        font=dict(size=14, color="var(--text-color)"),
        orientation="h",
        yanchor="bottom", y=-0.2,
    )
)

# Updated navigation bar - Clean and Professional
st.markdown("""
    <style>
        .top-nav {
            display: flex;
            justify-content: center;
            align-items: center;
            background: #ADD8E6;  /* Light Blue */
            padding: 14px;
            border-radius: 10px;
            width: 60%;
            margin: auto;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.3);
        }
        .top-nav-title {
            color: #00008B;  /* Dark Blue */
            font-size: 20px;
            font-weight: bold;
            text-align: center;
            text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.2);
            letter-spacing: 0.6px;
        }
    </style>
    <div class="top-nav">
        <span class="top-nav-title">📊 Gender Distribution of Visitors</span>
    </div>
""", unsafe_allow_html=True)  # Removed unnecessary <br>

# Display the pie chart
st.plotly_chart(fig_gender_pie, use_container_width=True)

# Age Distribution Bar Chart
age_bins = [0, 10, 20, 30, 40, 50, 60, 100]
age_labels = ['0-10', '10-20', '20-30', '30-40', '40-50', '50-60', '60+']
filtered_age_data['AGE_GROUP'] = pd.cut(filtered_age_data['AGE'], bins=age_bins, labels=age_labels, right=False)
age_count = filtered_age_data['AGE_GROUP'].value_counts().reindex(age_labels, fill_value=0).reset_index()
age_count.columns = ['Age Group', 'Count']

# Adjusting data for 0-10, 10-20, 40-50, and 50-60 age groups
if day_filter == "Saturday":
    age_count.loc[age_count['Age Group'] == '0-10', 'Count'] = 1200
    age_count.loc[age_count['Age Group'] == '10-20', 'Count'] = 1600
    age_count.loc[age_count['Age Group'] == '20-30', 'Count'] = 2000
    age_count.loc[age_count['Age Group'] == '30-40', 'Count'] = 1500
    age_count.loc[age_count['Age Group'] == '40-50', 'Count'] = 1100
    age_count.loc[age_count['Age Group'] == '50-60', 'Count'] = 700
    age_count.loc[age_count['Age Group'] == '60+', 'Count'] = 300
else:
    age_count.loc[age_count['Age Group'] == '0-10', 'Count'] = 1500
    age_count.loc[age_count['Age Group'] == '10-20', 'Count'] = 2500
    age_count.loc[age_count['Age Group'] == '20-30', 'Count'] = 3000
    age_count.loc[age_count['Age Group'] == '30-40', 'Count'] = 1500
    age_count.loc[age_count['Age Group'] == '40-50', 'Count'] = 1600
    age_count.loc[age_count['Age Group'] == '50-60', 'Count'] = 1000
    age_count.loc[age_count['Age Group'] == '60+', 'Count'] = 600




# Use light blue and dark blue colors for the bar chart
color_palette = ['#ADD8E6', '#00008B', '#ADD8E6', '#00008B', '#ADD8E6', '#00008B', '#ADD8E6']

fig_age_bar = px.bar(
    age_count, x='Age Group', y='Count', text='Count',
    color='Age Group', category_orders={"Age Group": age_labels},
    color_discrete_sequence=color_palette
)

fig_age_bar.update_traces(
    textposition='outside',
    marker=dict(line=dict(color="black", width=1.5)),
    width=0.5  # Make bars closer together for a better look
)

fig_age_bar.update_layout(
    showlegend=False,
    height=400,
    paper_bgcolor="var(--chart-background)",  # Transparent background
    plot_bgcolor="var(--chart-background)",  # Transparent background
    margin=dict(t=50, b=10, l=10, r=10),
    bargap=0.05  # Reduce gap between bars for a better look
)

# Add a professional and centered title bar for the chart
st.markdown("""
    <style>
        .top-nav {
            display: flex;
            justify-content: center;
            align-items: center;
            background: #ADD8E6;  /* Light Blue */
            padding: 10px;
            border-radius: 8px;
            width: 50%;
            margin: auto;
            box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.2);
        }
        .top-nav-title {
            color: #00008B;  /* Dark Blue */
            font-size: 18px;
            font-weight: bold;
            text-align: center;
            letter-spacing: 0.5px;
        }
    </style>
    <div class="top-nav">
        <span class="top-nav-title">📊 Age Distribution of Visitors</span>
    </div>
""", unsafe_allow_html=True)  # Removed unnecessary <br> to fix white space issues

# Display the bar chart without extra space issues
st.plotly_chart(fig_age_bar, use_container_width=True)

# Time-Wise Visitor Distribution Chart (Total Visitors)
# Update the time-wise visitor data based on your instructions
if day_filter == "Saturday":
    filtered_time_data.loc[filtered_time_data['TIME'] == '4 PM', 'VISITORS'] = 1500
    filtered_time_data.loc[filtered_time_data['TIME'] == '5 PM', 'VISITORS'] = 2500
    filtered_time_data.loc[filtered_time_data['TIME'] == '6 PM', 'VISITORS'] = 5000
    filtered_time_data.loc[filtered_time_data['TIME'] == '7 PM', 'VISITORS'] = 6700
    filtered_time_data.loc[filtered_time_data['TIME'] == '8 PM', 'VISITORS'] = 8000

elif day_filter == "Sunday":
    filtered_time_data = filtered_time_data[filtered_time_data['TIME'] != '9 PM']  # Remove 9 PM completely

    filtered_time_data.loc[filtered_time_data['TIME'] == '1 PM', 'VISITORS'] = 1000
    filtered_time_data.loc[filtered_time_data['TIME'] == '2 PM', 'VISITORS'] = 1800
    filtered_time_data.loc[filtered_time_data['TIME'] == '3 PM', 'VISITORS'] = 3000
    filtered_time_data.loc[filtered_time_data['TIME'] == '4 PM', 'VISITORS'] = 5400
    filtered_time_data.loc[filtered_time_data['TIME'] == '5 PM', 'VISITORS'] = 7000
    filtered_time_data.loc[filtered_time_data['TIME'] == '6 PM', 'VISITORS'] = 8700
    filtered_time_data.loc[filtered_time_data['TIME'] == '7 PM', 'VISITORS'] = 10000
    filtered_time_data.loc[filtered_time_data['TIME'] == '8 PM', 'VISITORS'] = 12000



# Use light blue for the line chart
fig_time_line = px.line(
    filtered_time_data, x='TIME', y='VISITORS', 
    markers=True, text='VISITORS',
    color_discrete_sequence=['#ADD8E6']  # Light Blue color for total visitors
)

# Add emojis to the X and Y axes
fig_time_line.update_xaxes(title_text="⏰ Time (12-Hour AM/PM)")
fig_time_line.update_yaxes(title_text="👥 Total Visitors")

# Update layout for better readability
fig_time_line.update_layout(
    showlegend=False,
    height=400,
    paper_bgcolor="var(--chart-background)",  # Transparent background
    plot_bgcolor="var(--chart-background)",  # Transparent background
    margin=dict(t=50, b=10, l=10, r=10)
)

# Add a professional and centered title bar for the chart
st.markdown("""
    <style>
        .top-nav {
            display: flex;
            justify-content: center;
            align-items: center;
            background: #ADD8E6;  /* Light Blue */
            padding: 10px;
            border-radius: 8px;
            width: 50%;
            margin: auto;
            box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.2);
        }
        .top-nav-title {
            color: #00008B;  /* Dark Blue */
            font-size: 18px;
            font-weight: bold;
            text-align: center;
            letter-spacing: 0.5px;
        }
    </style>
    <div class="top-nav">
        <span class="top-nav-title">📊 Time-Wise Visitor Distribution (Total Visitors)</span>
    </div>
""", unsafe_allow_html=True)  # Removed unnecessary <br> to fix white space issues

# Display the time-wise line chart
st.plotly_chart(fig_time_line, use_container_width=True)

# Data Summary Table
st.markdown("<h2 style='text-align: center; color: var(--text-color);'>DATA SUMMARY TABLE</h2>", unsafe_allow_html=True)
st.markdown("<div class='summary-container' style='border: 2px solid #6a11cb; padding: 10px; background-color: var(--chart-background);'>", unsafe_allow_html=True)
st.dataframe(
    filtered_data.assign(
        MALE_PERCENTAGE=filtered_data['MALE_PERCENTAGE'].astype(str) + '%',
        FEMALE_PERCENTAGE=filtered_data['FEMALE_PERCENTAGE'].astype(str) + '%'
    ),
    use_container_width=True
)
st.markdown("</div>", unsafe_allow_html=True)