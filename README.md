# GitHub Webhook Receiver (Flask + MongoDB)

## 📌 Overview

This project implements a GitHub Webhook listener using Flask.  
It captures GitHub events and stores them in MongoDB Atlas.

Supported events:
- Push
- Pull Request
- Merge (extra handling)

The stored events can be retrieved through a REST API endpoint.

---

## 🛠 Tech Stack

- Python
- Flask
- MongoDB Atlas
- PyMongo
- python-dotenv
- Ngrok (for exposing local server)

---

## 🚀 Features

- Receives GitHub webhook payloads
- Processes push and pull request events
- Detects and stores merge events
- Stores structured event data in MongoDB
- Secure configuration using environment variables
- REST endpoint to fetch stored events

---
