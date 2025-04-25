import os
import json
import hashlib
import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)  # ✅ Initialize Flask app before routes
CORS(app)

# Function to load blockchain from file
def load_blockchain():
    if os.path.exists("blockchain.json"):
        with open("blockchain.json", "r") as file:
            return json.load(file)
    return []

# Function to save blockchain to file
def save_blockchain(blockchain):
    with open("blockchain.json", "w") as file:
        json.dump(blockchain, file, indent=4)

blockchain = load_blockchain()

# Function to create a new block
def create_block(transaction_data):
    block = {
        'index': len(blockchain) + 1,
        'timestamp': str(datetime.datetime.now()),
        'transaction': transaction_data,
        'previous_hash': blockchain[-1]['hash'] if blockchain else '0',
    }
    block['hash'] = hashlib.sha256(str(block).encode()).hexdigest()
    blockchain.append(block)
    save_blockchain(blockchain)  # ✅ Save blockchain after adding new block
    return block

@app.route("/", methods=["GET"])
def welcome():
    return jsonify({"message": "Welcome to AI-Powered Blockchain Payments API!"})

@app.route("/mine_block", methods=["GET"])
def mine_block():
    new_block = create_block({"data": "New Transaction"})
    return jsonify({"message": "Block Mined!", "block": new_block})

@app.route("/get_chain", methods=["GET"])
def get_chain():
    return jsonify({"blockchain": blockchain, "length": len(blockchain)})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
