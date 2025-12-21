FROM python:3.11-slim

RUN pip install awslambdaric

WORKDIR /var/task

COPY lambda_function.py .
COPY requirements.txt .

RUN pip install -r requirements.txt

CMD ["python", "-m", "awslambdaric", "lambda_function.lambda_handler"]