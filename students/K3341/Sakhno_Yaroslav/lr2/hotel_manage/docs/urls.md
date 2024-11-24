**Файл hotel/urls.py:**

```python
from django.urls import path
from . import views

urlpatterns = [
    path("all", views.hotel_list, name="hotel_list"),
    path("create_hotel/", views.create_hotel, name="create_hotel"),
    path("view_hotel/<int:pk>/", views.view_hotel, name="view_hotel"),
    path("create_room/<int:hotel_pk>/", views.create_room, name="create_room"),
    path("book_room/<int:hotel_pk>/", views.book_room, name="book_room"),
    path("reservation_success/", views.reservation_success, name="reservation_success"),
    path("room/<int:room_id>/add_review/", views.add_review, name="add_review"),
    path("room/<int:room_id>/room_reviews/", views.room_reviews, name="room_reviews"),
]
```

- `hotel_list` - отображает список всех отелей: `/hotels/all`
- `create_hotel` - создает новый отель: `/hotels/create_hotel/`
- `view_hotel` - отображает информацию о конкретном отеле с идентификатором `<int:pk>`: `/hotels/view_hotel/<int:pk>/`
- `create_room` - создает новую комнату в отеле с идентификатором `<int:hotel_pk>`: `/hotels/create_room/<int:hotel_pk>/`
- `book_room` - бронирует комнату в отеле с идентификатором `<int:hotel_pk>`: `/hotels/book_room/<int:hotel_pk>/`
- `reservation_success` - отображает страницу успешного бронирования: `/hotels/reservation_success/`
- `add_review` - добавляет отзыв к комнате с идентификатором `<int:room_id>`: `/hotels/room/<int:room_id>/add_review/`
- `room_reviews` - отображает список отзывов о комнате с идентификатором `<int:room_id>`: `/hotels/room/<int:room_id>/room_reviews/`

**Файл urls.py:**

```python
from django.contrib import admin
from django.urls import path, include
from urls import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("hotels/", include("hotel.urls")),
    path("", views.home_view),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
]
```

- `admin` - панель администратора: `/admin/`
- `hotel` - подключает маршруты из файла `hotel/urls.py`: `/hotels/`
- `home_view` - отображает главную страницу: `/`
- `register` - регистрирует нового пользователя: `/register/`
- `login_view` - отображает страницу входа: `/login/`
- `logout_view` - выполняет выход из системы: `/logout/`