# Base on slim Python 3.10
FROM python:3.10-slim

# Set working dir
WORKDIR /app

# Install system deps
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download NLTK data (vader_lexicon)
RUN python -m nltk.downloader vader_lexicon

# Copy app code & data
COPY models/ ./models/
COPY data/   ./data/

# Expose Streamlit port
EXPOSE 8501

# Default command
CMD ["streamlit", "run", "models/sentiment_recommender_app.py", \
     "--server.port=8501", "--server.address=0.0.0.0"]
