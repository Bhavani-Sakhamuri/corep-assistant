import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
#from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
#from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings


DATA_PATH = "data"
CHROMA_PATH = "chroma_db"


def load_documents():
    docs = []

    for folder in ["pra", "corep"]:
        folder_path = os.path.join(DATA_PATH, folder)

        for file in os.listdir(folder_path):
            if file.endswith(".pdf"):
                loader = PyPDFLoader(os.path.join(folder_path, file))
                docs.extend(loader.load())

    return docs


def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )

    return splitter.split_documents(documents)


def create_vector_store(chunks):

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectordb = Chroma.from_documents(
        chunks,
        embeddings,
        persist_directory=CHROMA_PATH
    )

    vectordb.persist()
    print("Vector DB created successfully!")


if __name__ == "__main__":
    documents = load_documents()
    chunks = split_documents(documents)
    create_vector_store(chunks)
