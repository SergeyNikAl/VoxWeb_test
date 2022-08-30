# Тестовое задание python-разработчик в VoxWeb
### В проекте предусмотрено:
- Новости сервисов Яндекс.Маркет и Озон;
- Наполняет базу данных новостями, включая ссылки, теги и т.д.;
- Реализован API к эндпоинтам 'api/news' и 'api/tags'.

### Стек технологий:
- Python
- Django
- Django Rest Framework
- MySQL
- Selenium
- AdminLTE3

### Запуск проекта локально
Клонировать репозиторий и перейти в него:
```
git clone https://github.com/SergeyNikAl/foodgram-project-react.git
```
Создать и активировать виртуальное окружение, обновить pip и установить зависимости:
```
python -m venv venv
source venv/Scripts/activate - для Windows
source venv/bin/activate - для Mac/Linux
python -m pip install --upgrade pip
pip install -r news/requirements.txt
```
### Для запуска локально:
В каталоге, где расположен файл manage.py создать .env. Пример заполнения:
```
SECRET_KEY=*****
DB_ENGINE=django.db.backends.mysql
DB_NAME= (названние БД) - voxbet
MYSQL_USER= (ваш пользователь) - root
MYSQL_PASSWORD= (пароль для входа в БД) - root
DB_HOST=localhost (при запуске на локальной машине)
DB_PORT=3306
```
### Создать базу данных и загрузить шаблоны AdminLTE3:
```
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
```
### Для работы с Selenium 
(для Google Chrome) необходимо скачать файл chromedrive, предварительно проверив версию своего браузера, с сайта:
````
https://chromedriver.chromium.org/downloads
````
Не устанавливая exe файл, разместить его в папке парсер, предварительно распокава его.

### Запустить парсер для парсинга сервисов и выгрузки данных в БД:
Скопировать файл .env в папку parser для возможности подключения к БД и автоматической выгрузки полученных данных.
```
cd parser
python parser.py
```
### Запуск локального сервера
```
cd news
python manage.py runserver
```
### Эндпоинты
#### Админ-панель
- (http://127.0.0.1:8000/admin)
#### API
- (http://127.0.0.1:8000/api/news/)
- (http://127.0.0.1:8000/api/tags/)
