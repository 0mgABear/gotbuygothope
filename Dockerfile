FROM python:3.11-slim

RUN pip install awslambdaric

WORKDIR /var/task

COPY function.py .
COPY requirements.txt .

RUN pip install -r requirements.txt

CMD ["python", "-m", "awslambdaric", "function.lambda_handler"]