FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install google-generativeai pydantic playwright

# Create OpenClaw home properly
RUN mkdir -p /home/rashi/.openclaw

RUN cp -r agents /home/rashi/.openclaw/ || true
RUN cp -r skills /home/rashi/.openclaw/ || true
RUN cp -r workspace /home/rashi/.openclaw/ || true
RUN cp -r logs /home/rashi/.openclaw/ || true
RUN cp openclaw.json /home/rashi/.openclaw/ || true

ENV OPENCLAW_HOME=/home/rashi/.openclaw
ENV OPENCLAW_WORKSPACE=/home/rashi/.openclaw/workspace

CMD ["python", "run.py"]
