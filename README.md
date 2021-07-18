### **Установка и запуск**
**1. BACK**

1.1. python3 -m venv venv

1.2. source venv/bin/activate

1.3. pip install -r requirements.txt

1.4. Узнать свой IP локальный и прописать его в online_store/settings/ALLOWED_HOSTS

1.5. python manage.py runserver 0.0.0.0:8000

1.6. celery -A online_store worker --loglevel=info

**2. FRONT**

2.1 git clone https://github.com/lolsecret/react_online_store.git

2.2. pip install nodejs

2.3. npm install

2.4. react_online_store > package.json > proxy заменить на свой ID 

2.5. npm start

### **Работа**
Выбираете товар и нажимаете купить. Пользователю отправляется СМС-сообщение с рандомной задержкой  между двумя временами
указанными в настройках (от и до).
Пользователя перебрасывает на Опросник(один вопрос - одна страница).
После всех ответов появляется страница с благодарностью

Эксель.
По ссылке /excel выбираете две даты и нажимаете скачать. 
В екселе данные по Опроснику

**Ссылки**

/excel - Эксель файл с выбором даты (от и до)

/questionary - Опросник

** Если потребуется проверить как отправляется СМС по условию в react_online_store > main.js > mobile_phone меняете на 
свое значение