import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')
import seaborn as sns
import pandas as pd
import pycountry
import plotly.express as px
import io

df=None
def load_data(conn):
    global df
    try:
        data_sql_query = "SELECT * FROM hotel_management;"
        df = pd.read_sql_query(data_sql_query, conn)
        # df = pd.read_csv("hotel_bookings.csv")  # Load once
        print(df.head())
        print("Data loaded successfully!")

    except Exception as e:
        print(f"Error loading data: {e}")

def pre_process_data():
    global df
    if df is None:
        return {"error": "Data not loaded"}
    for col in df.columns:
        df[col].fillna('Unknown', inplace=True)
    df = df.drop_duplicates()
    df.to_csv("app/hotel_bookings_cleaned.csv", index=False)

def revenue_trend(ax):
    global df
    if df is None:
        return
    df["total_revenue"] = df["adr"] * (df["stays_in_weekend_nights"] + df["stays_in_week_nights"])
    revenue_trend = df.groupby(["arrival_date_year", "arrival_date_month"])["total_revenue"].sum().reset_index()
    
    month_order = ["January", "February", "March", "April", "May", "June", 
                   "July", "August", "September", "October", "November", "December"]
    
    revenue_trend["arrival_date_month"] = pd.Categorical(
        revenue_trend["arrival_date_month"], categories=month_order, ordered=True
    )
    revenue_trend = revenue_trend.sort_values(["arrival_date_year", "arrival_date_month"])
    
    sns.lineplot(data=revenue_trend, x="arrival_date_month", y="total_revenue", hue="arrival_date_year", marker="o", ax=ax)
    ax.set_xlabel("Time (Month)")
    ax.set_ylabel("Total Revenue")
    ax.set_title("Revenue Trend Over Time (by Year)")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    ax.legend(title="Year")
    ax.grid(True)

def cancellation_rate(ax):
    global df
    if df is None:
        return
    yearly_cancellations = df.groupby("arrival_date_year")["is_canceled"].sum().reset_index()
    labels = yearly_cancellations["arrival_date_year"].astype(str)
    sizes = yearly_cancellations["is_canceled"]
    colors = ["#1f77b4", "#ff7f0e", "#2ca02c"]
    
    ax.pie(sizes, labels=labels, autopct="%1.1f%%", colors=colors, startangle=140, explode=[0.05] * len(labels))
    ax.set_title("Year-wise Total Cancellations")

def booking_lead_time(ax):
    print("chanman pappu")
    global df
    if df is None:
        return
    df["lead_time"] = pd.to_numeric(df["lead_time"], errors="coerce")
    sns.histplot(df["lead_time"], bins=20, kde=True, color="blue", ax=ax)
    ax.set_xlabel("Lead Time")
    ax.set_ylabel("Frequency")
    ax.set_title("Histogram of Lead Time")

def geographical_distribution_image():
    global df
    if df is None:
        return None
    geo_bookings = df.groupby("country")["hotel"].count().reset_index()
    geo_bookings.columns = ["Country", "Total_Bookings"]
    
    def get_country_code(country_name):
        try:
            return pycountry.countries.lookup(country_name).alpha_3
        except LookupError:
            return None
    
    geo_bookings["Country_Code"] = geo_bookings["Country"].apply(get_country_code)
    geo_bookings = geo_bookings.dropna(subset=["Country_Code"])
    
    fig = px.choropleth(
        geo_bookings,
        locations="Country_Code",
        locationmode="ISO-3",
        color="Total_Bookings",
        hover_name="Country",
        hover_data={"Total_Bookings": True},
        title="Global Hotel Bookings",
        color_continuous_scale="Magma"
    )
    img_buffer = io.BytesIO()
    fig.write_image(img_buffer, format="png")
    img_buffer.seek(0)
    return img_buffer

