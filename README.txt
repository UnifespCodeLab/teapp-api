## Para executar com Docker

- Construa a imagem com `docker build -t ibeac-api .` no diretório com o arquivo `Dockerfile`

- Rode `docker run -d -t ibeac-api` para executar em modo desacoplado (-d)

- Use `docker network inspect bridge` para identificar o IṔ do container e utilize-o para fazer as requisições sobre a porta 8000

## Para executar com docker-compose
- Build: ```docker-compose build```

- Executar: ```docker-compose up flask-api```

- Verificar: ```http://172.18.0.2:8000/```