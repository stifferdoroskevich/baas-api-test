FROM python:3.7-alpine
WORKDIR /code
ENV FLASK_APP server.py
ENV FLASK_RUN_HOST 0.0.0.0
RUN apk update && apk add --no-cache postgresql-dev gcc python3-dev musl-dev
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["flask", "run"]