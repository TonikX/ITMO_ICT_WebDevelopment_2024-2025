# Описание маршрутов

- **`path('', RaceListView.as_view(), name='race_list')`**  
  **Описание**: Основная страница приложения, отображающая список всех гонок.  
  **Представление**: `RaceListView`  
  **Имя маршрута**: `race_list`

- **`path('register/', UserRegistrationView.as_view(), name='register')`**  
  **Описание**: Страница для регистрации новых пользователей.  
  **Представление**: `UserRegistrationView`  
  **Имя маршрута**: `register`

- **`path('race/<int:pk>/', RaceDetailView.as_view(), name='race_detail')`**  
  **Описание**: Детали конкретной гонки, включая список зарегистрированных участников и результаты.  
  **Представление**: `RaceDetailView`  
  **Имя маршрута**: `race_detail`

- **`path('race/<int:race_id>/register', RaceRegistrationView.as_view(), name='register_race')`**  
  **Описание**: Регистрация гонщика на гонку.  
  **Представление**: `RaceRegistrationView`  
  **Имя маршрута**: `register_race`

- **`path('race/<int:race_id>/unregister', RaceUnregisterView.as_view(), name='unregister_race')`**  
  **Описание**: Отмена регистрации на гонку для текущего пользователя.  
  **Представление**: `RaceUnregisterView`  
  **Имя маршрута**: `unregister_race`

- **`path('race/<int:race_id>/comment', CommentCreateView.as_view(), name='add_comment')`**  
  **Описание**: Добавление комментария к гонке.  
  **Представление**: `CommentCreateView`  
  **Имя маршрута**: `add_comment`

- **`path('accounts/logout/', LogoutUser.as_view(), name='logout')`**  
  **Описание**: Выход из учетной записи пользователя.  
  **Представление**: `LogoutUser`  
  **Имя маршрута**: `logout`

- **`path('create_racer_profile/', RacerProfileCreateView.as_view(), name='create_racer_profile')`**  
  **Описание**: Создание профиля гонщика для зарегистрированных пользователей.  
  **Представление**: `RacerProfileCreateView`  
  **Имя маршрута**: `create_racer_profile`

- **`path('profile/<int:pk>/', RacerProfileView.as_view(), name='racer_profile')`**  
  **Описание**: Отображение профиля гонщика.  
  **Представление**: `RacerProfileView`  
  **Имя маршрута**: `racer_profile`

- **`path('profile/<int:pk>/edit/', RacerProfileUpdateView.as_view(), name='edit_racer_profile')`**  
  **Описание**: Редактирование профиля гонщика.  
  **Представление**: `RacerProfileUpdateView`  
  **Имя маршрута**: `edit_racer_profile`

- **`path('race/<int:pk>/edit/', EditRaceView.as_view(), name='edit_race')`**  
  **Описание**: Редактирование данных гонки (только для администраторов).  
  **Представление**: `EditRaceView`  
  **Имя маршрута**: `edit_race`

- **`path('race/<int:pk>/delete/', DeleteRaceView.as_view(), name='delete_race')`**  
  **Описание**: Удаление гонки (только для администраторов).  
  **Представление**: `DeleteRaceView`  
  **Имя маршрута**: `delete_race`

- **`path('comment/<int:pk>/delete', DeleteCommentView.as_view(), name='delete_comment')`**  
  **Описание**: Удаление комментария (доступно только администраторам).  
  **Представление**: `DeleteCommentView`  
  **Имя маршрута**: `delete_comment`
