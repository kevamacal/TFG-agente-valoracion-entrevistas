import os
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from dotenv import load_dotenv

load_dotenv()

loader = TextLoader("./Documentos/Dataset_buenas_practicas/guia_buenas_practicas.txt", encoding="utf-8")
documents = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
splits = splitter.split_documents(documents)

model_name = os.getenv("MODEL")
embeddings = OllamaEmbeddings(model=model_name)

print("⏳ Creando base de datos de reglas...")
vectorstore = Chroma(
    persist_directory="./chroma_rules_db", 
    embedding_function=embeddings
)
vectorstore.add_documents(splits)

print("✅ ¡Listo! Reglas guardadas en './chroma_rules_db'.")