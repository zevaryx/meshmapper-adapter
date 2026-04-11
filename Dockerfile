FROM ghcr.io/astral-sh/uv:alpine

WORKDIR /app

COPY . /app

ENV UV_NO_DEV=1

RUN uv sync --locked

#CMD ["fastapi", "run", "app/main.py", "--port", "80"]

# If running behind a proxy like Nginx or Traefik add --proxy-headers
CMD ["uv", "run", "fastapi", "run", "main.py", "--port", "80", "--proxy-headers"]