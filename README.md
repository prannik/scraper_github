# SCRAPER_GITHUB
<hr>
Проект парсинга данных репозиториев пользователей или проектов
<hr>
Краткое описание работы 

<li>Парсер начинает свою работу с получения пути к файлу со списком ссылок на страницы пользователей (или
проектов)
<li>В функции инициализации(def __init__) start_urls заполняется ссылками из файла
<li>Перейдя по ссылке, парсер в 'def parse' определяет, в каком именно он аккаунте (аккаунт пользователя или 
аккаунт проекта)
<li>Исходя из особенности аккаунта парсер продолжает работу либо в 'def parse_person', либо 'def parse_org' 
соответственно
<li>Перейдя на страницу с репозиториями аккаунта, парсер передает в 'def parse_repository', ссылку на каждый 
отдельный репозиторий
<li>Перейдя в отдельный репозиторий 'def parse_repository' начинает сбор данных о нем 
<li>Закончив работу по сбору данных, парсер возвращается на страницу с репозиториями и повторяет процесс с 
репозиториями, в которых еще не был
<li>Пройдясь по всем репозиториям на этой странице (максимум их 30 на одной странице), парсер проверяет, есть ли 
переход на следующую страницу
<li>Если переход обнаружен, парсер повторяет 5 последних действий (включая это) до тех пор, пока не 
соберет 
информацию о каждом Публичном репозитории в этом аккаунте
<li>Одновременно со всем, что написано выше, парсер подключается к базе данных (в моем случае PostgreSQL) и создает 
таблицу (имя таблицы указывается в models.py -> class RepItems -> '__tablename__')
<li>После выполнения 'def parse_repository' данные добавляются в таблицу
<li>Структура таблицы описана ниже
<hr>
Развертывание проекта:

```
$ mkdir 'name_directory_project' 
$ cd 'name_directory-project'
$ python3 -m venv venv
$ source venv/bin/activate
$ git init
$ git clone https://github.com/prannik/scraper_github.git
// or
// git clone git@github.com:prannik/scraper_github.git
$ cd scraper_github
$ pip install -r requirements.txt
$ > .env
```
Последней командой мы создали файл '.env' для хранения переменных окружения. Запишите в ваши личные параметры для 
базы данных PostgreSQL:
    
    '''Файл заполняется без пробелов и ковычек'''
    DATABASE_NAME='your_database_name'
    DATABASE_USER='your_database_username'
    DATABASE_PASSWORD='your_database_password'
    DATABASE_HOST='your_database_host'
    DATABASE_PORT='your_database_port'

В файле 'list_repository.txt'(он добавлен для примера) указан список профилей для парсинга данных. Можно использовать 
любой другой необходимый 
вам файл с ссылками, просто нужно указать для него путь при вызове scrapy.
Для примера используются следующие ссылки:

    https://github.com/scrapy 
    https://github.com/celery/

Далее:
```
$ cd scraper_github
```
Теперь можно использовать наш скрапер, для этого выполняется команда:
```
// path - Путь к вашему файлу с сcылками
$ scrapy crawl parsing -a path='path'
```


Если есть необходимость записать JSON файл, выполняется команда:

```
// -O будет перезаписывать ваш JSON файл каждый раз по новой  
// -o будет добавлять данные в конец файла
$ scrapy crawl parsing -a path='path' -O jsonfile.json
```
<hr>
После выполнения последних команд в базе данных, которую вы подключили, будет создана таблица 'github_repository'.

Структура данной таблицы следующая:
    
    КОЛОНКА                 ТИП ДАННЫХ

    author                  String
    title                   String
    about                   TEXT
    url                     URLType
    stars                   INTEGER
    forks                   INTEGER
    watching                INTEGER
    commits                 INTEGER
    last_commits            JSONB
    releases                INTEGER
    last_releases           JSONB

    


