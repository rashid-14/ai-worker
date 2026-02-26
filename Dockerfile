FROM python:3.10

WORKDIR /app

COPY . /app

RUN pip install google-generativeai pydantic playwright

RUN mkdir -p /home/rashi/.openclaw
RUN cp -r workspace /home/rashi/.openclaw/

RUN echo "force rebuild"

EXPOSE 8080
ENV PORT=8080

CMD ["python", "run.py"]
