# Добавление новой категории

Позволяет добавить новую категорию

***URL*** : `/library/category`

***Method*** : `POST`

***Auth required*** : YES

***Permission required*** : None

## Success Responses

    HTTP 201 Created
    Allow: GET, POST, HEAD, OPTIONS
    Content-Type: application/json
    Vary: Accept
    
    {
        "id": 7,
        "category_name": "Рассказ"
    }