def get_all_analytics():
    global df
    if df is None:
        return {"error": "Data not loaded"}
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    revenue_trend(ax=axes[0, 0])
    cancellation_rate(ax=axes[0, 1])
    booking_lead_time(ax=axes[1, 0])
    geo_bookings = df.groupby("country")["hotel"].count().reset_index().sort_values(by="hotel", ascending=False).head(10)
    sns.barplot(ax=axes[1, 1], data=geo_bookings, x="hotel", y="country", palette="viridis")
    axes[1, 1].set_title("Top 10 Countries by Bookings")
    axes[1, 1].set_xlabel("Total Bookings")
    axes[1, 1].set_ylabel("Country")
    
    plt.tight_layout()
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close(fig)
    
    return buffer

# def get_analytics():
#     #load the data
#     # df = pd.read_csv('hotel_bookings.csv')
#     # global df
#     # if df is None:
#     #     return {"error": "Data not loaded"}
#     # for col in df.columns:
#     #     df[col].fillna('Unknown', inplace=True)

#     # # Remove duplicates
#     # df = df.drop_duplicates()

#     # df=pre_process_data()
#     global df
#     if df is None:
#         return {"error": "Data not loaded"} 
#     # revenue trend over the time visulization
#     df["total_revenue"] = df["adr"] * (df["stays_in_weekend_nights"] + df["stays_in_week_nights"])
#     revenue_trend = df.groupby(["arrival_date_year", "arrival_date_month"])["total_revenue"].sum().reset_index()

#     # Ensure "static/graphs" directory exists
#     # if not os.path.exists("static/graphs"):
#     #     os.makedirs("static/graphs")

#     # Define the correct month order
#     month_order = ["January", "February", "March", "April", "May", "June", 
#                 "July", "August", "September", "October", "November", "December"]

#     # Convert `arrival_date_month` to categorical type with the correct order
#     revenue_trend["arrival_date_month"] = pd.Categorical(
#         revenue_trend["arrival_date_month"], categories=month_order, ordered=True
#     )

#     # Sort data to ensure correct ordering
#     revenue_trend = revenue_trend.sort_values(["arrival_date_year", "arrival_date_month"])
#     # print(revenue_trend)
#     # Create the plot

#     fig, axes = plt.subplots(2, 2, figsize=(12, 10))

#     sns.lineplot(ax=axes[0, 0], data=revenue_trend, x="arrival_date_month", y="total_revenue", hue="arrival_date_year", marker="o")
#     axes[0, 0].set_title("Revenue Trend Over Time")
#     axes[0, 0].set_xlabel("Month")
#     axes[0, 0].set_ylabel("Total Revenue")
#     axes[0, 0].tick_params(axis='x', rotation=45)
#     axes[0, 0].legend(title="Year")


#     # plt.figure(figsize=(12, 6))
#     # sns.lineplot(
#     #     data=revenue_trend, 
#     #     x="arrival_date_month", 
#     #     y="total_revenue", 
#     #     hue="arrival_date_year", 
#     #     marker="o"
#     # )

#     # plt.xlabel("Time (Month)")
#     # plt.ylabel("Total Revenue")
#     # plt.title("Revenue Trend Over Time (by Year)")
#     # plt.xticks(rotation=45)  # Rotate for better readability
#     # plt.legend(title="Year")
#     # plt.grid(True)
#     # plt.show()
#     # Save the graph
#     # graph_path = "static/graphs/revenue_trend.png"
#     # plt.savefig(graph_path)
#     # plt.close()
# ######################################################################################
#   # Revenue trend table over the year summary
#     # Convert revenue_data to a DataFrame if it's a list
#     # if isinstance(revenue_trend, list):
#     #     revenue_data = pd.DataFrame(revenue_trend)
#     # revenue_data=revenue_trend

#     # Ensure column names are correct
#     # if "arrival_date_year" not in revenue_data.columns or "total_revenue" not in revenue_data.columns:
#     #     raise ValueError("Check if revenue_data has correct column names: 'arrival_date_year' and 'total_revenue'.")
#     if "arrival_date_year" not in revenue_trend.columns or "total_revenue" not in revenue_trend.columns:
#         raise ValueError("Check if revenue_data has correct column names: 'arrival_date_year' and 'total_revenue'.")

