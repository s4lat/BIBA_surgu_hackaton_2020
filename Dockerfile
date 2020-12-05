FROM python:3.8-alpine
WORKDIR /crime
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
# RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 1337
COPY . .
CMD ["flask", "run"]
