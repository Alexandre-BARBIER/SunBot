FROM python:3.11-bookworm

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# Run the Python script using the Python 3 interpreter
CMD ["python3", "main.py"]