#     yearly_summary = revenue_trend.groupby("arrival_date_year")["total_revenue"].agg(
#         total_revenue="sum",
#         average_revenue="mean"
#     ).reset_index()

#     # Save to CSV
#     # csv_path = "static/tables/yearly_revenue_summary.csv"
#     # yearly_summary.to_csv(csv_path, index=False)


#     ############`Cancellation Rate`####################
#     # Calculate the cancellation rate
#     total_bookings = len(df)
#     total_cancellations = df["is_canceled"].sum()
#     cancellation_rate = (total_cancellations / total_bookings) * 100


#     yearly_cancellation_rate = df.groupby("arrival_date_year")["is_canceled"].mean() * 100
#     yearly_cancellation_rate = yearly_cancellation_rate.round(2)
#     # Convert to DataFrame
#     yearly_cancellation_rate = yearly_cancellation_rate.reset_index()
#     yearly_cancellation_rate.rename(columns={"is_canceled": "cancellation_rate"}, inplace=True)

#     # Save to CSV
#     # csv_path = "static/tables/yearly_cancellation_rate.csv"
#     # yearly_cancellation_rate.to_csv(csv_path, index=False)

#     # Group by year and count total cancellations
#     yearly_cancellations = df.groupby("arrival_date_year")["is_canceled"].sum()

#     # Convert to DataFrame
#     yearly_cancellations = yearly_cancellations.reset_index()
#     yearly_cancellations.rename(columns={"is_canceled": "total_cancellations"}, inplace=True)

#     # Define data for pie chart
#     labels = yearly_cancellations["arrival_date_year"].astype(str)  # Convert years to string
#     sizes = yearly_cancellations["total_cancellations"]  # Total cancellations per year
#     colors = ["#1f77b4", "#ff7f0e", "#2ca02c"]  # Different colors for each year

#     # Create pie chart

#     axes[0, 1].pie(yearly_cancellations["total_cancellations"], labels=yearly_cancellations["arrival_date_year"].astype(str), autopct="%1.1f%%", startangle=140, colors=["#1f77b4", "#ff7f0e", "#2ca02c"])
#     axes[0, 1].set_title("Yearly Cancellations")


#     # plt.figure(figsize=(8, 6))
#     # plt.pie(sizes, labels=labels, autopct="%1.1f%%", colors=colors, startangle=140, explode=[0.05] * len(labels))
#     # plt.title("Year-wise Total Cancellations")
#     # plt.show()
#     # Save Pie Chart
#     # plt.savefig("static/graphs/yearly_cancellation_pie.png")
#     # plt.close()
#     ################################################################################################
#     # Geographical distribution of bookings
#     # if not os.path.exists("static/tables"):
#     #     os.makedirs("static/tables")

#     # Group by country and count bookings
#     geo_bookings = df.groupby("country")["hotel"].count().reset_index()
#     geo_bookings.columns = ["Country", "Total_Bookings"]

#     # Sort by highest bookings
#     geo_bookings = geo_bookings.sort_values(by="Total_Bookings", ascending=False)

#     # Save as CSV
#     # csv_path = "static/tables/geographical_bookings.csv"
#     # geo_bookings.to_csv(csv_path, index=False)



#     # Sample Data: Group bookings by country
#     # geo_bookings = df.groupby("country")["hotel"].count().reset_index()
#     # geo_bookings.columns = ["Country", "Total_Bookings"]

#     # # Function to convert country names to ISO-3 codes
#     # def get_country_code(country_name):
#     #     try:
#     #         return pycountry.countries.lookup(country_name).alpha_3  # Convert to 3-letter code
#     #     except LookupError:
#     #         return None  # Return None if not found

#     # # Apply conversion
#     # geo_bookings["Country_Code"] = geo_bookings["Country"].apply(get_country_code)

