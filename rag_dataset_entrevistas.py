from langchain_ollama import OllamaEmbeddings

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_chroma import Chroma
import psycopg2, os
from dotenv import load_dotenv

load_dotenv(encoding='utf-8')
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),  
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
}

def get_documents_from_postgres():
    print("=== DB_CONFIG ===")
    for k, v in DB_CONFIG.items():
        print(k, repr(v))

    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute('''SELECT id, titulo, resumen, transcripcion FROM entrevistas ORDER BY id ASC;''') 
    raw_data = cursor.fetchall()
    cursor.close()
    conn.close()
    
    documents = []
    for row in raw_data:
        doc = Document(
            page_content=row[3],  
            metadata={
                "id": row[0],
                "titulo": row[1],
                "resumen": row[2]
            }
        )
        documents.append(doc)
    return documents

model = os.getenv("MODEL")
embeddings = OllamaEmbeddings(model=model)
splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 200)
raw_data = get_documents_from_postgres()
batch_size = 10
vectorstore = Chroma(persist_directory="./chroma.db", embedding_function=embeddings)
splits = splitter.split_documents(raw_data)
for i in range(0, len(splits), batch_size):
    batch = splits[i:i+batch_size]
    vectorstore.add_documents(batch)
