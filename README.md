# Проект YaMDb

> Проект YaMDb представляет собой платформу для сбора отзывов пользователей на различные произведения и создания рейтингов этих произведений. На этой платформе пользователи могут оценивать и комментировать книги, фильмы, музыку и другие виды произведений.

## Основные возможности

Пользователи могут оценивать произведения в диапазоне от 1 до 10 и оставлять текстовые отзывы.
Произведения делятся на категории, такие как "Книги", "Фильмы", "Музыка" и другие.
Каждое произведение может иметь несколько жанров.
Пользователи могут просматривать рейтинги произведений и читать отзывы.
Аутентифицированные пользователи могут добавлять отзывы и комментарии к произведениям.
Администраторы имеют право добавлять и редактировать произведения, категории и жанры.

## Установка

1. Клонируйте репозиторий с проектом на свой компьютер:
```
git clone git@github.com:SHURSHALO/api_yamdb.git
```
2. Перейдите в директорию проекта:
```
cd api_yamdb
```
3. Создайте виртуальное окружение и активируйте его:
```
py -3.9 -m venv venv
```
```
source venv/Scripts/activate
```
4. Установите зависимости проекта:
```
pip install -r requirements.txt
```
5. Примените миграции:
```
cd api_yamdb
```
```
python manage.py migrate
```
## Запуск
Запустите локальный сервер разработки:
```
python manage.py runserver
```
Откройте веб-браузер и перейдите по адресу http://127.0.0.1:8000/ для доступа к проекту.

# Использование платформы

Для начала работы с платформой зарегистрируйтесь как новый пользователь.

После регистрации войдите в систему, используя свой логин и пароль.

Перейдите к разделу с произведениями и начните оценивать и комментировать произведения.

Для администраторов доступен раздел администрирования, где можно добавлять и редактировать произведения, категории и жанры.

### Команда
https://github.com/vlad786901

https://github.com/NRenat

