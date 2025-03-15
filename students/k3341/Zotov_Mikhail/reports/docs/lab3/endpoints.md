# API
Description

## Version: v2

### Terms of service
https://www.google.com/policies/terms/

**Contact information:**  
hardbeat34@gmail.com  

**License:** BSD License

### Security
**Basic**  

| basic | *Basic* |
| ----- | ------- |

**Schemes:** http

---
### /api/check-ins/

#### GET
##### Description

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ------ |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 |  | [ [ClientRoom](#clientroom) ] |

#### POST
##### Description

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ------ |
| data | body |  | Yes | [ClientRoom](#clientroom) |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 201 |  | [ClientRoom](#clientroom) |

### /api/check-ins/{id}/

#### GET
##### Description

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ------ |
| id | path | A unique integer value identifying this client room. | Yes | integer |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 |  | [ClientRoom](#clientroom) |

#### PUT
##### Description

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ------ |
| id | path | A unique integer value identifying this client room. | Yes | integer |
| data | body |  | Yes | [ClientRoom](#clientroom) |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 |  | [ClientRoom](#clientroom) |

#### PATCH
##### Description

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ------ |
| id | path | A unique integer value identifying this client room. | Yes | integer |
| data | body |  | Yes | [ClientRoom](#clientroom) |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 |  | [ClientRoom](#clientroom) |

#### DELETE
##### Description

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ------ |
| id | path | A unique integer value identifying this client room. | Yes | integer |

##### Responses

| Code | Description |
| ---- | ----------- |
| 204 |  |

### /api/clients/

#### GET
##### Description

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ------ |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 |  | [ [Client](#client) ] |

#### POST
##### Description

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ------ |
| data | body |  | Yes | [Client](#client) |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 201 |  | [Client](#client) |

### /api/clients/{id}/

#### GET
##### Description

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ------ |
| id | path | A unique integer value identifying this client. | Yes | integer |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 |  | [Client](#client) |

#### PUT
##### Description

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ------ |
| id | path | A unique integer value identifying this client. | Yes | integer |
| data | body |  | Yes | [Client](#client) |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 |  | [Client](#client) |

#### PATCH
##### Description

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ------ |
| id | path | A unique integer value identifying this client. | Yes | integer |
| data | body |  | Yes | [Client](#client) |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 |  | [Client](#client) |

#### DELETE
##### Description

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ------ |
| id | path | A unique integer value identifying this client. | Yes | integer |

##### Responses

| Code | Description |
| ---- | ----------- |
| 204 |  |

### /api/employees/

#### GET
##### Description

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ------ |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 |  | [ [Employee](#employee) ] |

#### POST
##### Description

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ------ |
| data | body |  | Yes | [Employee](#employee) |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 201 |  | [Employee](#employee) |

### /api/employees/{id}

#### GET
##### Description

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ------ |
| id | path | A unique integer value identifying this employee. | Yes | integer |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 |  | [Employee](#employee) |

#### PUT
##### Description

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ------ |
| id | path | A unique integer value identifying this employee. | Yes | integer |
| data | body |  | Yes | [Employee](#employee) |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 |  | [Employee](#employee) |

#### PATCH
##### Description

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ------ |
| id | path | A unique integer value identifying this employee. | Yes | integer |
| data | body |  | Yes | [Employee](#employee) |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 |  | [Employee](#employee) |

#### DELETE
##### Description

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ------ |
| id | path | A unique integer value identifying this employee. | Yes | integer |

##### Responses

| Code | Description |
| ---- | ----------- |
| 204 |  |

### /api/reports/

#### GET
##### Description

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ------ |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 |  |

### /api/rooms/

#### GET
##### Description

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ------ |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 |  | [ [Room](#room) ] |

---
### /auth/token/login/

#### POST
##### Description

Use this endpoint to obtain user authentication token.

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ------ |
| data | body |  | Yes | [TokenCreate](#tokencreate) |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 201 |  | [TokenCreate](#tokencreate) |

### /auth/token/logout/

#### POST
##### Description

Use this endpoint to logout user (remove user authentication token).

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ------ |

##### Responses

| Code | Description |
| ---- | ----------- |
| 201 |  |

### /auth/users/

#### GET
##### Description

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ------ |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 |  | [ [User](#user) ] |

#### POST
##### Description

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ------ |
| data | body |  | Yes | [UserCreate](#usercreate) |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 201 |  | [UserCreate](#usercreate) |

### /auth/users/activation/

#### POST
##### Description

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ------ |
| data | body |  | Yes | [Activation](#activation) |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 201 |  | [Activation](#activation) |

### /auth/users/me/

#### GET
##### Description

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ------ |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 |  | [ [User](#user) ] |

#### PUT
##### Description

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ------ |
| data | body |  | Yes | [User](#user) |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 |  | [User](#user) |

#### PATCH
##### Description

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ------ |
| data | body |  | Yes | [User](#user) |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 |  | [User](#user) |

#### DELETE
##### Description

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ------ |

##### Responses

| Code | Description |
| ---- | ----------- |
| 204 |  |

### /auth/users/resend_activation/

#### POST
##### Description

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ------ |
| data | body |  | Yes | [SendEmailReset](#sendemailreset) |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 201 |  | [SendEmailReset](#sendemailreset) |

### /auth/users/reset_password/

#### POST
##### Description

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ------ |
| data | body |  | Yes | [SendEmailReset](#sendemailreset) |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 201 |  | [SendEmailReset](#sendemailreset) |

### /auth/users/reset_password_confirm/

#### POST
##### Description

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ------ |
| data | body |  | Yes | [PasswordResetConfirm](#passwordresetconfirm) |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 201 |  | [PasswordResetConfirm](#passwordresetconfirm) |

### /auth/users/reset_username/

#### POST
##### Description

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ------ |
| data | body |  | Yes | [SendEmailReset](#sendemailreset) |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 201 |  | [SendEmailReset](#sendemailreset) |

### /auth/users/reset_username_confirm/

#### POST
##### Description

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ------ |
| data | body |  | Yes | [UsernameResetConfirm](#usernameresetconfirm) |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 201 |  | [UsernameResetConfirm](#usernameresetconfirm) |

### /auth/users/set_password/

#### POST
##### Description

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ------ |
| data | body |  | Yes | [SetPassword](#setpassword) |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 201 |  | [SetPassword](#setpassword) |

### /auth/users/set_username/

#### POST
##### Description

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ------ |
| data | body |  | Yes | [SetUsername](#setusername) |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 201 |  | [SetUsername](#setusername) |

### /auth/users/{id}/

#### GET
##### Description

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ------ |
| id | path | A unique integer value identifying this user. | Yes | integer |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 |  | [User](#user) |

#### PUT
##### Description

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ------ |
| id | path | A unique integer value identifying this user. | Yes | integer |
| data | body |  | Yes | [User](#user) |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 |  | [User](#user) |

#### PATCH
##### Description

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ------ |
| id | path | A unique integer value identifying this user. | Yes | integer |
| data | body |  | Yes | [User](#user) |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 |  | [User](#user) |

#### DELETE
##### Description

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ------ |
| id | path | A unique integer value identifying this user. | Yes | integer |

##### Responses

| Code | Description |
| ---- | ----------- |
| 204 |  |

---
### Models

#### Client

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| id | integer |  | No |
| passport_number | string |  | Yes |
| last_name | string |  | Yes |
| first_name | string |  | Yes |
| city | string |  | Yes |

#### ClientRoom

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| id | integer |  | No |
| client | [Client](#client) |  | Yes |
| room | integer |  | Yes |
| check_in_date | date |  | No |
| check_out_date | date |  | No |
| count_of_clients | integer |  | No |

#### FloorSchedule

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| floor | integer |  | Yes |
| day_of_week | string | *Enum:* `"Monday"`, `"Tuesday"`, `"Wednesday"`, `"Thursday"`, `"Friday"`, `"Saturday"`, `"Sunday"` | Yes |

#### CleaningAssignment

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| floor_schedule | [FloorSchedule](#floorschedule) |  | Yes |

#### Employee

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| id | integer |  | No |
| last_name | string |  | Yes |
| first_name | string |  | Yes |
| cleaning_assignments | [ [CleaningAssignment](#cleaningassignment) ] |  | Yes |

#### Floor

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| id | integer |  | No |
| number | integer |  | Yes |

#### Room

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| id | integer |  | No |
| floor | [Floor](#floor) |  | Yes |
| number | integer |  | Yes |
| room_type | string | *Enum:* `"single"`, `"double"`, `"triple"` | Yes |
| price_per_day | integer |  | No |
| phone | string |  | Yes |

#### TokenCreate

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| password | string |  | No |
| username | string |  | No |

#### User

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| email | string (email) |  | No |
| id | integer |  | No |
| username | string | Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only. | No |

#### UserCreate

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| email | string (email) |  | No |
| username | string | Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only. | Yes |
| id | integer |  | No |
| password | string |  | Yes |

#### Activation

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| uid | string |  | Yes |
| token | string |  | Yes |

#### SendEmailReset

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| email | string (email) |  | Yes |

#### PasswordResetConfirm

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| uid | string |  | Yes |
| token | string |  | Yes |
| new_password | string |  | Yes |

#### UsernameResetConfirm

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| new_username | string | Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only. | Yes |

#### SetPassword

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| new_password | string |  | Yes |
| current_password | string |  | Yes |

#### SetUsername

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| current_password | string |  | Yes |
| new_username | string | Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only. | Yes |