#     # # Drop missing values (if any countries couldn't be mapped)
#     # geo_bookings = geo_bookings.dropna(subset=["Country_Code"])

#     # Create an interactive choropleth map with dark contrast colors

  
#     geo_bookings = df.groupby("country")["hotel"].count().reset_index().sort_values(by="hotel", ascending=False).head(10)
#     sns.barplot(ax=axes[1, 1], data=geo_bookings, x="hotel", y="country", palette="viridis")
#     axes[1, 1].set_title("Top 10 Countries by Bookings")
#     axes[1, 1].set_xlabel("Total Bookings")
#     axes[1, 1].set_ylabel("Country")


#     # fig = px.choropleth(
#     #     geo_bookings,
#     #     locations="Country_Code",  # Use 3-letter country codes
#     #     locationmode="ISO-3",
#     #     color="Total_Bookings",
#     #     hover_name="Country",  
#     #     hover_data={"Total_Bookings": True},
#     #     title="Global Hotel Bookings",
#     #     color_continuous_scale="Magma"  # Dark contrast color scheme
#     # )

#     # Save as an interactive HTML file
#     # graph_path = "static/graphs/geographical_bookings.html"
#     # fig.write_html(graph_path)


#     ########################################################################################
#     # Booking lead time distribution
#     # Load your DataFrame (Replace this with actual data loading)
#     # df = pd.read_csv("your_data.csv")  # Uncomment if loading from a file

#     # Ensure 'lead_time' column exists and is numeric
#     df["lead_time"] = pd.to_numeric(df["lead_time"], errors="coerce")

#     # ✅ Ensure directories exist
#     # os.makedirs("static/tables", exist_ok=True)
#     # os.makedirs("static/graphs", exist_ok=True)

#     # ✅ Save Top 5 Days to CSV
#     # top_5_days = df.nlargest(5, "lead_time")
#     # top_5_days.to_csv("static/tables/top_5_days.csv", index=False)
#     # print("✅ Top 5 days saved as 'static/tables/top_5_days.csv'")

#     # ✅ Create and Save Histogram
#     sns.histplot(ax=axes[1, 0], data=df, x="lead_time", bins=20, kde=True, color="blue")
#     axes[1, 0].set_title("Lead Time Distribution")
#     axes[1, 0].set_xlabel("Lead Time")
#     axes[1, 0].set_ylabel("Frequency")




#     # plt.figure(figsize=(8, 5))
#     # sns.histplot(df["lead_time"], bins=5, kde=True, color="blue")
#     # plt.xlabel("Lead Time")
#     # plt.ylabel("Frequency")
#     # plt.title("Histogram of Lead Time")

#     # # Show the plot before saving
#     # plt.show()

#     # Save the figure
#     # histogram_path = "static/graphs/lead_time_histogram.png"
#     # plt.savefig(histogram_path, dpi=300)
#     # print(f"✅ Histogram saved as '{histogram_path}'")

#     # Close the figure
#     # plt.close()

#     plt.tight_layout()
#     buffer = io.BytesIO()
#     plt.savefig(buffer, format="png")
#     plt.close(fig)
#     buffer.seek(0)



#     ########################################################################################

#     # dividing data to catagorical columns and numerical columns for word embedding
#     text_columns = ['hotel', 'arrival_date_month','meal','country','reserved_room_type','assigned_room_type','deposit_type','market_segment', 'distribution_channel', 'customer_type', 'reservation_status']
#     df['combined_text'] = df[text_columns].astype(str).agg(' '.join, axis=1)  # Combine text fields

#     # Select numerical columns for separate storage
#     numerical_columns = ['adr', 'lead_time', 'stays_in_weekend_nights', 'stays_in_week_nights', 'adults', 'children', 'babies','booking_changes','required_car_parking_spaces']
#     df_numerical = df[numerical_columns]  # Store separately

#     # Convert NaNs in text data (if any) to empty strings
#     df['combined_text'] = df['combined_text'].fillna('')

#     return buffer


