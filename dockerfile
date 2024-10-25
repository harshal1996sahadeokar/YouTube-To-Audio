# Backend (Python Flask + yt-dlp)
FROM python:3.9-slim

# Install yt-dlp and Flask
RUN pip install Flask yt-dlp werkzeug

# Set up the application directory
WORKDIR /app
COPY backend/ /app/

# Expose the Flask port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
