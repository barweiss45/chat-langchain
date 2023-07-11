"""Load html from files, clean up, split, ingest into Weaviate."""
import os
from dotenv import load_dotenv

from langchain.document_loaders import ReadTheDocsLoader, UnstructuredMarkdownLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.chroma import Chroma
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings

# Load .env
load_dotenv()

# OpenAI Key for OpenAI API
openai_api_key = os.environ['OPENAI_API_KEY']

def ingest_docs():
    """Get documents from web pages."""
    #loader = ReadTheDocsLoader("api.python.langchain.com/en/latest/modules", features="html.parser")
    markdown_path = "/Users/barweiss/Library/CloudStorage/OneDrive-Cisco/Markdowns/XPATH_Quick_Notes.md"
    loader = UnstructuredMarkdownLoader(markdown_path)
    raw_documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    documents = text_splitter.split_documents(raw_documents)
    embedding_function = OpenAIEmbeddings()
    # create the open-source embedding function
    #embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = Chroma.from_documents(documents, 
                                        embedding_function,
                                        persist_directory="./chroma_db")
    vectorstore.persist()



if __name__ == "__main__":
    ingest_docs()
