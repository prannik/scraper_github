SCRAPER_GITHUB
<hr>
Проект парсинга данных репозиториев пользователей или проектов
<hr>
Развертывание проекта:

```
mkdir 'name_directory_project' 
cd 'name_directory-project'
python3 -m venv venv
source venv/bin/activate
git init
git clone https://github.com/prannik/scraper_github.git
# (or)
# git clone git@github.com:prannik/scraper_github.git
cd scraper_github
pip install -r requirements.txt
> .env
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
```
https://github.com/scrapy 
https://github.com/celery/
```

Далее:
```
cd scraper_github
```
Теперь можно использовать наш скрапер, для этого выполняется команда:
```
scrapy crawl parsing -a path='path'
# path - Путь к вашему файлу с сcылками
```


Если есть необходимость записать JSON файл, выполняется команда:

```
scrapy crawl parsing -a path='path' -O jsonfile.json
# -O будет перезаписывать ваш JSON файл каждый раз по новой  
# -o будет добавлять данные в конец файла
```

