from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

CHROMA_PATH = "chroma_db"


def get_retriever():

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectordb = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embeddings
    )

    return vectordb.as_retriever(search_kwargs={"k": 4})


if __name__ == "__main__":

    retriever = get_retriever()

    query = "What is CET1 capital?"

    docs = retriever.invoke(query)

    for i, doc in enumerate(docs):
        print(f"\n--- Document {i+1} ---\n")
        print(doc.page_content)
