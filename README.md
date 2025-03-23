# LLM-Powered Hotel Booking Analytics & QA System

## 📌 Objective
This project processes hotel booking data, extracts insights, and enables retrieval-augmented question answering (RAG) using an LLM. It provides analytics and allows users to query booking-related information.

---

## ✨ Features


### 🔹 Analytics & Reporting
- 📊 Revenue trends over time
- 📉 Cancellation rate percentage
- 🌍 Geographical distribution of bookings
- ⏳ Booking lead time distribution
- 📌 Additional insights

### 🔹 Retrieval-Augmented Question Answering (RAG)
- Uses **FAISS, ChromaDB, or Weaviate** for vector storage
- Implements **natural language Q&A** with an open-source LLM using mistral model(light weight).

-------


### 🔹 API Development(main.py)

- `POST /analytics` → Returns analytics reports
- `POST /ask` → Answers booking-related questions 
- `POST /reset_schema` → reset schema of the database table
- `POST /revenue_trend` → create the revenue graphs
- `POST /cancellation_rate` → create the cancellation rate pie chart
- `POST /booking_lead_time` → Booking lead time stats.
- `POST /geo_map_image` → Geographical representation of the country booking stats.
- `POST /get_all_analytics` → Get the combined graphs for all analytics
- `POST /search_history` → To track the history of the query given to the LLM.
- `POST /load_sample_data` → load the file data in the database

---
# START -> END:

1. Create a database.
2. Load the data set to the database.
3. Run the Uvicorn:-   unicorn app.main:app --host 127.0.0.1 --port 8080 --reload.
4. Run the streamlet Enjoy! the seamless interface and get the analytics by running :- streamlet run dashboard/Home.py.

--------
# Files 
- main.py:- Contains all the API and the database integration.
- analytics.py:- Contains the analysis and the analysis of the different columns in the data.
- embedding.py:- Code for the word embedding.
- ask.py:- Contain the setup of the model and the code for the user query containing the file of pre-embedded (hotel_index. faiss). And contain the prompt based on which our model going to answer.
- databas.py:- Contains the code for the Postgres setup.
- models.py:- Contain the Schema of the data.

----------
# **Important**:
- Refer to file .env containing the host,ip, and password.
- Inside app folder there is vector embedding folder provided with the drive link download the file from there before running the program
-------
# Referance photo:
- refer to the photo of streamlit dashboard and swager api.

## 👨‍💻 Contributors
- **Aditya Kaushal**

