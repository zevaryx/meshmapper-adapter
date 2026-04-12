# MeshMapper Webhook Adapter

## Getting Started

1. Copy `config.example.yaml` to `config.yaml` and edit it to meet your needs
2. Copy `compose.example.yaml` to `compose.yaml` and edit it to meet your needs
3. Run `docker compose up --build --force-recreate -d`
4. Point your MeshMapper admin panel at `https://your.website.tld/webhook`

## Database backing

This adapter supports MongoDB database backing for alerts for admins to use. The default `compose.example.yaml` file automatically spins up a database configured to use the default credentials in `config.example.yaml`, but you can modify `compose.yaml` file to save to an external database

## 3rd Party API

This adapter also supports 3rd party API collection via the `/ingest` endpoint, allowing you to collect pings separately from MeshMapper if you have a need for it. This requires the MongoDB database backing to work!

To use, use the following URL, replacing `your.website.tld` with your URL:

`https://your.website.tld/ingest`

For the API key, please go to the `/docs` URL and manually modify the info under `/api/v1/auth/register` section to register. Clunky, but temporary until there's a registration page