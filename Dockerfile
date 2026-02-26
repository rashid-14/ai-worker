FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install google-generativeai pydantic playwright

ENV OPENCLAW_HOME=/app
ENV OPENCLAW_WORKSPACE=/app/workspace

CMD ["python", "run.py"]
