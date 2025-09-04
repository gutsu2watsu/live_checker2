# 📺 YouTube Live Status Microservice

This is a lightweight microservice that checks if a list of YouTube channels are currently live using [`yt-dlp`](https://github.com/yt-dlp/yt-dlp), and exposes the results through a FastAPI REST API.

Ideal for monitoring live stream activity across multiple channels, this service is built to run continuously and efficiently in a containerized environment.

---

## 🚀 Features

- 🔍 Periodically checks multiple YouTube channels for live status
- 🧠 Caches results in memory for quick access
- 🌐 Simple FastAPI REST API
- 🐳 Dockerized for portability and deployment
- ✅ Ignores scheduled streams (only shows active lives)

---

## 📦 Project Structure

live-checker/
├── app/
│ ├── main.py # FastAPI application logic
│ └── requirements.txt # Python dependencies
├── Dockerfile # Docker container configuration
└── docker-compose.yml # Docker Compose file (optional)


---

## ⚙️ Configuration

To add or remove YouTube channels, edit the `CHANNEL_IDS` dictionary in `app/main.py`:

```python
CHANNEL_IDS = {
    "UCxxxxxxxxxxxxx": "YourChannelName",
    ...
}

Each key is a YouTube channel ID, and the value is a human-readable channel name.
🐳 Running with Docker
1. Clone the repository

git clone https://github.com/yourusername/live-checker.git
cd live-checker

2. Build the Docker image

docker build -t live-checker .

3. Run the container

docker run -p 8000:8000 live-checker

The service will be available at:

http://localhost:8000/live-status/all

🧩 Running with Docker Compose (Optional)

To use Docker Compose:

docker compose up --build

This will expose the app on port 8000 by default.
🧪 API Endpoints
Method	Endpoint	Description
GET	/live-status/all	Returns cached status of all channels







🔧 Requirements (if not using Docker)

    Python 3.10+

    yt-dlp

    FastAPI

    Uvicorn

    ffmpeg (optional, but useful)

Install dependencies manually:

pip install -r app/requirements.txt

Run the app:

uvicorn app.main:app --host 0.0.0.0 --port 8000
