FROM python:3.10

WORKDIR /app

COPY . /app

RUN pip install google-generativeai pydantic playwright

RUN mkdir -p /home/rashi/.openclaw
RUN cp -r workspace /home/rashi/.openclaw/

ENV PORT=8080
EXPOSE 8080

RUN echo "force rebuild"

CMD ["python", "run.py"]
