from dotenv import load_dotenv
import os
import sys
sys.path.insert(0, '/home/mubarek/all_about_programing/10x_projects/Enterprise-Level-Automated-Prompt-Engineering/backend')
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
import weaviate
from langchain.vectorstores import Weaviate
from utility.env_manager import get_env_manager

load_dotenv()

env_manager = get_env_manager()
OPENAI_KEY = env_manager['openai_keys']['OPENAI_API_KEY']


def load_data():
    script_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    pdfs_dir = os.path.join(script_dir, 'pdfs')
    loader = DirectoryLoader(pdfs_dir, glob="**/*.pdf")
    data = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
    docs = text_splitter.split_documents(data)

    text_meta_pair = [(doc.page_content, doc.metadata) for doc in docs]
    texts, meta = list(zip(*text_meta_pair))

    return texts, meta


def vectorize_data(texts, meta):
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_KEY)

    client = weaviate.Client(
        url="http://localhost:8080",
        additional_headers={"X-OpenAI-Api-Key": OPENAI_KEY},
        startup_period=10
    )

    client.schema.delete_all()
    client.schema.get()
    schema = {
        "classes": [
            {
                "class": "Chatbot",
                "description": "Documents for chatbot",
                "vectorizer": "text2vec-openai",
                "moduleConfig": {"text2vec-openai": {"model": "ada", "type": "text"}},
                "properties": [
                    {
                        "dataType": ["text"],
                        "description": "The content of the paragraph",
                        "moduleConfig": {
                            "text2vec-openai": {
                                "skip": False,
                                "vectorizePropertyName": False,
                            }
                        },
                        "name": "content",
                    },
                ],
            },
        ]
    }

    client.schema.create(schema)

    vectorstore = Weaviate(client, "Chatbot", "content", attributes=["source"])
    vectorstore.add_texts(texts, meta)

    return vectorstore


def get_context_from_rag(user_objective):
    texts, meta = load_data()
    vectorstore = vectorize_data(texts, meta)

    query = user_objective
    docs = vectorstore.similarity_search(query, k=5)

    context = " ".join(doc.page_content for doc in docs)

    return context


if __name__ == "__main__":
    user_objective = str(input("objective: "))
    print(get_context_from_rag(user_objective))