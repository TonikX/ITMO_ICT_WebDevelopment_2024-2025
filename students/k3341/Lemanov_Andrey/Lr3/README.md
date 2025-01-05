# Документация API Peer-Review

## Версия API: 0.1.0

### Эндпоинт проверки состояния

#### `GET /api/v1/healthz`
- **Описание:** Проверка состояния
- **ID операции:** `healthcheck_api_v1_healthz_get`
- **Ответ:**
  - `200 OK`: 
    - **Описание:** Успешный ответ
    - **Схема:** 
      ```json
      {
        "type": "object",
        "title": "Ответ проверки состояния API V1 Healthz Get",
        "additionalProperties": {
          "type": "string"
        }
      }
      ```

---

## Эндпоинты для заданий

### `POST /api/v1/create_assignment`
- **Описание:** Создать задание
- **ID операции:** `create_assignment_api_v1_create_assignment_post`
- **Тело запроса:** 
  - **Тип контента:** `application/json`
  - **Ссылка на схему:** `#/components/schemas/RequestCreateAssignment`
- **Ответы:**
  - `200 OK`:
    - **Описание:** Успешный ответ
    - **Ссылка на схему:** `#/components/schemas/ResponseCreateAssignment`
  - `422 Unprocessable Entity`:
    - **Описание:** Ошибка валидации
    - **Ссылка на схему:** `#/components/schemas/HTTPValidationError`

---

### `GET /api/v1/get_assignment/{assignment_id}`
- **Описание:** Получить задание
- **ID операции:** `get_assignment_api_v1_get_assignment__assignment_id__get`
- **Параметры:**
  - **assignment_id** (параметр пути, обязательный, тип: `integer`)
- **Ответы:**
  - `200 OK`:
    - **Описание:** Успешный ответ
    - **Ссылка на схему:** `#/components/schemas/ResponseAssignment`
  - `422 Unprocessable Entity`:
    - **Описание:** Ошибка валидации
    - **Ссылка на схему:** `#/components/schemas/HTTPValidationError`

---

### `GET /api/v1/get_all_assignments`
- **Описание:** Получить все задания
- **ID операции:** `get_all_assignments_api_v1_get_all_assignments_get`
- **Ответы:**
  - `200 OK`:
    - **Описание:** Успешный ответ
    - **Ссылка на схему:** `#/components/schemas/ResponseAllAssignments`

---

### `PUT /api/v1/update_assignment`
- **Описание:** Обновить задание
- **ID операции:** `update_assignment_api_v1_update_assignment_put`
- **Тело запроса:** 
  - **Тип контента:** `application/json`
  - **Ссылка на схему:** `#/components/schemas/RequestUpdateAssignment`
- **Ответы:**
  - `200 OK`:
    - **Описание:** Успешный ответ
    - **Ссылка на схему:** `#/components/schemas/ResponseAssignment`
  - `422 Unprocessable Entity`:
    - **Описание:** Ошибка валидации
    - **Ссылка на схему:** `#/components/schemas/HTTPValidationError`

---

### `DELETE /api/v1/delete_assignment/{assignment_id}`
- **Описание:** Удалить задание
- **ID операции:** `delete_assignment_api_v1_delete_assignment__assignment_id__delete`
- **Параметры:**
  - **assignment_id** (параметр пути, обязательный, тип: `integer`)
- **Ответы:**
  - `200 OK`:
    - **Описание:** Успешный ответ
    - **Ссылка на схему:** `#/components/schemas/ResponseAssignment`
  - `422 Unprocessable Entity`:
    - **Описание:** Ошибка валидации
    - **Ссылка на схему:** `#/components/schemas/HTTPValidationError`

---

## Эндпоинты для оценок

### `POST /api/v1/create_grade`
- **Описание:** Создать оценку
- **ID операции:** `create_grade_api_v1_create_grade_post`
- **Тело запроса:** 
  - **Тип контента:** `application/json`
  - **Ссылка на схему:** `#/components/schemas/RequestCreateGrade`
- **Ответы:**
  - `200 OK`:
    - **Описание:** Успешный ответ
    - **Ссылка на схему:** `#/components/schemas/ResponseCreateGrade`
  - `422 Unprocessable Entity`:
    - **Описание:** Ошибка валидации
    - **Ссылка на схему:** `#/components/schemas/HTTPValidationError`

