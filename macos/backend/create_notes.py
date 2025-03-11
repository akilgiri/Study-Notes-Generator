from qdrant_client import QdrantClient
from mlx_lm import load, generate
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_qdrant import QdrantVectorStore
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_openai import OpenAI, ChatOpenAI
import os

def create_notes():
    # Check for environment variables
    if os.getenv("QDRANT_URL") is None:
        raise ValueError("QDRANT_URL environment variable not set.")
    else:
        qdrant_url = os.getenv("QDRANT_URL")

    if os.getenv("QDRANT_API_KEY") is None:
        raise ValueError("QDRANT_API_KEY environment variable not set.")
    else:
        qdrant_api_key = os.getenv("QDRANT_API_KEY")

    if os.getenv("OPENAI_API_KEY") is None:
        raise ValueError("OPENAI_API_KEY environment variable not set.")
    else:
        openai_api_key = os.getenv("OPENAI_API_KEY")

    # Initialize Qdrant Vector Store, Embedding Model and Chat Model
    client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large", api_key=openai_api_key)

    vector_store = QdrantVectorStore(
        client=client,
        collection_name="knowledge-base",
        embedding=embeddings,
    )
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 20})
    llm = ChatOpenAI(model="o3-mini-2025-01-31",api_key=openai_api_key)

    prompt_template = """
    You are an intelligent assistant tasked with creating study notes. 
    Use the provided topic details and context to create comprehensive study notes for students.

    Context:
    {context}

    Topic Details:
    {query}

    Answer:
    """
    prompt = ChatPromptTemplate.from_template(prompt_template)

    # Configure the LLM chain
    chain = (
        {"context": retriever, "query": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain

# result = chain.invoke("Course: Compilers, Topic: regex to DFA")
# print(result)