# Iris Classifier API

A machine learning web service built using **Flask** and **Docker** that predicts the species of Iris flowers based on sepal and petal measurements.
The project uses the **Iris dataset** from Scikit-learn and a **Random Forest Classifier** for prediction.

---

## Project Overview

This project demonstrates how to:

1. Load and preprocess a dataset (Iris)
2. Train and evaluate a machine learning model
3. Expose predictions through a RESTful API built with Flask
4. Containerize the application using Docker for deployment

---

## Dataset

**Name:** Iris Dataset (built-in to Scikit-learn)
**Features:**

| Feature           | Description         |
| ----------------- | ------------------- |
| sepal length (cm) | Length of the sepal |
| sepal width (cm)  | Width of the sepal  |
| petal length (cm) | Length of the petal |
| petal width (cm)  | Width of the petal  |

**Target Classes:**

* 0 → *Setosa*
* 1 → *Versicolor*
* 2 → *Virginica*

---

## Setup and Installation

### Prerequisites

* Python 3.8+
* pip installed
* Docker (for containerized run)
* (Optional) Postman for testing API endpoints

---

### Clone the Repository

```bash
git clone <your-repo-url>
cd iris-flask-api
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Train the Model

Run the training script:

```bash
python train_model.py
```

This will:

* Load and split the Iris dataset
* Train a **RandomForestClassifier**
* Save the model as `model.joblib`
* Store performance metrics in `metrics.json`

Example output:


<img width="776" height="857" alt="image" src="https://github.com/user-attachments/assets/2057049a-14bf-4f26-94bd-76b0bd9dcd51" />




---

## Run the API Locally

Start the Flask app:

```bash
python app.py
```

You’ll see:

```
 * Running on http://127.0.0.1:5000
