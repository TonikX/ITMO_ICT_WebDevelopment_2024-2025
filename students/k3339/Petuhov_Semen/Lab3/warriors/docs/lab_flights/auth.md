# Аутентификация
Для аутентификации нужно сделать несколько действийЖ
1) Создать пользователя по ссылке http://localhost:8000/auth/token/login/
![html страница](images/user_create.PNG)
2) Получить токен
http://localhost:8000/auth/token/login/
![html страница](images/get_token.PNG)
3) Ввести этот токен в тело запроса, можно для этого использовать postman
![html страница](images/token_postman.PNG)
4) Получить текущего пользователя можно по ссылке(http://localhost:8000/auth/current-user/)
![html страница](images/get_user.PNG)