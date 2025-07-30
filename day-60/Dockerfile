# day-60/Dockerfile

# 1) Base image
FROM python:3.10-slim

# 2) System deps for C extensions
RUN apt-get update && \
    apt-get install -y build-essential gcc g++ && \
    rm -rf /var/lib/apt/lists/*

# 3) Set workdir
WORKDIR /app

# 4) Copy only requirements first (to leverage cache)
COPY day-60/requirements.txt .

# 5) Upgrade pip and install core FastAPI/Uvicorn first
RUN pip install --upgrade pip && \
    pip install --no-cache-dir fastapi uvicorn[standard]

# 6) Install the rest of your Python deps
RUN pip install --no-cache-dir -r requirements.txt

# 7) Copy the application code
COPY day-60/ .

# 8) Expose and run
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
