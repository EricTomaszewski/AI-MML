# https://www.youtube.com/watch?v=N7TQgp18kA4
# https://github.com/Leon-Sander/langchain_faiss_vectorindex

from langchain.embeddings.huggingface import HuggingFaceBgeEmbeddings
from langchain.vectorstores import faiss
from utils import load_documents


db = faiss.load_local(folder_path="faiss_db/", index_name="books", embeddings=embeddings)
db.add_documents(load_documents("new_document/"))

db.save_local("faiss_db/", "books")





from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from utils import load_documents, load_db, save_db, load_embeddings

db = load_db(embedding_function=load_embeddings())
db.add_documents(load_documents("new_document/"))
save_db(db)