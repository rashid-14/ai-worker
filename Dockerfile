FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /home/rashi/.openclaw
RUN cp -r workspace /home/rashi/.openclaw/

EXPOSE 8080

CMD ["sh", "-c", "uvicorn run:app --host 0.0.0.0 --port $PORT"]
