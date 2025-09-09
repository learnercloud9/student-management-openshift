FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

# Run the Flask app with gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
