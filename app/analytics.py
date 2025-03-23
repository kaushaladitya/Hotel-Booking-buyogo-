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
