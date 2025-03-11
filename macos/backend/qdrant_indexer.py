from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
import os

def index2qdrant(output_folder, video_path, notes_path):
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


    # Initialize Qdrant and Embedding model
    client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
    # client.set_model("intfloat/multilingual-e5-large")
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large", api_key=openai_api_key)


    # Intialize langchain text splitter
    text_splitter = SemanticChunker(OpenAIEmbeddings(model="text-embedding-3-large", api_key=openai_api_key))

    # Read the video transcript and notes
    # with open("../videos/uw_ece351_regex2dfa.txt", "r") as f:
    if video_path != "":
        text_file_name = os.path.split(video_path)[-1].replace(".mp4", ".txt")
        text_file = os.path.join(output_folder, text_file_name)
        with open(text_file, "r") as f:
            vid_transcript = f.read()
            # print(vid_transcript)
            split_vid_transcript = text_splitter.create_documents([vid_transcript])
    else:
        split_vid_transcript = []


    # with open("../study_data/ece351/04a-regex2dfa/04a-regex2dfa.md", "r") as f:

    if notes_path != "":
        pdf_name = os.path.split(notes_path)[-1].replace(".pdf", "")
        pdf_path = os.path.join(output_folder, f"{pdf_name}.md")
        with open(pdf_path, "r") as f:
            notes = f.read()
            # print(notes)

        split_notes = text_splitter.create_documents([notes])
    else:
        split_notes = []

    # Concatenate the video transcript and notes to be indexed
    embedding_docs = split_notes + split_vid_transcript

    # Create Qdrant collection if it doesn't exist already
    if not client.collection_exists(collection_name="knowledge-base"):
        client.create_collection(
            collection_name="{collection_name}",
            vectors_config=VectorParams(size=3072, distance=Distance.COSINE),
        )

    # Index the documents to Qdrant
    qdrant = QdrantVectorStore.from_documents(
        embedding_docs,
        embeddings,
        url=qdrant_url,
        prefer_grpc=True,
        api_key=qdrant_api_key,
        collection_name="knowledge-base",
    )

    # print(split_vid_transcript[0].page_content)
    # print(split_notes[0].page_content)

    # print(type(split_vid_transcript), type(split_vid_transcript[0]))
    # print(type(split_notes))



