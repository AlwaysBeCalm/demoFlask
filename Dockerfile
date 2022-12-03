FROM python:3.9-alpine

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT ["gunicorn"]
CMD ["app:create_app()", "-b", "0.0.0.0:5000", "-w", "1"]