```

---

## API Endpoints

### 1️⃣ `GET /`

**Description:** API Information
**Example Response:**

```json
{
  "service": "Iris classifier API",
  "description": "Predict iris species from flower measurements",
  "endpoints": {
    "/health": "Health check",
    "/predict": "Predict iris species from features"
  }
}
```

---

### 2️⃣ `GET /health`

**Description:** Health check
**Example Response:**

```json
{
  "status": "ok",
  "model_loaded": true
}
```

---

### 3️⃣ `POST /predict`

**Description:** Predict iris species from input features

**Request Example (JSON):**

```json
{
  "input": [5.1, 3.5, 1.4, 0.2]
}
```

**Response Example:**

```json
{
  "predicted_class": "setosa",
  "predicted_label": 0,
  "probabilities": [1.0, 0.0, 0.0]
}
```

---

## Testing with Postman

Import the `IrisClassifier.postman_collection.json` file into Postman.

Run:

* `GET /` → API info
* `GET /health` → check model status
* `POST /predict` → send sample input `[5.1, 3.5, 1.4, 0.2]`

---
<img width="1769" height="826" alt="image" src="https://github.com/user-attachments/assets/24bde65a-c6e3-437b-b9c2-ff394de34f94" />

<img width="1769" height="826" alt="image" src="https://github.com/user-attachments/assets/664e6a5c-c810-42d1-bd3a-d68865cf92e1" />


## Build and Run with Docker

### Build Image

```bash
docker build -t iris-api .
```

### Run Container

```bash
docker run -p 5000:5000 iris-api
```

Then test endpoints via browser or Postman at:

```
http://127.0.0.1:5000
```

---

## Example Metrics (from training)

```json
{
  "accuracy": 0.97,
  "precision": 0.97,
  "recall": 0.97,
  "f1_score": 0.97
}
```

---

## Technologies Used

* Python 3
* Flask
* Scikit-learn
* Joblib
* Docker

---



## **Core Concept Answers — Iris Classifier ML Deployment**

---

### **1️⃣ What is the difference between model training and model deployment?**

| Aspect          | Model Training                              | Model Deployment                                  |
| --------------- | ------------------------------------------- | ------------------------------------------------- |
| **Goal**        | Build and optimize a machine learning model | Make the trained model accessible for predictions |
| **Environment** | Development / Jupyter / local scripts       | Production / web server / cloud                   |
| **Process**     | Data preprocessing → training → evaluation  | Load trained model → serve predictions via API    |
| **Tools**       | Scikit-learn, pandas, numpy                 | Flask, FastAPI, Docker, Gunicorn                  |
| **Output**      | `.joblib` or `.pkl` model file              | Running API endpoint (`/predict`)                 |

✅ In short:
**Training** creates the model; **deployment** delivers it for real-world use.

---

### **2️⃣ Why do we save trained models using `joblib` or `pickle`?**

* To **serialize** (save) the trained model object for later use.
* So we **don’t need to retrain** the model every time the API starts.
* `joblib` is optimized for large NumPy arrays (faster, more efficient than pickle).
* Example:

  ```python
  joblib.dump(model, "model.joblib")
  model = joblib.load("model.joblib")
  ```

✅ It ensures **consistency and reproducibility** across environments.

---

### **3️⃣ What are the advantages of serving ML models through REST APIs?**

* **Accessibility:** Anyone can consume predictions via HTTP (web, app, service).
* **Scalability:** Easier to handle multiple users and integrate into systems.
* **Reusability:** Same API can serve multiple applications.
* **Language Agnostic:** Any client (Java, JS, etc.) can call it via HTTP.
* **Centralized Maintenance:** Update model in one place; all clients benefit.

---

### **4️⃣ Explain the purpose of each HTTP method (GET, POST) used in your API.**

| Method    | Endpoint   | Purpose                                              |
| --------- | ---------- | ---------------------------------------------------- |
| **GET /** | `/`        | Returns API information (metadata)                   |
| **GET**   | `/health`  | Health check — ensures API and model are running     |
| **POST**  | `/predict` | Accepts JSON input (features) and returns prediction |

✅ `GET` → retrieve data
✅ `POST` → send data (used when input payload exists)

---

### **5️⃣ What is Docker, and why is containerization important for ML deployment?**

**Docker** is a platform that packages applications with all dependencies into **containers**.

**Importance:**

* Ensures **same environment everywhere** (no “it works on my machine” issues)
* Simplifies **deployment and scaling**
* Makes ML apps **portable, lightweight, and reproducible**
* Each container runs in isolation, avoiding dependency conflicts.

---

### **6️⃣ How does Docker ensure consistency across environments (dev, staging, production)?**

* By using a **Dockerfile** that defines exactly how the app runs:
  OS base image, Python version, libraries, and ports.
* The same image runs identically anywhere — local, server, or cloud.
* No dependency mismatches or missing libraries.

✅ Build once → run anywhere.

---

### **7️⃣ What is the role of `requirements.txt` in Python projects and Docker containers?**

* Lists all Python dependencies required to run the project.
* Example:

  ```
  flask
  scikit-learn
  joblib
  gunicorn
  ```
* Used in Dockerfile:

  ```dockerfile
  RUN pip install -r requirements.txt
  ```

✅ Ensures consistent package versions and reproducible builds.

---

### **8️⃣ Why do we expose ports in Docker containers?**

* Containers are isolated; exposing ports allows **external communication**.
* Flask runs on port 5000 inside the container — exposing it makes it reachable from the host.
* In Dockerfile:

  ```dockerfile
  EXPOSE 5000
  ```
* In run command:

  ```bash
  docker run -p 5000:5000 iris-api
  ```

✅ Maps **container port → host port**.

---

### **9️⃣ How would you scale your API to handle 1000 requests per second?**

* Use a **production WSGI server** (Gunicorn + multiple workers/threads).
* Run **multiple containers** (replicas) behind a load balancer (e.g., Nginx, AWS ALB).
* Use **caching** for repeated predictions.
* Add **asynchronous processing** (Celery, Redis).
* Deploy on **Kubernetes or ECS** for auto-scaling.

✅ Horizontal scaling + load balancing = high throughput.

---

### **🔟 What are some security considerations when deploying ML models as APIs?**

* **Input validation** → prevent malformed JSON or code injection.
* **Authentication & Authorization** → restrict access using API keys/JWT.
* **Rate limiting** → prevent abuse (DDoS).
* **HTTPS** → encrypt data in transit.
* **Model privacy** → don’t expose internal model details or parameters.
* **Logging & monitoring** → detect suspicious usage.

✅ Always treat ML APIs like any web service — secure endpoints and monitor access.

---

Would you like me to format these answers into a **“Theory_Questions.md”** file and include it alongside your project (for submission or viva)?
