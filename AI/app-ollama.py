import json
import chromadb
import ollama
from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document

# Load issues from JSON
def load_issues(json_file="issues.json"):
    with open(json_file, "r", encoding="utf-8") as file:
        issues_data = json.load(file).get("issues", [])
    
    documents = [
        Document(
            page_content=issue["problem"] + " - " + " ".join(issue["steps"]),
            metadata={"category": issue["category"]}
        )
        for issue in issues_data
    ]
    return documents

# Initialize ChromaDB
def initialize_vectorstore(documents, db_path="./chroma_db"):
    chroma_client = chromadb.PersistentClient(path=db_path)
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=OllamaEmbeddings(model="gemma:2b"),
        persist_directory=db_path
    )
    return vectorstore

# Retrieve relevant issues
def retrieve_issues(query, vectorstore, top_k=3):
    results = vectorstore.similarity_search(query, k=top_k)
    return results

# Generate AI response
def generate_response(user_query, vectorstore):
    relevant_issues = retrieve_issues(user_query, vectorstore)
    context = "\n\n".join([doc.page_content for doc in relevant_issues])
    
    prompt = f"""
    You are an advanced AI support assistant for the Breath of the Wild Multiplayer Mod. Your goal is to help users with troubleshooting their issues related to the mod, providing clear, concise, and actionable guidance. You are knowledgeable about known bugs, workarounds, and fixes for common problems that may occur when using the mod.

When a user reports an issue, you will follow this approach:

    Acknowledge the problem and reassure the user that you can help.
    Analyze the user’s query and compare it with the known issues and solutions.
    Offer a step-by-step troubleshooting guide based on the problem, ensuring clarity and ease of following.
    If no direct solution is found, guide the user to provide more information or suggest potential temporary workarounds, and let them know about future fixes (if applicable).
    Only suggest fixes that are found in the known issues and fixes.
    Only suggest the fix or fixes that are related to the issue the user is having.
    DO NOT give the users any fixes that are not in the lists of known issues and fixes.
    If the user sends an issue that does not have a fix tell them that that problem has no currently known fix.

Your Task:

A user reported the following issue: "{user_query}"

Using the known issues and fixes listed below, create a comprehensive troubleshooting guide. Break it down into clear steps, and if the solution requires any system modifications, provide the necessary details and instructions for the user to follow. If the issue is known but cannot be resolved, mention potential future fixes or workarounds.

Known Issues and Fixes:

{context}

Notes for Handling Specific Issues:

    If the issue involves networking (e.g., connectivity problems), check if the user’s network settings and firewall configurations are correct.
    If the user mentions crashes or game instability, recommend checking the game’s log files or verifying mod files.
    Always suggest restarting the game or system as a first step before diving into more complex fixes.
    Be polite, understanding, and offer encouragement throughout the process.
    """
    
    response = ollama.chat(model="gemma:2b", messages=[{"role": "user", "content": prompt}])
    return response['message']['content']

# Flask API setup
app = Flask(__name__)
CORS(app)
documents = load_issues()
vectorstore = initialize_vectorstore(documents)

@app.route("/support", methods=["POST"])
def support():
    data = request.json
    query = data.get("query", "").strip()
    if not query:
        return jsonify({"error": "Missing query"}), 400
    
    response = generate_response(query, vectorstore)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1423, debug=True)