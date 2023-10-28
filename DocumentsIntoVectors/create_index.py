# https://www.youtube.com/watch?v=N7TQgp18kA4
# https://github.com/Leon-Sander/langchain_faiss_vectorindex



# Massive Text Embedding Benchmark (MTEB) Leaderboard
# https://huggingface.co/spaces/mteb/leaderboard

# VECTOR INDEXES:
# Elasticsearch, FAISS, Annoy
# in this example => use of FAISS
# https://faiss.ai/index.html
# it is really fast (10x) but loses precision compared to other methods (10% incorrect answers)

# VECTOR DATABASES:
# Pinecone, Weaviate, Milvus


from langchain.embeddings.huggingface import HuggingFaceBgeEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import faiss
from langchain.document_loaders import PyPDFLoader
from glob import glob
from tqdm import tqdm
from utils import load_documents


# https://python.langchain.com/docs/modules/data_connection/document_loaders/
# WHILE IN THE VIDEO:
# https://api.python.langchain.com/en/latest/document_loaders/langchain.document_loaders.pdf.PyPDFLoader.html

# https://api.python.langchain.com/en/latest/text_splitter/langchain.text_splitter.RecursiveCharacterTextSplitter.html

# https://api.python.langchain.com/en/latest/text_splitter/langchain.text_splitter.TextSplitter.html



documents = load_documents("data/")

# https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2
embedding_function = HuggingFaceBgeEmbeddings(model_name="all-MiniLM-L6-v2", model_kwargs = {'device': 'cuda'})



# creating vector database
db = faiss.from_documents(documents, embedding_function)
db.save_local("faiss_db/", "books")

print(db.similarity_search("Hermetic principle"))