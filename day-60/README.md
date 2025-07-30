# 🎧 Recommender API (FastAPI + Docker)

## A FastAPI-powered music/movie recommender API, containerized with Docker and ready to run anywhere

## 🚀 Features

- Built with FastAPI for lightning-fast performance
- Auto-generated Swagger Docs at /docs
- Containerized using Docker
- Ready to deploy to any cloud or local environment

---

## 📦 Image Tags

| Tag      | Description                                  |
| -------- | -------------------------------------------- |
| `latest` | Latest stable release of the recommender api |

---

## 📂 Project Structure

```bash
day-60/
├── Dockerfile                    # Docker build instructions
├── requirements.txt              # Python dependencies
├── app.py                        # FastAPI entrypoint
├── data/
│   ├── tracks.csv
│   └── ratings.csv
├── models/                       # Recommender logic & ML models
│   ├── tfidf_vect.pkl
│   ├── cosine_mtx.npy
│   ├── svd_model.pkl
│   ├── user2idx.pkl
│   ├── item2idx.pkl
└── └── bpr_model.pkl
```

---

## 📦 Build & Run Locally (Docker)

---

## 1️⃣ Clone the repo

```bash
git clone https://github.com/<your-username>/recommender-api.git
cd recommender-api
```

---

---

## 2️⃣ Build the Docker image

```bash
docker build -t xenon6230/recommender-api:latest -f day-60/Dockerfile .
```

---

---

## 3️⃣ Run the container

```bash
docker run -p 8000:8000 xenon6230/recommender-api:latest
```

---

## 🌐 Access the API

- Swagger UI: <http://localhost:8000/docs>

- ReDoc: <http://localhost:8000/redoc>

---

---

## 📤 Pull from Docker Hub (No Build Needed)

```bash
docker pull xenon6230/recommender-api:latest
docker run -p 8000:8000 xenon6230/recommender-api:latest
```

---

## 🛠 Tech Stack

- FastAPI – Python web framework

- Uvicorn – ASGI server

- Docker – Containerization

- (Optional) SQLite/Postgres – Backend database for recommendations

---

---

### Created with ❤️ by xenon6230
