docker build -t fakeapi .
docker run --name serveit -p 8080:8080 fakeapi
