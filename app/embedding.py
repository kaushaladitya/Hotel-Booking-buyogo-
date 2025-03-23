import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

df=pd.read_csv('text_data.csv')
model = SentenceTransformer('all-MiniLM-L6-v2')
df["embedding"] = df['combined_text'].apply(lambda x: model.encode(x))
d = len(df["embedding"][0])  
index = faiss.IndexFlatL2(d)
embeddings = np.vstack(df["embedding"].values)
index.add(embeddings)
faiss.write_index(index, "hotel_index.faiss")
print("Hotel booking data and FAISS index created successfully!")


