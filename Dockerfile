FROM python:3.10-alpine

WORKDIR /app

COPY requirements.txt .

# 
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# 
COPY . .

# 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]