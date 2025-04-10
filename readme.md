Instructions to run the app

## Docker Commands

- `docker-compose build` - Build the container images
- `docker-compose up` - Build (if needed) and start the containers
- `docker-compose up -d` - Build (if needed) and start the containers in detached mode (background)
- `docker-compose up -d --build` - Force rebuild and start the containers in detached mode
- `docker-compose ps` - Check status once its running
- `docker-compose down` - Stop and remove containers

## Curl command for predictions

curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [38.2, 18.1, 18.5, 38]}'

[44.9, 13.3, 21.3, 51.0]

curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [44.9, 13.3, 21.3, 51.0] }'
