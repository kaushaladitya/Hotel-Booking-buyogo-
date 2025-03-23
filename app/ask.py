import sys
sys.path.append('../')
import faiss
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from transformers import pipeline
import ollama
from sqlalchemy.orm import Session
import asyncpg


model = SentenceTransformer('all-MiniLM-L6-v2')
df = pd.read_csv('app/hotel_bookings_cleaned.csv')
index = faiss.read_index("app/hotel_index.faiss")

numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()

stat_operations = {
    "average": "mean",
    "mean": "mean",
    "median": "median",
    "total": "sum",
    "sum": "sum",
    "maximum": "max",
    "max": "max",
    "minimum": "min",
    "min": "min",
    "count": "count",
}

def extract_stat_query(user_query: str):
    """Extract column name and statistical operation from user query."""
    user_query_lower = user_query.lower()
    operation = None
    for keyword, method in stat_operations.items():
        if keyword in user_query_lower:
            operation = method
            break
    found_column = None
    for col in numeric_columns:
        col_lower = col.replace("_", " ").lower()  
        if col_lower in user_query_lower:
            found_column = col
            break

    return operation, found_column

def search_query(conn, user_query: str):
    curr=conn.cursor()
    curr.execute("""
        INSERT INTO search_history (
            query,time
        )
        VALUES (%s, CURRENT_TIMESTAMP AT TIME ZONE 'UTC');
    """, 
        (user_query,)
        )
    conn.commit()
    """Process user query dynamically: either compute stats or use FAISS for retrieval."""
    operation, column = extract_stat_query(user_query)
    if operation and column:
        result = getattr(df[column], operation)()
        return f"The {operation} of {column.replace('_', ' ')} is {result:.2f}."
    query_embedding = model.encode(user_query).reshape(1, -1)
    k = 5  
    distances, indices = index.search(query_embedding, k)

    retrieved_data = df.iloc[indices[0]]
    relevant_data = retrieved_data.to_string(index=False)
    summary_table = df.describe().to_string()
    prompt = f"""
    You are an AI expert in hotel booking analysis. Your role is to analyze the hotel booking dataset and provide insights.

    ### User Query:
    {user_query}

    ### Data Sample:
    ```
    {relevant_data}
    ```

    ### Statistical Summary:
    ```
    {summary_table}
    ```
    **Guidelines for your response:**
    - Keep it short (1-3 sentences).
    - If data is missing, say "Data not available for this query."
    - If a calculation is possible, provide the direct result.
    
    Answer the query using the data provided, applying calculations where needed.
    """

    response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])

    return response['message']['content']
