# Администрирование отеля (Django Rest Framework)

---

## **Описание основных endpoint-ов**

Получить информацию о всех комнатах отеля с возможностью добавления новой 

`GET, POST /hotel/rooms/`

![img_4.png](lab_imgs/img_4.png)

Получить информацию об одной комнате с возможностью изменения и удаления объекта 

`GET, PATCH, DELETE /hotel/rooms/<room_id>/`

![img_5.png](lab_imgs/img_5.png)

Получить информацию о всех клиентах отеля с возможностью добавления нового 

`GET, POST /hotel/clients/`

![img.png](lab_imgs/img.png)

Получить информацию об одном клиенте с возможностью изменения и удаления объекта 

`GET, PATCH, DELETE /hotel/clients/<client_id>/`

![img_1.png](lab_imgs/img_1.png)

Получить информацию о всех работниках отеля с возможностью добавления нового 

`GET, POST /hotel/employees/`

![img_2.png](lab_imgs/img_2.png)

Получить информацию об одном работнике с возможностью изменения и удаления объекта 

`GET, PATCH, DELETE /hotel/employees/<employee_id>/`

![img_3.png](lab_imgs/img_3.png)

Получить информацию о всех бронированиях в отеле с возможностью добавления нового 

`GET, POST /hotel/bookings/`

![img_6.png](lab_imgs/img_6.png)

Получить информацию об одном бронировании с возможностью изменения и удаления объекта 

`GET, PATCH, DELETE /hotel/bookings/<booking_id>/`

![img_7.png](lab_imgs/img_7.png)

Получить информацию о всех уборках комнат с возможностью добавления нового 

`GET, POST /hotel/cleanings/`

![img_8.png](lab_imgs/img_8.png)

Получить информацию об одной уборки комнат с возможностью изменения и удаления объекта 

`GET, PATCH, DELETE /hotel/cleanings/<cleaning_id>/`

![img_9.png](lab_imgs/img_9.png)

## **Описание дополнительных endpoint-ов**

Получение информации:

- о клиентах, проживавших в заданном номере, в заданный период времени

`GET /hotel/clients-in-room/<room_id>/<start_date>/<end_date>/`

![img_10.png](lab_imgs/img_10.png)

- о количестве клиентов, прибывших из заданного города

`GET /hotel/clients-from-city/<origin_city>/`

![img_11.png](lab_imgs/img_11.png)

- о том, кто из служащих убирал номер указанного клиента в заданный день недели

`GET /hotel/cleaning-employees/<client_id>/<week_day>/`

![img_12.png](lab_imgs/img_12.png)

- о количестве в гостинице свободных номеров

`GET /hotel/free-rooms/<start_date>/<end_date>/`

![img_13.png](lab_imgs/img_13.png)

- о списке клиентов с указанием места жительства, которые проживали в те же дни,
что и заданный клиент

`GET /hotel/clients-while-client/<request_client_id>/`

![img_14.png](lab_imgs/img_14.png)


### Выдача отчёта за запрашиваемый квартал

Отчёт содержит следующие данные:

- число клиентов за указанный период в каждом номере;
- количество номеров на каждом этаже;
- общая сумма дохода за каждый номер;
- суммарный доход по всей гостинице.

`GET /hotel/report/<requested_quarter>/`

![img_15.png](lab_imgs/img_15.png)
![img_16.png](lab_imgs/img_16.png)


## Добавление Djoser в проект

Регистрация нового пользователя
`POST http://127.0.0.1:8000/auth/users/`

![img_17.png](lab_imgs/img_17.png)

Авторизация пользователя -> получение токена
`POST http://127.0.0.1:8000/auth/token/login/`

![img_18.png](lab_imgs/img_18.png)

Запрос информации о пользователе с использованием личного токена
`GET http://127.0.0.1:8000/auth/users/me/`

![img_19.png](lab_imgs/img_19.png)