---

### `GET /api/v1/get_grade/{grade_id}`
- **Описание:** Получить оценку
- **ID операции:** `get_grade_api_v1_get_grade__grade_id__get`
- **Параметры:**
  - **grade_id** (параметр пути, обязательный, тип: `integer`)
- **Ответы:**
  - `200 OK`:
    - **Описание:** Успешный ответ
    - **Ссылка на схему:** `#/components/schemas/ResponseGradeWithRelationships`
  - `422 Unprocessable Entity`:
    - **Описание:** Ошибка валидации
    - **Ссылка на схему:** `#/components/schemas/HTTPValidationError`

---

### `GET /api/v1/get_grades/student/{student_id}`
- **Описание:** Получить оценки для студента
- **ID операции:** `get_grades_for_student_api_v1_get_grades_student__student_id__get`
- **Параметры:**
  - **student_id** (параметр пути, обязательный, тип: `integer`)
- **Ответы:**
  - `200 OK`:
    - **Описание:** Успешный ответ
    - **Ссылка на схему:** `#/components/schemas/ResponseAllGradesOfStudent`
  - `422 Unprocessable Entity`:
    - **Описание:** Ошибка валидации
    - **Ссылка на схему:** `#/components/schemas/HTTPValidationError`

---

### `GET /api/v1/get_grades/submission/{submission_id}`
- **Описание:** Получить оценки для работы
- **ID операции:** `get_grades_for_submission_api_v1_get_grades_submission__submission_id__get`
- **Параметры:**
  - **submission_id** (параметр пути, обязательный, тип: `integer`)
- **Ответы:**
  - `200 OK`:
    - **Описание:** Успешный ответ
    - **Ссылка на схему:** `#/components/schemas/ResponseAllGradesOfSubmission`
  - `422 Unprocessable Entity`:
    - **Описание:** Ошибка валидации
    - **Ссылка на схему:** `#/components/schemas/HTTPValidationError`

---

### `POST /api/v1/create_grading_criteria`
- **Описание:** Создать критерии оценки
- **ID операции:** `create_grade_api_v1_create_grading_criteria_post`
- **Тело запроса:** 
  - **Тип контента:** `application/json`
  - **Ссылка на схему:** `#/components/schemas/RequestCreateGradingCriteria`
- **Ответы:**
  - `200 OK`:
    - **Описание:** Успешный ответ
    - **Ссылка на схему:** `#/components/schemas/ResponseCreateGradingCriteria`
  - `422 Unprocessable Entity`:
    - **Описание:** Ошибка валидации
    - **Ссылка на схему:** `#/components/schemas/HTTPValidationError`

---

### `GET /api/v1/get_grading_criteria/{submission_id}`
- **Описание:** Получить критерии оценки
- **ID операции:** `get_grading_criteria_api_v1_get_grading_criteria__submission_id__get`
- **Параметры:**
  - **submission_id** (параметр пути, обязательный, тип: `integer`)
- **Ответы:**
  - `200 OK`:
    - **Описание:** Успешный ответ
    - **Ссылка на схему:** `#/components/schemas/ResponseGradingCriteria`
  - `422 Unprocessable Entity`:
    - **Описание:** Ошибка валидации
    - **Ссылка на схему:** `#/components/schemas/HTTPValidationError`

---

## Эндпоинты для отправок

### `POST /api/v1/create_submission`
- **Описание:** Создать отправку
- **ID операции:** `create_submission_api_v1_create_submission_post`
- **Тело запроса:** 
  - **Тип контента:** `application/json`
  - **Ссылка на схему:** `#/components/schemas/RequestCreateSubmission`
- **Ответы:**
  - `200 OK`:
    - **Описание:** Успешный ответ
  - `422 Unprocessable Entity`:
    - **Описание:** Ошибка валидации
    - **Ссылка на схему:** `#/components/schemas/HTTPValidationError`

---

### `GET /api/v1/get_submission/{submission_id}`
- **Описание:** Получить отправку
- **ID операции:** `get_submission_api_v1_get_submission__submission_id__get`
- **П
