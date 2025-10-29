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
python train.py
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


## **Core Concept Questions**

### 🔹 **1. Model Training vs Deployment**

* In *our project*, model training happens in a **Python script** (`train_model.py`) where we use **scikit-learn’s Iris dataset** and train a classifier such as `RandomForestClassifier` or `LogisticRegression`.
* Deployment is done by the **Flask app (`app.py`)**, which loads the saved model and exposes it via the `/predict` endpoint.

---

### 🔹 **2. Saving Model with Joblib/Pickle**

* We save the trained model using:

  ```python
  joblib.dump(model, 'model.joblib')
  ```

  and in our Flask API, we load it using:

  ```python
  model = joblib.load('model.joblib')
  ```

  This allows the API to start instantly without retraining each time.

---

### 🔹 **3. REST API Advantage**

* We expose two REST endpoints:

  * `GET /health` → to check API status
  * `POST /predict` → to send input features and receive predicted species (`setosa`, `versicolor`, or `virginica`)

This makes our ML model reusable — by web applications, mobile clients, or other backend services.

---

### 🔹 **4. HTTP Methods**

* `GET /health` → returns `"API is healthy"` to verify that the service is running.
* `POST /predict` → accepts JSON input like:

  ```json
  {"input": [5.1, 3.5, 1.4, 0.2]}
  ```

  and returns:

  ```json
  {"prediction": "Iris-setosa"}
  ```

---

### 🔹 **5. Docker Importance**

* We create a `Dockerfile` that uses a Python base image, installs dependencies from `requirements.txt`, and runs Gunicorn to serve the Flask app.
* Docker ensures our application runs consistently across different environments — local machines, servers, or cloud platforms — without dependency conflicts.

---

### 🔹 **6. Docker Consistency**

* Our Dockerfile defines everything needed to reproduce the runtime environment:

  ```dockerfile
  FROM python:3.10-slim
  COPY . /app
  RUN pip install -r requirements.txt
  CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
  ```

  This ensures the application behaves identically in all environments.

---

### 🔹 **7. Role of `requirements.txt`**

* We create a `requirements.txt` file listing dependencies:

  ```
  flask
  scikit-learn
  joblib
  gunicorn
  ```

  This helps Docker (and others) install the exact versions of libraries required to run our API successfully.

---

### 🔹 **8. Exposing Ports**

* In our Dockerfile:

  ```dockerfile
  EXPOSE 5000
  ```
* When running the container:

  ```bash
  docker run -p 5000:5000 iris-api
  ```

  This maps the internal container port (5000) to the host machine’s port so we can access the Flask API via browser or Postman at `http://localhost:5000`.

---

### 🔹 **9. Scaling to 1000 req/sec**

* Our setup uses Gunicorn, which is production-ready.
* To scale:

  * Increase Gunicorn workers:

    ```bash
    gunicorn -w 4 -b 0.0.0.0:5000 app:app
    ```
  * Run multiple containers using Docker Compose or Kubernetes.
  * Load balance requests using Nginx or a cloud load balancer.

---

### 🔹 **10. Security for ML APIs**

In our Iris API:

* Validate JSON input to ensure it contains four numeric values.
* Restrict public access to `/predict` using authentication or API keys.
* Use HTTPS when deploying online.
* Log requests and prediction outputs for monitoring.
* Sanitize inputs to prevent injection or malicious data attacks.

---
