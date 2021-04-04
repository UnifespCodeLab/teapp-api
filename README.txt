*Para executar com Docker*

- Construa a imagem com `docker build -t ibeac-api .` no diretório com o arquivo `Dockerfile`

- Rode `docker run -d -t ibeac-api` para executar em modo desacoplado (-d)

- Use `docker network inspect bridge` para identificar o IṔ do container e utilize-o para fazer as requisições sobre a porta 8000
