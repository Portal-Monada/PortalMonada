# Django Docker

Estrutura Padrão Inicial do Projeto

## Configuração

No diretório raiz do projeto vamos criar o arquivo `.env` com o seguinte conteúdo:

```
SECRET_KEY=your_secret_key
DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,0.0.0.0
DATABASE_ENGINE=postgresql_psycopg2
DATABASE_NAME=dockerdjango
DATABASE_USERNAME=dbuser
DATABASE_PASSWORD=dbpassword
DATABASE_HOST=db
DATABASE_PORT=5432
DJANGO_LOGLEVEL=INFO
```

Para construir a aplicação executamos o seguinte comando:

```
docker-compose build
```

Então podemos executar o projeto:

```
docker-compose up
```

Conectando ao banco de dados:

```
docker-compose exec db bash
psql --username=dbuser --dbname=dockerdjango
```

Acessando o shell da aplicação web:

```
docker-compose exec django-web bash
docker exec -it portalmonada sh
```
