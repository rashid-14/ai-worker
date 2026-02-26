FROM python:3.10

WORKDIR /app
COPY . .

RUN pip install google-generativeai pydantic playwright

# Create OpenClaw runtime folder for Railway
RUN mkdir -p /.openclaw
RUN cp -r workspace /.openclaw/

ENV OPENCLAW_HOME=/.openclaw
ENV OPENCLAW_WORKSPACE=/.openclaw/workspace

CMD ["python", "run.py"]
