import os

from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_community.vectorstores.chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


def create_rag(knowledge_base_path, vectorstore_path):
    all_document_chunks = list([])
    project_root = os.environ["PROJECT_ROOT"]
    for path, subdirs, files in os.walk("{}/{}".format(project_root, knowledge_base_path)):
        for name in files:
            file_path = os.path.join(path, name)
            if file_path.endswith(".pdf"):
                loader = PyPDFLoader(file_path)
                pages = loader.load()
                text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000,
                                                               chunk_overlap=500)
                t_splits = text_splitter.split_documents(pages)
                all_document_chunks.extend([x for x in t_splits if len(x.page_content.strip()) > 0])
                print("Processed file: {}".format(file_path))
            else:
                print("Skipping file: {}".format(file_path))

    gpt_based_embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

    # TODO: Replace this with some scalable vectorstore, e.g. Elasticsearch
    Chroma.from_documents(all_document_chunks, gpt_based_embeddings,
                          persist_directory=f"{project_root}/{vectorstore_path}",
                          collection_name="embedding_db")


if __name__ == "__main__":
    create_rag("knowledge_base", "vectorstore")
