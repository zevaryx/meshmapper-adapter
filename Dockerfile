FROM python:3.14

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir --upgrade .

#CMD ["fastapi", "run", "app/main.py", "--port", "80"]

# If running behind a proxy like Nginx or Traefik add --proxy-headers
CMD ["fastapi", "run", "main.py", "--port", "80", "--proxy-headers"]