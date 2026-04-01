## Installation
```bash
git clone https://github.com/everi59/backend-tochka-marketplace
cd backend-tochka-marketplace
cp .env.docker.example .env.docker
docker-compose up -d --build
docker-compose exec api alembic upgrade head
curl http://localhost:8000/health
```