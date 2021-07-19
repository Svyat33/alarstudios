# Схема
Впереди стоит нгинкс, за ним три контейнера 
- account - пользователи, залогинивание
- dots - хранит точки и треки пользователей
- buildtrack - отвечает за построение трека. Только показывает возможный маршрут. Не создает его. Рандомно генерит набор точек через которые в принципе можно добраться от указанных точек.
  
Для хранения пользоательских записей используется accountdb, для оповещения сервиса dots о новых пользователях - rabbitmq. account_consumer обеспечивает синхронизацию через ребит таблицы пользователей о новой длинне треков пользователя и о количестве его треков.
Для хранения точек используется контейнер dotsdb и для быстрого доступа и поиска redis. Так же используется rabbitmq для получения новых пользователей и оповещения о новом треке. dots_consumer слушает ребит и добавляет пользователя. 
Модели пользователей разные, благодаря JWT айди пользователя можно получить из запроса но для джанго ОРМ удобнее делать связь с таблицей чем просто айди.


# Установка
```
docker-compose up
```
дождаться создания БД
```
./install.sh
```
Если все ОК то запуск займет около 5 минут, за это время будут созданы тестовые пользователи
user0, user1, user2 (пароль совпадает с логином)
Также сгенерированы 500000 точек с рандомными именами. И размещены в редисе. 
После этого можно проверять АПИ запросы.

Пример запросов в коллекции [Postman](https://github.com/Svyat33/alarstudios/blob/master/api_examples.postman_collection.json)