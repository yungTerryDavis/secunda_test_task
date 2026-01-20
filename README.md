# Secunda Test
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