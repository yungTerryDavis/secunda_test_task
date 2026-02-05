# Secunda Test
## Launch
Запуск для проверки тестового задания
```sh
docker-compose up
```
После этого сервер будет доступен по http://localhost:8000/  
Документация на http://localhost:8000/docs

Если автоматически не соберется, можно вручную сбилдить Docker-образ, и указать в docker-compose image.
## Develop
### Dependencies
Запуск БД
```sh
docker-compose up -d db
```
Создание venv и установка зависимостей
```sh
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
Для применения переменных среды создать файл *.env* на подобие *example.env*.

Применение миграций
```sh
alembic upgrade head
```
Запуск сервера
```sh
uvicorn main:app
```

