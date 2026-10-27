FROM python:3.14-slim
WORKDIR /app
COPY requirements.txt .
RUN python3 -m pip install --no-cache-dir -r requirements.txt
COPY wordle/ wordle/
RUN useradd --create-home app
USER app
EXPOSE 8000
CMD ["uvicorn", "wordle.api:app", "--host", "0.0.0.0", "--port", "8000"]
