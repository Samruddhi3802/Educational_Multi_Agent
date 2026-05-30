from sentence_transformers import SentenceTransformer
import chromadb

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.Client()
collection = client.get_or_create_collection(name="study-material")

def load_data():
    with open("data/notes.txt", "r") as f:
        data = f.readlines()

    for i, line in enumerate(data):
        embedding=model.encode(line).tolist()
        collection.add(
            documents=[line],
            embeddings=[embedding],
            ids=[str(i)]
        )

def get_context(query):
    query_embedding=model.encode(query).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=2
    )
    return " ".join(results['documents'][0])