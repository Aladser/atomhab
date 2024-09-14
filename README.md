#### Настройки проекта
+ Создать файл .env в корне проекта с настройками, аналогичными .env.example.
+ ``python manage.py createusers`` - создать пользователей
+ ``python manage.py seed`` - сидирование таблиц
+ JWT - авториазция
+ Запуск отложенных задач: ``celery -A config worker -l INFO``
+ Запуск периодических задач: ``celery -A config worker --beat --scheduler django --loglevel=info``
