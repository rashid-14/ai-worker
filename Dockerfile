FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install google-generativeai pydantic playwright

# Create OpenClaw expected home
RUN mkdir -p /home/rashi/.openclaw
RUN cp -r workspace /home/rashi/.openclaw/

CMD ["python", "run.py"]
