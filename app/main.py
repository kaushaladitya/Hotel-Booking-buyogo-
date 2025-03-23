import sys
sys.path.append('../')
from fastapi import FastAPI,Depends
from fastapi.responses import JSONResponse,StreamingResponse
from .analytics import *
from .ask import *
from pydantic import BaseModel
from contextlib import asynccontextmanager
import matplotlib.pyplot as plt
from . import models
import asyncpg
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, database, DATABASE_URL, get_db_connection
from app import database

models.Base.metadata.create_all(bind=database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_sql_db():
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        yield conn
    finally:
        await conn.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load and preprocess data on startup."""
    print("Loading and preprocessing data at startup...")
    conn = get_db_connection()
    load_data(conn)
    pre_process_data()
    print("Data loaded successfully.")
    yield  # Keeps the app running


app = FastAPI(lifespan=lifespan)

@app.post("/reset_schema", tags=["Schema"])
async def reset_schema(conn: Session = Depends(get_sql_db)):
    query = """DO $$ DECLARE
                r RECORD;
            BEGIN
                -- Loop through all tables in the current schema
                FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = current_schema()) LOOP
                    EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE';
                END LOOP;
            END $$;"""
    await conn.fetch(query)
    # return True
    models.Base.metadata.create_all(bind=engine)
    return {'message': "Successfully created"}

@app.post("/load_sample_data/",tags=["Schema"])
def load_sample_data(db: Session = Depends(get_db)): 
    df = pd.read_csv("app/hotel_bookings.csv")
    for _, row in df.iterrows():
        hotel_entry = models.HotelManagement(
            id=row.get("id"),
            hotel=row.get("hotel"),
            is_canceled=bool(row.get("is_canceled")),
            lead_time=row.get("lead_time"),
            arrival_date_year=row.get("arrival_date_year"),
            arrival_date_month=row.get("arrival_date_month"),
            arrival_date_week_number=row.get("arrival_date_week_number"),
            arrival_date_day_of_month=row.get("arrival_date_day_of_month"),
            stays_in_weekend_nights=row.get("stays_in_weekend_nights"),
            stays_in_week_nights=row.get("stays_in_week_nights"),
            adults=row.get("adults"),
            children=row.get("children") if not pd.isna(row.get("children")) else None,
            babies=row.get("babies") if not pd.isna(row.get("babies")) else None,
            meal=row.get("meal"),
            country=row.get("country") if not pd.isna(row.get("country")) else None,
            market_segment=row.get("market_segment"),
            distribution_channel=row.get("distribution_channel"),
            is_repeated_guest=bool(row.get("is_repeated_guest")),
            previous_cancellations=row.get("previous_cancellations"),
            previous_bookings_not_canceled=row.get("previous_bookings_not_canceled"),
            reserved_room_type=row.get("reserved_room_type"),
            assigned_room_type=row.get("assigned_room_type"),
            booking_changes=row.get("booking_changes"),
            deposit_type=row.get("deposit_type"),
            agent=row.get("agent") if not pd.isna(row.get("agent")) else None,
            company=row.get("company") if not pd.isna(row.get("company")) else None,
            days_in_waiting_list=row.get("days_in_waiting_list"),
            customer_type=row.get("customer_type"),
            adr=row.get("adr"),
            required_car_parking_spaces=row.get("required_car_parking_spaces"),
            total_of_special_requests=row.get("total_of_special_requests"),
            reservation_status=row.get("reservation_status"),
            reservation_status_date=str(row.get("reservation_status_date")) if not pd.isna(row.get("reservation_status_date")) else None
        )
        db.add(hotel_entry)
    db.commit()

    return {"message": "✅ Data successfully inserted into hotel_management!"}

def generate_plot(plot_function):
    """Helper function to generate a plot and return as an image buffer."""
    fig, ax = plt.subplots(figsize=(8, 6))
    plot_function(ax)
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close(fig)
    return buffer

@app.post("/revenue_trend/")
def revenue_trend1():
    """Returns the revenue trend as an image."""
    buffer = generate_plot(revenue_trend)
    return StreamingResponse(buffer, media_type="image/png")

@app.post("/cancellation_rate/")
def cancellation_rate1():
    """Returns the cancellation rate as an image."""
    buffer = generate_plot(cancellation_rate)
    return StreamingResponse(buffer, media_type="image/png")

@app.post("/booking_lead_time/")
def booking_lead_time1():
    """Returns the booking lead time as an image."""
    buffer = generate_plot(booking_lead_time)
    return StreamingResponse(buffer, media_type="image/png")

@app.post("/geo_map_image/")
def get_geo_map_image1():
    """Returns the geographical distribution map as an image."""
    buffer = geographical_distribution_image()
    return StreamingResponse(buffer, media_type="image/png")

@app.post("/get_all_analytics/")
async def get_saved_analytics1():
    """Return all analytics graphs combined into one image."""
    buffer = get_all_analytics()
    return StreamingResponse(buffer, media_type="image/png")

@app.post("/search_history/")
async def get_search_history():
    conn = get_db_connection()
    data_sql_query = "SELECT * FROM search_history;"
    df = pd.read_sql_query(data_sql_query, conn)
    df.to_csv('app/search_history.csv', index=False)
    return {'message': "Data saved successfully"}

class QueryRequest(BaseModel):
    query: str

@app.post("/ask/")
async def query_llm(request: QueryRequest):
    """Fetch the most relevant answer from FAISS search."""
    conn=get_db_connection()
    response = search_query(conn,request.query)
    return {"response": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)
