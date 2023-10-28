# https://www.youtube.com/watch?v=N7TQgp18kA4
# https://github.com/Leon-Sander/langchain_faiss_vectorindex

from langchain.embeddings.huggingface import HuggingFaceBgeEmbeddings
from langchain.vectorstores import faiss
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI

load_dotenv()

embedding_function = HuggingFaceBgeEmbeddings(model_name="all-MiniLM-L6-v2", model_kwargs = {'device': 'cuda'})

db = faiss.load_local(folder_path="faiss_db/", index_name="books", embeddings=embedding_function)

qa = RetrievalQA.from_llm(llm=ChatOpenAI(temperature=0.1), retriever=db.as_retriever())

while True:
    print("What's Your Question: ")
    query = input()
    if query == "exit":
        break
    print(qa.run(query))