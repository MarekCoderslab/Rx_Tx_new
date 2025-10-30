FROM python:3.10-slim

WORKDIR /app

COPY rx_tx_CSV.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "rx_tx_CSV.py"]

