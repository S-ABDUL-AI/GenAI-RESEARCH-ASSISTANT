# ============================
# 📘 GenAI Research Assistant
# ============================

# Use official lightweight Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Prevent Python from writing pyc files & buffering
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies (only what's needed for pdfplumber + Pillow)
RUN apt-get update && apt-get install -y \
    build-essential \
    libjpeg-dev \
    zlib1g-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libtiff5-dev \
    libwebp-dev \
    tcl8.6-dev tk8.6-dev python3-tk \
    ghostscript \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Streamlit entrypoint
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
