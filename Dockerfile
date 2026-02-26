FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install fastapi uvicorn google-generativeai pydantic playwright

RUN mkdir -p /home/rashi/.openclaw
RUN cp -r workspace /home/rashi/.openclaw/

ENV PORT=8080

EXPOSE 8080

CMD ["python", "-u", "run.py"]
