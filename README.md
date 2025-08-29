# Real-Time Stock Analysis Pipeline (Learning Project)

A complete, serverless, event-driven data pipeline built on Microsoft Azure to ingest, process, and visualize real-time stock price data. This project was undertaken to gain hands-on experience with modern, full-stack cloud architecture for handling and presenting streaming data.

## 🎯 Project Goal & Learning Objectives

In the world of financial services, the ability to process and act on market data in real-time is crucial. **This project was designed as a deep dive into cloud architecture to learn how to solve this challenge.** The primary learning objective was to design and build a fully serverless pipeline that could fetch live stock prices, perform time-series calculations (like a 5-minute moving average), and display the results on a live-updating web dashboard, all while adhering to cloud best practices like security and cost-effectiveness.

## ✨ Key Features & Components

* **Automated Data Ingestion:** A serverless Python function runs on a schedule to automatically fetch the latest stock price from an external API.
* **Scalable Event Streaming:** Azure Event Hubs is used to ingest the stream of raw price data, capable of handling millions of events per second.
* **Real-Time Data Processing:** An Azure Stream Analytics job processes the data in-flight, using a time-window query to calculate a 5-minute moving average.
* **Secure & Passwordless Architecture:** The entire pipeline is secured using Azure Managed Identities, eliminating the need for storing secrets or connection strings in code.
* **Resilient Frontend Dashboard:** A custom-built frontend, hosted on Azure App Service, calls a secure API endpoint to fetch the processed data. It includes error handling to inform the user if the backend API is unavailable.
* **Serverless & Cost-Effective:** The architecture uses consumption-based services, demonstrating an understanding of cloud cost management principles.

## 🛠️ Tech Stack

* **Backend Compute:** Azure Functions (Python)
* **Data Streaming:** Azure Event Hubs
* **Real-Time Analytics:** Azure Stream Analytics
* **Data Storage:** Azure Blob Storage
* **Frontend Hosting:** Azure App Service (Free Tier)
* **Security:** Azure Managed Identity, CORS
* **Frontend Libraries:** Chart.js, Express.js

## 🚀 Key Learnings & Challenges

**As a learning project, the challenges encountered were the most valuable part of the experience.** A key challenge was debugging authentication and permission issues between services, which provided a deep understanding of Azure's identity and access management (IAM) and the importance of Managed Identities. A major success was building a resilient custom frontend and a secure API, demonstrating the ability to connect backend data processing with a user-facing application that can handle real-world API downtime. Writing the Stream Analytics query to use `TumblingWindow` was also a key learning for performing time-series analysis.

---
# Architecture Diagram
![Architecture Diagram](http://url/to/img.png](https://lucid.app/publicSegments/view/4777dbde-7768-4eeb-b368-4c5194778a84/image.png)
