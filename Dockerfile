FROM python:3.10.6-alpine

# ENV PYTHONUNBUFFERED 1
# WORKDIR /app
# COPY requirements.txt requirements.txt
# RUN pip install --no-cache-dir --upgrade -r requirements.txt
# COPY ./app .
# CMD ["uvicorn", "main:app","--host", "0.0.0.0" ,"--port", "80"]

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./app . 

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
CMD ["python", "main.py"]
# If running behind a proxy like Nginx or Traefik add --proxy-headers
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--proxy-headers"]
