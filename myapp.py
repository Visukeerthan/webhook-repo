from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

# MongoDB connection using .env
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)

db = client["github_webhooks"]
collection = db["events"]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    if not data:
        return "No data received", 400

    event = request.headers.get("X-GitHub-Event")

    # ----------------------------
    # PUSH EVENT
    # ----------------------------
    if event == "push":
        author = data["pusher"]["name"]
        to_branch = data["ref"].split("/")[-1]

        event_data = {
            "type": "push",
            "author": author,
            "to_branch": to_branch,
            "timestamp": datetime.utcnow()
        }

        collection.insert_one(event_data)

    # ----------------------------
    # PULL REQUEST EVENT
    # ----------------------------
    elif event == "pull_request":
        action = data["action"]
        pr = data["pull_request"]

        author = pr["user"]["login"]
        from_branch = pr["head"]["ref"]
        to_branch = pr["base"]["ref"]

        # Merge detection (Brownie Points)
        if action == "closed" and pr["merged"]:
            event_type = "merge"
        else:
            event_type = action  # opened, closed, etc.

        event_data = {
            "type": event_type,
            "author": author,
            "from_branch": from_branch,
            "to_branch": to_branch,
            "timestamp": datetime.utcnow()
        }

        collection.insert_one(event_data)

    return "Webhook received", 200


@app.route("/events", methods=["GET"])
def get_events():
    events = list(collection.find({}, {"_id": 0}).sort("timestamp", -1))
    return jsonify(events)


if __name__ == "__main__":
    app.run(debug=True)