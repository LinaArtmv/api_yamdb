# api_yamdb
api_yamdb
### Описание
Проект YaMDb собирает отзывы пользователей на различные произведения.
В проекте реализован API для всех моделей приложения YaMDb,
благодаря чему программа может взаимодействовать с другими программами.
Это позволяет расширить функциональность проекта и связывать его с другими.
### Запуск проекта
- Установите и активируйте виртуальное окружение
```
python -m venv venv
source venv/scripts/activate
``` 
- Установите зависимости из файла requirements.txt
```
pip install -r requirements.txt
``` 
- Выполните миграции:
```
cd api_yamdb/
python manage.py migrate
```
- Загрузите в БД тестовые записи (опционально):
```
python manage.py load
```
- В папке с файлом manage.py выполните команду:
```
python manage.py runserver
```
### Примеры запросов к API и ответов от сервера

- Пример POST-запроса на адрес 
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/ 
для добавления отзыва: 
```
{
"text": "Интересная книга!",
"score": 8
}
```

Пример ответа:

```
{
"id": 1,
"text": "Интересная книга!",
"author": "natalya",
"score": 8,
"pub_date": "2023-05-27T14:15:22Z"
}
```
- GET-запрос на адрес http://127.0.0.1:8000/api/v1/users/{username}/ для получения пользователя по username.

Пример ответа:

```
{
"username": "string",
"email": "user@example.com",
"first_name": "string",
"last_name": "string",
"bio": "string",
"role": "user"
}
```
### Технологии
- Python 3.7
- Django 3.2
### Авторы
- Ангелина Артемьева (тимлид),
github: LinaArtmv
- Александр Стерлягов,
github: AlexSt3
- Наталья Фанькина,
github: NatalyaF8
