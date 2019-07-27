FROM python:3.7-alpine
WORKDIR /app
RUN apk add --update --no-cache g++ gcc libxslt-dev
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8080
CMD python -m aiohttp.web -H 0.0.0.0 -P 8080 proxy:init_app