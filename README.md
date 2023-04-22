# Foodgram

Workflow status

https://github.com/IskanderRRR/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg

Адресс проекта - http://pepegas.ddns.net

1. Чтобы развернуть проект зайдите в папку /infra и выполните команду запуска фоновой сборки.
```bash
docker-compose up -d --build
```
2. После успешного запуска контейнеров выполниете команда и создайте суперпользоателя.
```bash
docker-compose exec backend python manage.py migrate 
docker-compose exec backend python manage.py load_data_csv
docker-compose exec backend python manage.py createsuperuser 
docker-compose exec backend python manage.py collectstatic --no-input
```
3. Готово:
    -  http://localhost/ - главная страница сайта;
    -  http://localhost/admin/ - админ панель;
    -  http://localhost/api/ - API проекта
    -  http://localhost/api/docs/redoc.html - документация к API
4. Админ:
Почта: pepega@pepega.com
Пароль: pepega

---
## Автор
**[Iskander Ryskulov](https://github.com/IskanderRRR)**
