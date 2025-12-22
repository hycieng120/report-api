FROM python:3.12-slim

WORKDIR /app
COPY . .

RUN pip install --upgrade pip setuptools wheel
RUN pip install --only-binary=:all: -r requirements.txt

CMD ["gunicorn", "quant_app.app:api"]