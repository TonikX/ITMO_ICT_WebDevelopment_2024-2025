## API Эндпоинты

---
title: API v0.0.0
language_tabs:
  - shell: Shell
  - http: HTTP
  - javascript: JavaScript
  - ruby: Ruby
  - python: Python
  - php: PHP
  - java: Java
  - go: Go
toc_footers: []
includes: []
search: true
highlight_theme: darkula
headingLevel: 2

---

<!-- Generator: Widdershins v4.0.1 -->

<h1 id="api"> v0.0.0</h1>

> Scroll down for code samples, example requests and responses. Select a language for code samples from the tabs above or the mobile navigation menu.

# Authentication

* API Key (cookieAuth)
    - Parameter Name: **sessionid**, in: cookie. 

* API Key (tokenAuth)
    - Parameter Name: **Authorization**, in: header. Token-based authentication with required prefix "Token"

<h1 id="api-api">api</h1>

## api_schema_retrieve

<a id="opIdapi_schema_retrieve"></a>

`GET /api/schema/`

OpenApi3 schema for this API. Format can be selected via content negotiation.

- YAML: application/vnd.oai.openapi
- JSON: application/vnd.oai.openapi+json

<h3 id="api_schema_retrieve-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|format|query|string|false|none|
|lang|query|string|false|none|

#### Enumerated Values

|Parameter|Value|
|---|---|
|format|json|
|format|yaml|
|lang|af|
|lang|ar|
|lang|ar-dz|
|lang|ast|
|lang|az|
|lang|be|
|lang|bg|
|lang|bn|
|lang|br|
|lang|bs|
|lang|ca|
|lang|ckb|
|lang|cs|
|lang|cy|
|lang|da|
|lang|de|
|lang|dsb|
|lang|el|
|lang|en|
|lang|en-au|
|lang|en-gb|
|lang|eo|
|lang|es|
|lang|es-ar|
|lang|es-co|
|lang|es-mx|
|lang|es-ni|
|lang|es-ve|
|lang|et|
|lang|eu|
|lang|fa|
|lang|fi|
|lang|fr|
|lang|fy|
|lang|ga|
|lang|gd|
|lang|gl|
|lang|he|
|lang|hi|
|lang|hr|
|lang|hsb|
|lang|hu|
|lang|hy|
|lang|ia|
|lang|id|
|lang|ig|
|lang|io|
|lang|is|
|lang|it|
|lang|ja|
|lang|ka|
|lang|kab|
|lang|kk|
|lang|km|
|lang|kn|
|lang|ko|
|lang|ky|
|lang|lb|
|lang|lt|
|lang|lv|
|lang|mk|
|lang|ml|
|lang|mn|
|lang|mr|
|lang|ms|
|lang|my|
|lang|nb|
|lang|ne|
|lang|nl|
|lang|nn|
|lang|os|
|lang|pa|
|lang|pl|
|lang|pt|
|lang|pt-br|
|lang|ro|
|lang|ru|
|lang|sk|
|lang|sl|
|lang|sq|
|lang|sr|
|lang|sr-latn|
|lang|sv|
|lang|sw|
|lang|ta|
|lang|te|
|lang|tg|
|lang|th|
|lang|tk|
|lang|tr|
|lang|tt|
|lang|udm|
|lang|ug|
|lang|uk|
|lang|ur|
|lang|uz|
|lang|vi|
|lang|zh-hans|
|lang|zh-hant|

> Example responses

> 200 Response

```json
{
  "property1": null,
  "property2": null
}
```

<h3 id="api_schema_retrieve-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

<h3 id="api_schema_retrieve-responseschema">Response Schema</h3>

Status Code **200**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» **additionalProperties**|any|false|none|none|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth, tokenAuth, None
</aside>

<h1 id="api-ascents">ascents</h1>

## ascents_list

<a id="opIdascents_list"></a>

`GET /ascents/`

<h3 id="ascents_list-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|ordering|query|string|false|Which field to use when ordering the results.|
|route|query|integer|false|none|
|route__mountain|query|integer|false|none|

> Example responses

> 200 Response

```json
[
  {
    "id": 0,
    "route": {
      "id": 0,
      "name": "string",
      "description": "string",
      "duration_days": 32767,
      "mountain": 0
    },
    "mountain": {
      "id": 0,
      "name": "string",
      "elevation": 32767,
      "region": "string",
      "country": 0
    },
    "participants": [
      {
        "id": 0,
        "user": "string",
        "is_successful": true,
        "incident_type": "INJ",
        "incident_details": "string",
        "ascent": 0
      }
    ],
    "planned_start_datetime": "2019-08-24T14:15:22Z",
    "planned_end_datetime": "2019-08-24T14:15:22Z",
    "actual_start_datetime": "2019-08-24T14:15:22Z",
    "actual_end_datetime": "2019-08-24T14:15:22Z",
    "is_successful": true,
    "summary": "string"
  }
]
```

<h3 id="ascents_list-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

<h3 id="ascents_list-responseschema">Response Schema</h3>

Status Code **200**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|*anonymous*|[[AscentDetail](#schemaascentdetail)]|false|none|none|
|» id|integer|true|read-only|none|
|» route|[Route](#schemaroute)|true|read-only|none|
|»» id|integer|true|read-only|none|
|»» name|string|true|none|none|
|»» description|string¦null|false|none|none|
|»» duration_days|integer¦null|false|none|none|
|»» mountain|integer¦null|false|none|none|
|» mountain|[Mountain](#schemamountain)|true|read-only|none|
|»» id|integer|true|read-only|none|
|»» name|string|true|none|none|
|»» elevation|integer|true|none|none|
|»» region|string¦null|false|none|none|
|»» country|integer|true|none|none|
|» participants|[[AscentParticipation](#schemaascentparticipation)]|true|read-only|none|
|»» id|integer|true|read-only|none|
|»» user|string|true|read-only|none|
|»» is_successful|boolean|false|none|none|
|»» incident_type|any|false|none|none|

*oneOf*

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|»»» *anonymous*|[IncidentTypeEnum](#schemaincidenttypeenum)|false|none|* `INJ` - Injured<br>* `MIS` - Missing<br>* `FAT` - Fatality|

*xor*

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|»»» *anonymous*|string|false|none|none|

*xor*

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|»»» *anonymous*|object|false|none|none|

*continued*

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|»» incident_details|string¦null|false|none|none|
|»» ascent|integer|true|read-only|none|
|» planned_start_datetime|string(date-time)|true|none|none|
|» planned_end_datetime|string(date-time)|true|none|none|
|» actual_start_datetime|string(date-time)¦null|false|none|none|
|» actual_end_datetime|string(date-time)¦null|false|none|none|
|» is_successful|boolean|false|none|none|
|» summary|string¦null|false|none|none|

#### Enumerated Values

|Property|Value|
|---|---|
|*anonymous*|INJ|
|*anonymous*|MIS|
|*anonymous*|FAT|
|*anonymous*||
|*anonymous*|null|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth, tokenAuth, None
</aside>

## ascents_create

<a id="opIdascents_create"></a>

`POST /ascents/`

> Body parameter

```json
{
  "planned_start_datetime": "2019-08-24T14:15:22Z",
  "planned_end_datetime": "2019-08-24T14:15:22Z",
  "actual_start_datetime": "2019-08-24T14:15:22Z",
  "actual_end_datetime": "2019-08-24T14:15:22Z",
  "is_successful": true,
  "summary": "string",
  "route": 0
}
```

```yaml
planned_start_datetime: 2019-08-24T14:15:22Z
planned_end_datetime: 2019-08-24T14:15:22Z
actual_start_datetime: 2019-08-24T14:15:22Z
actual_end_datetime: 2019-08-24T14:15:22Z
is_successful: true
summary: string
route: 0

```

<h3 id="ascents_create-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[Ascent](#schemaascent)|true|none|

> Example responses

> 201 Response

```json
{
  "id": 0,
  "planned_start_datetime": "2019-08-24T14:15:22Z",
  "planned_end_datetime": "2019-08-24T14:15:22Z",
  "actual_start_datetime": "2019-08-24T14:15:22Z",
  "actual_end_datetime": "2019-08-24T14:15:22Z",
  "is_successful": true,
  "summary": "string",
  "route": 0
}
```

<h3 id="ascents_create-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|201|[Created](https://tools.ietf.org/html/rfc7231#section-6.3.2)|none|[Ascent](#schemaascent)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth, tokenAuth
</aside>

## ascents_participants_retrieve

<a id="opIdascents_participants_retrieve"></a>

`GET /ascents/{ascent_pk}/participants/{ascentparticipation_pk}/`

<h3 id="ascents_participants_retrieve-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|ascent_pk|path|integer|true|none|
|ascentparticipation_pk|path|integer|true|none|

> Example responses

> 200 Response

```json
{
  "id": 0,
  "user": "string",
  "is_successful": true,
  "incident_type": "INJ",
  "incident_details": "string",
  "ascent": 0
}
```

<h3 id="ascents_participants_retrieve-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[AscentParticipation](#schemaascentparticipation)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth, tokenAuth
</aside>

## ascents_participants_update

<a id="opIdascents_participants_update"></a>

`PUT /ascents/{ascent_pk}/participants/{ascentparticipation_pk}/`

> Body parameter

```json
{
  "is_successful": true,
  "incident_type": "INJ",
  "incident_details": "string"
}
```

```yaml
is_successful: true
incident_type: INJ
incident_details: string

```

<h3 id="ascents_participants_update-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|ascent_pk|path|integer|true|none|
|ascentparticipation_pk|path|integer|true|none|
|body|body|[AscentParticipation](#schemaascentparticipation)|false|none|

> Example responses

> 200 Response

```json
{
  "id": 0,
  "user": "string",
  "is_successful": true,
  "incident_type": "INJ",
  "incident_details": "string",
  "ascent": 0
}
```

<h3 id="ascents_participants_update-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[AscentParticipation](#schemaascentparticipation)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth, tokenAuth
</aside>

## ascents_participants_partial_update

<a id="opIdascents_participants_partial_update"></a>

`PATCH /ascents/{ascent_pk}/participants/{ascentparticipation_pk}/`

> Body parameter

```json
{
  "is_successful": true,
  "incident_type": "INJ",
  "incident_details": "string"
}
```

```yaml
is_successful: true
incident_type: INJ
incident_details: string

```

<h3 id="ascents_participants_partial_update-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|ascent_pk|path|integer|true|none|
|ascentparticipation_pk|path|integer|true|none|
|body|body|[PatchedAscentParticipation](#schemapatchedascentparticipation)|false|none|

> Example responses

> 200 Response

```json
{
  "id": 0,
  "user": "string",
  "is_successful": true,
  "incident_type": "INJ",
  "incident_details": "string",
  "ascent": 0
}
```

<h3 id="ascents_participants_partial_update-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[AscentParticipation](#schemaascentparticipation)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth, tokenAuth
</aside>

## ascents_participants_destroy

<a id="opIdascents_participants_destroy"></a>

`DELETE /ascents/{ascent_pk}/participants/{ascentparticipation_pk}/`

<h3 id="ascents_participants_destroy-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|ascent_pk|path|integer|true|none|
|ascentparticipation_pk|path|integer|true|none|

<h3 id="ascents_participants_destroy-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|204|[No Content](https://tools.ietf.org/html/rfc7231#section-6.3.5)|No response body|None|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth, tokenAuth
</aside>

## ascents_retrieve

<a id="opIdascents_retrieve"></a>

`GET /ascents/{id}/`

<h3 id="ascents_retrieve-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|id|path|integer|true|none|

> Example responses

> 200 Response

```json
{
  "id": 0,
  "route": {
    "id": 0,
    "name": "string",
    "description": "string",
    "duration_days": 32767,
    "mountain": 0
  },
  "mountain": {
    "id": 0,
    "name": "string",
    "elevation": 32767,
    "region": "string",
    "country": 0
  },
  "participants": [
    {
      "id": 0,
      "user": "string",
      "is_successful": true,
      "incident_type": "INJ",
      "incident_details": "string",
      "ascent": 0
    }
  ],
  "planned_start_datetime": "2019-08-24T14:15:22Z",
  "planned_end_datetime": "2019-08-24T14:15:22Z",
  "actual_start_datetime": "2019-08-24T14:15:22Z",
  "actual_end_datetime": "2019-08-24T14:15:22Z",
  "is_successful": true,
  "summary": "string"
}
```

<h3 id="ascents_retrieve-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[AscentDetail](#schemaascentdetail)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth, tokenAuth, None
</aside>

## ascents_update

<a id="opIdascents_update"></a>

`PUT /ascents/{id}/`

> Body parameter

```json
{
  "planned_start_datetime": "2019-08-24T14:15:22Z",
  "planned_end_datetime": "2019-08-24T14:15:22Z",
  "actual_start_datetime": "2019-08-24T14:15:22Z",
  "actual_end_datetime": "2019-08-24T14:15:22Z",
  "is_successful": true,
  "summary": "string",
  "route": 0
}
```

```yaml
planned_start_datetime: 2019-08-24T14:15:22Z
planned_end_datetime: 2019-08-24T14:15:22Z
actual_start_datetime: 2019-08-24T14:15:22Z
actual_end_datetime: 2019-08-24T14:15:22Z
is_successful: true
summary: string
route: 0

```

<h3 id="ascents_update-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|id|path|integer|true|none|
|body|body|[Ascent](#schemaascent)|true|none|

> Example responses

> 200 Response

```json
{
  "id": 0,
  "planned_start_datetime": "2019-08-24T14:15:22Z",
  "planned_end_datetime": "2019-08-24T14:15:22Z",
  "actual_start_datetime": "2019-08-24T14:15:22Z",
  "actual_end_datetime": "2019-08-24T14:15:22Z",
  "is_successful": true,
  "summary": "string",
  "route": 0
}
```

<h3 id="ascents_update-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[Ascent](#schemaascent)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth, tokenAuth
</aside>

## ascents_partial_update

<a id="opIdascents_partial_update"></a>

`PATCH /ascents/{id}/`

> Body parameter

```json
{
  "planned_start_datetime": "2019-08-24T14:15:22Z",
  "planned_end_datetime": "2019-08-24T14:15:22Z",
  "actual_start_datetime": "2019-08-24T14:15:22Z",
  "actual_end_datetime": "2019-08-24T14:15:22Z",
  "is_successful": true,
  "summary": "string",
  "route": 0
}
```

```yaml
planned_start_datetime: 2019-08-24T14:15:22Z
planned_end_datetime: 2019-08-24T14:15:22Z
actual_start_datetime: 2019-08-24T14:15:22Z
actual_end_datetime: 2019-08-24T14:15:22Z
is_successful: true
summary: string
route: 0

```

<h3 id="ascents_partial_update-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|id|path|integer|true|none|
|body|body|[PatchedAscent](#schemapatchedascent)|false|none|

> Example responses

> 200 Response

```json
{
  "id": 0,
  "planned_start_datetime": "2019-08-24T14:15:22Z",
  "planned_end_datetime": "2019-08-24T14:15:22Z",
  "actual_start_datetime": "2019-08-24T14:15:22Z",
  "actual_end_datetime": "2019-08-24T14:15:22Z",
  "is_successful": true,
  "summary": "string",
  "route": 0
}
```

<h3 id="ascents_partial_update-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[Ascent](#schemaascent)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth, tokenAuth
</aside>

## ascents_destroy

<a id="opIdascents_destroy"></a>

`DELETE /ascents/{id}/`

<h3 id="ascents_destroy-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|id|path|integer|true|none|

<h3 id="ascents_destroy-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|204|[No Content](https://tools.ietf.org/html/rfc7231#section-6.3.5)|No response body|None|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth, tokenAuth
</aside>

## ascents_participants_list

<a id="opIdascents_participants_list"></a>

`GET /ascents/{id}/participants/`

<h3 id="ascents_participants_list-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|id|path|integer|true|none|

> Example responses

> 200 Response

```json
[
  {
    "id": 0,
    "user": "string",
    "is_successful": true,
    "incident_type": "INJ",
    "incident_details": "string",
    "ascent": 0
  }
]
```

<h3 id="ascents_participants_list-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

<h3 id="ascents_participants_list-responseschema">Response Schema</h3>

Status Code **200**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|*anonymous*|[[AscentParticipation](#schemaascentparticipation)]|false|none|none|
|» id|integer|true|read-only|none|
|» user|string|true|read-only|none|
|» is_successful|boolean|false|none|none|
|» incident_type|any|false|none|none|

*oneOf*

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|»» *anonymous*|[IncidentTypeEnum](#schemaincidenttypeenum)|false|none|* `INJ` - Injured<br>* `MIS` - Missing<br>* `FAT` - Fatality|

*xor*

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|»» *anonymous*|string|false|none|none|

*xor*

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|»» *anonymous*|object|false|none|none|

*continued*

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» incident_details|string¦null|false|none|none|
|» ascent|integer|true|read-only|none|

#### Enumerated Values

|Property|Value|
|---|---|
|*anonymous*|INJ|
|*anonymous*|MIS|
|*anonymous*|FAT|
|*anonymous*||
|*anonymous*|null|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth, tokenAuth, None
</aside>

## ascents_participants_create

<a id="opIdascents_participants_create"></a>

`POST /ascents/{id}/participants/`

> Body parameter

```json
{
  "is_successful": true,
  "incident_type": "INJ",
  "incident_details": "string"
}
```

```yaml
is_successful: true
incident_type: INJ
incident_details: string

```

<h3 id="ascents_participants_create-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|id|path|integer|true|none|
|body|body|[AscentParticipation](#schemaascentparticipation)|false|none|

> Example responses

> 201 Response

```json
{
  "id": 0,
  "user": "string",
  "is_successful": true,
  "incident_type": "INJ",
  "incident_details": "string",
  "ascent": 0
}
```

<h3 id="ascents_participants_create-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|201|[Created](https://tools.ietf.org/html/rfc7231#section-6.3.2)|none|[AscentParticipation](#schemaascentparticipation)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth, tokenAuth
</aside>

## ascents_me_list

<a id="opIdascents_me_list"></a>

`GET /ascents/me/`

<h3 id="ascents_me_list-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|ascent__route__mountain|query|integer|false|none|
|ordering|query|string|false|Which field to use when ordering the results.|

> Example responses

> 200 Response

```json
[
  {
    "id": 0,
    "user": "string",
    "ascent": {
      "id": 0,
      "route": {
        "id": 0,
        "name": "string",
        "description": "string",
        "duration_days": 32767,
        "mountain": 0
      },
      "mountain": {
        "id": 0,
        "name": "string",
        "elevation": 32767,
        "region": "string",
        "country": 0
      },
      "participants": [
        {
          "id": 0,
          "user": "string",
          "is_successful": true,
          "incident_type": "INJ",
          "incident_details": "string",
          "ascent": 0
        }
      ],
      "planned_start_datetime": "2019-08-24T14:15:22Z",
      "planned_end_datetime": "2019-08-24T14:15:22Z",
      "actual_start_datetime": "2019-08-24T14:15:22Z",
      "actual_end_datetime": "2019-08-24T14:15:22Z",
      "is_successful": true,
      "summary": "string"
    },
    "is_successful": true,
    "incident_type": "INJ",
    "incident_details": "string"
  }
]
```

<h3 id="ascents_me_list-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

<h3 id="ascents_me_list-responseschema">Response Schema</h3>

Status Code **200**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|*anonymous*|[[MyAscentParticipation](#schemamyascentparticipation)]|false|none|none|
|» id|integer|true|read-only|none|
|» user|string|true|read-only|none|
|» ascent|[AscentDetail](#schemaascentdetail)|true|read-only|none|
|»» id|integer|true|read-only|none|
|»» route|[Route](#schemaroute)|true|read-only|none|
|»»» id|integer|true|read-only|none|
|»»» name|string|true|none|none|
|»»» description|string¦null|false|none|none|
|»»» duration_days|integer¦null|false|none|none|
|»»» mountain|integer¦null|false|none|none|
|»» mountain|[Mountain](#schemamountain)|true|read-only|none|
|»»» id|integer|true|read-only|none|
|»»» name|string|true|none|none|
|»»» elevation|integer|true|none|none|
|»»» region|string¦null|false|none|none|
|»»» country|integer|true|none|none|
|»» participants|[[AscentParticipation](#schemaascentparticipation)]|true|read-only|none|
|»»» id|integer|true|read-only|none|
|»»» user|string|true|read-only|none|
|»»» is_successful|boolean|false|none|none|
|»»» incident_type|any|false|none|none|

*oneOf*

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|»»»» *anonymous*|[IncidentTypeEnum](#schemaincidenttypeenum)|false|none|* `INJ` - Injured<br>* `MIS` - Missing<br>* `FAT` - Fatality|

*xor*

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|»»»» *anonymous*|string|false|none|none|

*xor*

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|»»»» *anonymous*|object|false|none|none|

*continued*

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|»»» incident_details|string¦null|false|none|none|
|»»» ascent|integer|true|read-only|none|
|»» planned_start_datetime|string(date-time)|true|none|none|
|»» planned_end_datetime|string(date-time)|true|none|none|
|»» actual_start_datetime|string(date-time)¦null|false|none|none|
|»» actual_end_datetime|string(date-time)¦null|false|none|none|
|»» is_successful|boolean|false|none|none|
|»» summary|string¦null|false|none|none|
|» is_successful|boolean|false|none|none|
|» incident_type|any|false|none|none|

*oneOf*

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|»» *anonymous*|[IncidentTypeEnum](#schemaincidenttypeenum)|false|none|* `INJ` - Injured<br>* `MIS` - Missing<br>* `FAT` - Fatality|

*xor*

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|»» *anonymous*|string|false|none|none|

*xor*

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|»» *anonymous*|object|false|none|none|

*continued*

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» incident_details|string¦null|false|none|none|

#### Enumerated Values

|Property|Value|
|---|---|
|*anonymous*|INJ|
|*anonymous*|MIS|
|*anonymous*|FAT|
|*anonymous*||
|*anonymous*|null|
|*anonymous*|INJ|
|*anonymous*|MIS|
|*anonymous*|FAT|
|*anonymous*||
|*anonymous*|null|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth, tokenAuth
</aside>

<h1 id="api-auth">auth</h1>

## auth_token_login_create

<a id="opIdauth_token_login_create"></a>

`POST /auth/token/login/`

Use this endpoint to obtain user authentication token.

> Body parameter

```json
{
  "password": "string",
  "username": "string"
}
```

```yaml
password: string
username: string

```

<h3 id="auth_token_login_create-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[TokenCreate](#schematokencreate)|false|none|

> Example responses

> 200 Response

```json
{
  "password": "string",
  "username": "string"
}
```

<h3 id="auth_token_login_create-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[TokenCreate](#schematokencreate)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth, tokenAuth, None
</aside>

## auth_token_logout_create

<a id="opIdauth_token_logout_create"></a>

`POST /auth/token/logout/`

Use this endpoint to logout user (remove user authentication token).

<h3 id="auth_token_logout_create-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|No response body|None|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth, tokenAuth
</aside>

## auth_users_list

<a id="opIdauth_users_list"></a>

`GET /auth/users/`

> Example responses

> 200 Response

```json
[
  {
    "id": 0,
    "username": "string",
    "first_name": "string",
    "last_name": "string",
    "email": "user@example.com",
    "is_superuser": true,
    "is_staff": true,
    "phone_number": "string",
    "city": 0,
    "club": {
      "id": 0,
      "name": "string",
      "country": 0,
      "city": 0,
      "contact_user": 0
    }
  }
]
```

<h3 id="auth_users_list-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

<h3 id="auth_users_list-responseschema">Response Schema</h3>

Status Code **200**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|*anonymous*|[[User](#schemauser)]|false|none|none|
|» id|integer|true|read-only|none|
|» username|string|true|none|Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.|
|» first_name|string|true|none|none|
|» last_name|string|true|none|none|
|» email|string(email)|true|none|none|
|» is_superuser|boolean|false|none|Designates that this user has all permissions without explicitly assigning them.|
|» is_staff|boolean|false|none|Designates whether the user can log into this admin site.|
|» phone_number|string¦null|false|none|none|
|» city|integer¦null|false|none|none|
|» club|[Club](#schemaclub)|true|read-only|none|
|»» id|integer|true|read-only|none|
|»» name|string|true|none|none|
|»» country|integer¦null|false|none|none|
|»» city|integer¦null|false|none|none|
|»» contact_user|integer¦null|false|none|none|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth, tokenAuth
</aside>

## auth_users_create

<a id="opIdauth_users_create"></a>

`POST /auth/users/`

> Body parameter

```json
{
  "username": "string",
  "password": "string",
  "first_name": "string",
  "last_name": "string",
  "email": "user@example.com",
  "phone_number": "string",
  "city": 0
}
```

```yaml
username: string
password: string
first_name: string
last_name: string
email: user@example.com
phone_number: string
city: 0

```

<h3 id="auth_users_create-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[UserCreate](#schemausercreate)|true|none|

> Example responses

> 201 Response

```json
{
  "username": "string",
  "password": "string",
  "first_name": "string",
  "last_name": "string",
  "email": "user@example.com",
  "phone_number": "string",
  "city": 0
}
```

<h3 id="auth_users_create-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|201|[Created](https://tools.ietf.org/html/rfc7231#section-6.3.2)|none|[UserCreate](#schemausercreate)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth, tokenAuth, None
</aside>

## auth_users_retrieve

<a id="opIdauth_users_retrieve"></a>

`GET /auth/users/{id}/`

<h3 id="auth_users_retrieve-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|id|path|integer|true|A unique integer value identifying this user.|

> Example responses

> 200 Response

```json
{
  "id": 0,
  "username": "string",
  "first_name": "string",
  "last_name": "string",
  "email": "user@example.com",
  "is_superuser": true,
  "is_staff": true,
  "phone_number": "string",
  "city": 0,
  "club": {
    "id": 0,
    "name": "string",
    "country": 0,
    "city": 0,
    "contact_user": 0
  }
}
```

<h3 id="auth_users_retrieve-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[User](#schemauser)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth, tokenAuth
</aside>

## auth_users_update

<a id="opIdauth_users_update"></a>

`PUT /auth/users/{id}/`

> Body parameter

```json
{
  "username": "string",
  "first_name": "string",
  "last_name": "string",
  "email": "user@example.com",
  "is_superuser": true,
  "is_staff": true,
  "phone_number": "string",
  "city": 0
}
```

```yaml
username: string
first_name: string
last_name: string
email: user@example.com
is_superuser: true
is_staff: true
phone_number: string
city: 0

```

<h3 id="auth_users_update-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|id|path|integer|true|A unique integer value identifying this user.|
|body|body|[User](#schemauser)|true|none|

> Example responses

> 200 Response

```json
{
  "id": 0,
  "username": "string",
  "first_name": "string",
  "last_name": "string",
  "email": "user@example.com",
  "is_superuser": true,
  "is_staff": true,
  "phone_number": "string",
  "city": 0,
  "club": {
    "id": 0,
    "name": "string",
    "country": 0,
    "city": 0,
    "contact_user": 0
  }
}
```

<h3 id="auth_users_update-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[User](#schemauser)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth, tokenAuth
</aside>

## auth_users_partial_update

<a id="opIdauth_users_partial_update"></a>

`PATCH /auth/users/{id}/`

> Body parameter

```json
{
  "username": "string",
  "first_name": "string",
  "last_name": "string",
  "email": "user@example.com",
  "is_superuser": true,
  "is_staff": true,
  "phone_number": "string",
  "city": 0
}
```

```yaml
username: string
first_name: string
last_name: string
email: user@example.com
is_superuser: true
is_staff: true
phone_number: string
city: 0

```

<h3 id="auth_users_partial_update-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|id|path|integer|true|A unique integer value identifying this user.|
|body|body|[PatchedUser](#schemapatcheduser)|false|none|

> Example responses

> 200 Response

```json
{
  "id": 0,
  "username": "string",
  "first_name": "string",
  "last_name": "string",
  "email": "user@example.com",
  "is_superuser": true,
  "is_staff": true,
  "phone_number": "string",
  "city": 0,
  "club": {
    "id": 0,
    "name": "string",
    "country": 0,
    "city": 0,
    "contact_user": 0
  }
}
```

<h3 id="auth_users_partial_update-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[User](#schemauser)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth, tokenAuth
</aside>

## auth_users_destroy

<a id="opIdauth_users_destroy"></a>

`DELETE /auth/users/{id}/`

<h3 id="auth_users_destroy-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|id|path|integer|true|A unique integer value identifying this user.|

<h3 id="auth_users_destroy-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|204|[No Content](https://tools.ietf.org/html/rfc7231#section-6.3.5)|No response body|None|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth, tokenAuth
</aside>

## auth_users_activation_create

<a id="opIdauth_users_activation_create"></a>

`POST /auth/users/activation/`

> Body parameter

```json
{
  "uid": "string",
  "token": "string"
}
```

```yaml
uid: string
token: string

```

<h3 id="auth_users_activation_create-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[Activation](#schemaactivation)|true|none|

> Example responses

> 200 Response

```json
{
  "uid": "string",
  "token": "string"
}
```

<h3 id="auth_users_activation_create-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[Activation](#schemaactivation)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth, tokenAuth, None
</aside>

## auth_users_me_retrieve

<a id="opIdauth_users_me_retrieve"></a>

`GET /auth/users/me/`

> Example responses

> 200 Response

```json
{
  "id": 0,
  "username": "string",
  "first_name": "string",
  "last_name": "string",
  "email": "user@example.com",
  "is_superuser": true,
  "is_staff": true,
  "phone_number": "string",
  "city": 0,
  "club": {
    "id": 0,
    "name": "string",
    "country": 0,
    "city": 0,
    "contact_user": 0
  }
}
```

<h3 id="auth_users_me_retrieve-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[User](#schemauser)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth, tokenAuth
</aside>

## auth_users_me_update

<a id="opIdauth_users_me_update"></a>

`PUT /auth/users/me/`

> Body parameter

```json
{
  "username": "string",
  "first_name": "string",
  "last_name": "string",
  "email": "user@example.com",
  "is_superuser": true,
  "is_staff": true,
  "phone_number": "string",
  "city": 0
}
```

```yaml
username: string
first_name: string
last_name: string
email: user@example.com
is_superuser: true
is_staff: true
phone_number: string
city: 0

```

<h3 id="auth_users_me_update-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[User](#schemauser)|true|none|

> Example responses

> 200 Response

```json
{
  "id": 0,
  "username": "string",
  "first_name": "string",
  "last_name": "string",
  "email": "user@example.com",
  "is_superuser": true,
  "is_staff": true,
  "phone_number": "string",
  "city": 0,
  "club": {
    "id": 0,
    "name": "string",
    "country": 0,
    "city": 0,
    "contact_user": 0
  }
}
```

<h3 id="auth_users_me_update-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[User](#schemauser)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth, tokenAuth
</aside>

## auth_users_me_partial_update

<a id="opIdauth_users_me_partial_update"></a>

`PATCH /auth/users/me/`

> Body parameter

```json
{
  "username": "string",
  "first_name": "string",
  "last_name": "string",
  "email": "user@example.com",
  "is_superuser": true,
  "is_staff": true,
  "phone_number": "string",
  "city": 0
}
```

```yaml
username: string
first_name: string
last_name: string
email: user@example.com
is_superuser: true
is_staff: true
phone_number: string
city: 0

```

<h3 id="auth_users_me_partial_update-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[PatchedUser](#schemapatcheduser)|false|none|

> Example responses

> 200 Response

```json
{
  "id": 0,
  "username": "string",
  "first_name": "string",
  "last_name": "string",
  "email": "user@example.com",
  "is_superuser": true,
  "is_staff": true,
  "phone_number": "string",
  "city": 0,
  "club": {
    "id": 0,
    "name": "string",
    "country": 0,
    "city": 0,
    "contact_user": 0
  }
}
```

<h3 id="auth_users_me_partial_update-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[User](#schemauser)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth, tokenAuth
</aside>

## auth_users_me_destroy

<a id="opIdauth_users_me_destroy"></a>

`DELETE /auth/users/me/`

<h3 id="auth_users_me_destroy-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|204|[No Content](https://tools.ietf.org/html/rfc7231#section-6.3.5)|No response body|None|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth, tokenAuth
</aside>

## auth_users_resend_activation_create

<a id="opIdauth_users_resend_activation_create"></a>

`POST /auth/users/resend_activation/`

> Body parameter

```json
{
  "email": "user@example.com"
}
```

```yaml
email: user@example.com

```

<h3 id="auth_users_resend_activation_create-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[SendEmailReset](#schemasendemailreset)|true|none|

> Example responses

> 200 Response

```json
{
  "email": "user@example.com"
}
```

<h3 id="auth_users_resend_activation_create-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[SendEmailReset](#schemasendemailreset)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth, tokenAuth, None
</aside>

## auth_users_reset_password_create

<a id="opIdauth_users_reset_password_create"></a>

`POST /auth/users/reset_password/`

> Body parameter

```json
{
  "email": "user@example.com"
}
```

```yaml
email: user@example.com

```

<h3 id="auth_users_reset_password_create-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[SendEmailReset](#schemasendemailreset)|true|none|

> Example responses

> 200 Response

```json
{
  "email": "user@example.com"
}
```

<h3 id="auth_users_reset_password_create-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[SendEmailReset](#schemasendemailreset)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth, tokenAuth, None
</aside>

## auth_users_reset_password_confirm_create

<a id="opIdauth_users_reset_password_confirm_create"></a>

`POST /auth/users/reset_password_confirm/`

> Body parameter

```json
{
  "uid": "string",
  "token": "string",
  "new_password": "string"
}
```

```yaml
uid: string
token: string
new_password: string

```

<h3 id="auth_users_reset_password_confirm_create-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[PasswordResetConfirm](#schemapasswordresetconfirm)|true|none|

> Example responses

> 200 Response

```json
{
  "uid": "string",
  "token": "string",
  "new_password": "string"
}
```

<h3 id="auth_users_reset_password_confirm_create-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[PasswordResetConfirm](#schemapasswordresetconfirm)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth, tokenAuth, None
</aside>

## auth_users_reset_username_create

<a id="opIdauth_users_reset_username_create"></a>

`POST /auth/users/reset_username/`

> Body parameter

```json
{
  "email": "user@example.com"
}
```

```yaml
email: user@example.com

```

<h3 id="auth_users_reset_username_create-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[SendEmailReset](#schemasendemailreset)|true|none|

> Example responses

> 200 Response

```json
{
  "email": "user@example.com"
}
```

<h3 id="auth_users_reset_username_create-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[SendEmailReset](#schemasendemailreset)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth, tokenAuth, None
</aside>

## auth_users_reset_username_confirm_create

<a id="opIdauth_users_reset_username_confirm_create"></a>

`POST /auth/users/reset_username_confirm/`

> Body parameter

```json
{
  "new_username": "string"
}
```

```yaml
new_username: string

```

<h3 id="auth_users_reset_username_confirm_create-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[UsernameResetConfirm](#schemausernameresetconfirm)|true|none|

> Example responses

> 200 Response

```json
{
  "new_username": "string"
}
```

<h3 id="auth_users_reset_username_confirm_create-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[UsernameResetConfirm](#schemausernameresetconfirm)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth, tokenAuth, None
</aside>

## auth_users_set_password_create

<a id="opIdauth_users_set_password_create"></a>

`POST /auth/users/set_password/`

> Body parameter

```json
{
  "new_password": "string",
  "current_password": "string"
}
```

```yaml
new_password: string
current_password: string

```

<h3 id="auth_users_set_password_create-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[SetPassword](#schemasetpassword)|true|none|

> Example responses

> 200 Response

```json
{
  "new_password": "string",
  "current_password": "string"
}
```

<h3 id="auth_users_set_password_create-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[SetPassword](#schemasetpassword)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth, tokenAuth
</aside>

## auth_users_set_username_create

<a id="opIdauth_users_set_username_create"></a>

`POST /auth/users/set_username/`

> Body parameter

```json
{
  "current_password": "string",
  "new_username": "string"
}
```

```yaml
current_password: string
new_username: string

```

<h3 id="auth_users_set_username_create-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[SetUsername](#schemasetusername)|true|none|

> Example responses

> 200 Response

```json
{
  "current_password": "string",
  "new_username": "string"
}
```

<h3 id="auth_users_set_username_create-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[SetUsername](#schemasetusername)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth, tokenAuth
</aside>

<h1 id="api-cities">cities</h1>

## cities_list

<a id="opIdcities_list"></a>

`GET /cities/`

<h3 id="cities_list-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|country|query|integer|false|none|
|ordering|query|string|false|Which field to use when ordering the results.|

> Example responses

> 200 Response

```json
[
  {
    "id": 0,
    "name": "string",
    "country": {
      "id": 0,
      "name": "string"
    }
  }
]
```

<h3 id="cities_list-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

<h3 id="cities_list-responseschema">Response Schema</h3>

Status Code **200**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|*anonymous*|[[CityDetail](#schemacitydetail)]|false|none|none|
|» id|integer|true|read-only|none|
|» name|string|true|none|none|
|» country|[Country](#schemacountry)|true|read-only|none|
|»» id|integer|true|read-only|none|
|»» name|string|true|none|none|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth, tokenAuth
</aside>

## cities_create

<a id="opIdcities_create"></a>

`POST /cities/`

> Body parameter

```json
{
  "name": "string",
  "country": 0
}
```

```yaml
name: string
country: 0

```

<h3 id="cities_create-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[City](#schemacity)|true|none|

> Example responses

> 201 Response

```json
{
  "id": 0,
  "name": "string",
  "country": 0
}
```

<h3 id="cities_create-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|201|[Created](https://tools.ietf.org/html/rfc7231#section-6.3.2)|none|[City](#schemacity)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth, tokenAuth
</aside>

## cities_retrieve

<a id="opIdcities_retrieve"></a>

`GET /cities/{id}/`

<h3 id="cities_retrieve-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|id|path|integer|true|none|

> Example responses

> 200 Response

```json
{
  "id": 0,
  "name": "string",
  "country": {
    "id": 0,
    "name": "string"
  }
}
```

<h3 id="cities_retrieve-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[CityDetail](#schemacitydetail)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth, tokenAuth
</aside>

## cities_update

<a id="opIdcities_update"></a>

`PUT /cities/{id}/`

> Body parameter

```json
{
  "name": "string",
  "country": 0
}
```

```yaml
name: string
country: 0

```

<h3 id="cities_update-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|id|path|integer|true|none|
|body|body|[City](#schemacity)|true|none|

> Example responses

> 200 Response

```json
{
  "id": 0,
  "name": "string",
  "country": 0
}
```

<h3 id="cities_update-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[City](#schemacity)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth, tokenAuth
</aside>

## cities_partial_update

<a id="opIdcities_partial_update"></a>

`PATCH /cities/{id}/`

> Body parameter

```json
{
  "name": "string",
  "country": 0
}
```

```yaml
name: string
country: 0

```

<h3 id="cities_partial_update-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|id|path|integer|true|none|
|body|body|[PatchedCity](#schemapatchedcity)|false|none|

> Example responses

> 200 Response

```json
{
  "id": 0,
  "name": "string",
  "country": 0
}
```

<h3 id="cities_partial_update-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[City](#schemacity)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth, tokenAuth
</aside>

## cities_destroy

<a id="opIdcities_destroy"></a>

`DELETE /cities/{id}/`

<h3 id="cities_destroy-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|id|path|integer|true|none|

<h3 id="cities_destroy-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|204|[No Content](https://tools.ietf.org/html/rfc7231#section-6.3.5)|No response body|None|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth, tokenAuth
</aside>

<h1 id="api-clubs">clubs</h1>

## clubs_list

<a id="opIdclubs_list"></a>

`GET /clubs/`

<h3 id="clubs_list-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|country|query|integer|false|none|
|ordering|query|string|false|Which field to use when ordering the results.|

> Example responses

> 200 Response

```json
[
  {
    "id": 0,
    "name": "string",
    "country": 0,
    "city": 0,
    "contact_user": 0
  }
]
```

<h3 id="clubs_list-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

<h3 id="clubs_list-responseschema">Response Schema</h3>

Status Code **200**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|*anonymous*|[[Club](#schemaclub)]|false|none|none|
|» id|integer|true|read-only|none|
|» name|string|true|none|none|
|» country|integer¦null|false|none|none|
|» city|integer¦null|false|none|none|
|» contact_user|integer¦null|false|none|none|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth, tokenAuth
</aside>

## clubs_create

<a id="opIdclubs_create"></a>

`POST /clubs/`

> Body parameter

```json
{
  "name": "string",
  "country": 0,
  "city": 0,
  "contact_user": 0
}
```

```yaml
name: string
country: 0
city: 0
contact_user: 0

```

<h3 id="clubs_create-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[Club](#schemaclub)|true|none|

> Example responses

> 201 Response

```json
{
  "id": 0,
  "name": "string",
  "country": 0,
  "city": 0,
  "contact_user": 0
}
```

<h3 id="clubs_create-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|201|[Created](https://tools.ietf.org/html/rfc7231#section-6.3.2)|none|[Club](#schemaclub)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth, tokenAuth
</aside>

## clubs_members_retrieve

<a id="opIdclubs_members_retrieve"></a>

`GET /clubs/{club_pk}/members/{membership_pk}/`

<h3 id="clubs_members_retrieve-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|club_pk|path|integer|true|none|
|membership_pk|path|integer|true|none|

> Example responses

> 200 Response

```json
{
  "id": 0,
  "join_datetime": "2019-08-24T14:15:22Z",
  "leave_datetime": "2019-08-24T14:15:22Z",
  "user": 0,
  "club": 0
}
```

<h3 id="clubs_members_retrieve-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[ClubMembership](#schemaclubmembership)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth, tokenAuth
</aside>

## clubs_members_update

<a id="opIdclubs_members_update"></a>

`PUT /clubs/{club_pk}/members/{membership_pk}/`

> Body parameter

```json
{
  "join_datetime": "2019-08-24T14:15:22Z",
  "leave_datetime": "2019-08-24T14:15:22Z"
}
```

```yaml
join_datetime: 2019-08-24T14:15:22Z
leave_datetime: 2019-08-24T14:15:22Z

```

<h3 id="clubs_members_update-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|club_pk|path|integer|true|none|
|membership_pk|path|integer|true|none|
|body|body|[ClubMembership](#schemaclubmembership)|false|none|

> Example responses

> 200 Response

```json
{
  "id": 0,
  "join_datetime": "2019-08-24T14:15:22Z",
  "leave_datetime": "2019-08-24T14:15:22Z",
  "user": 0,
  "club": 0
}
```

<h3 id="clubs_members_update-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[ClubMembership](#schemaclubmembership)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth, tokenAuth
</aside>

## clubs_members_partial_update

<a id="opIdclubs_members_partial_update"></a>

`PATCH /clubs/{club_pk}/members/{membership_pk}/`

> Body parameter

```json
{
  "join_datetime": "2019-08-24T14:15:22Z",
  "leave_datetime": "2019-08-24T14:15:22Z"
}
```

```yaml
join_datetime: 2019-08-24T14:15:22Z
leave_datetime: 2019-08-24T14:15:22Z

```

<h3 id="clubs_members_partial_update-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|club_pk|path|integer|true|none|
|membership_pk|path|integer|true|none|
|body|body|[PatchedClubMembership](#schemapatchedclubmembership)|false|none|

> Example responses

> 200 Response

```json
{
  "id": 0,
  "join_datetime": "2019-08-24T14:15:22Z",
  "leave_datetime": "2019-08-24T14:15:22Z",
  "user": 0,
  "club": 0
}
```

<h3 id="clubs_members_partial_update-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[ClubMembership](#schemaclubmembership)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth, tokenAuth
</aside>

## clubs_members_destroy

<a id="opIdclubs_members_destroy"></a>

`DELETE /clubs/{club_pk}/members/{membership_pk}/`

<h3 id="clubs_members_destroy-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|club_pk|path|integer|true|none|
|membership_pk|path|integer|true|none|

<h3 id="clubs_members_destroy-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|204|[No Content](https://tools.ietf.org/html/rfc7231#section-6.3.5)|No response body|None|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth, tokenAuth
</aside>

## clubs_retrieve

<a id="opIdclubs_retrieve"></a>

`GET /clubs/{id}/`

<h3 id="clubs_retrieve-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|id|path|integer|true|none|

> Example responses

> 200 Response

```json
{
  "id": 0,
  "members": [
    {
      "id": 0,
      "join_datetime": "2019-08-24T14:15:22Z",
      "leave_datetime": "2019-08-24T14:15:22Z",
      "user": 0,
      "club": 0
    }
  ],
  "country": {
    "id": 0,
    "name": "string"
  },
  "city": {
    "id": 0,
    "name": "string",
    "country": 0
  },
  "name": "string",
  "contact_user": 0
}
```

<h3 id="clubs_retrieve-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[ClubDetail](#schemaclubdetail)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth, tokenAuth
</aside>

## clubs_update

<a id="opIdclubs_update"></a>

`PUT /clubs/{id}/`

> Body parameter

```json
{
  "name": "string",
  "country": 0,
  "city": 0,
  "contact_user": 0
}
```

```yaml
name: string
country: 0
city: 0
contact_user: 0

```

<h3 id="clubs_update-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|id|path|integer|true|none|
|body|body|[Club](#schemaclub)|true|none|

> Example responses

> 200 Response

```json
{
  "id": 0,
  "name": "string",
  "country": 0,
  "city": 0,
  "contact_user": 0
}
```

<h3 id="clubs_update-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[Club](#schemaclub)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth, tokenAuth
</aside>

## clubs_partial_update

<a id="opIdclubs_partial_update"></a>

`PATCH /clubs/{id}/`

> Body parameter

```json
{
  "name": "string",
  "country": 0,
  "city": 0,
  "contact_user": 0
}
```

```yaml
name: string
country: 0
city: 0
contact_user: 0

```

<h3 id="clubs_partial_update-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|id|path|integer|true|none|
|body|body|[PatchedClub](#schemapatchedclub)|false|none|

> Example responses

> 200 Response

```json
{
  "id": 0,
  "name": "string",
  "country": 0,
  "city": 0,
  "contact_user": 0
}
```

<h3 id="clubs_partial_update-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[Club](#schemaclub)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth, tokenAuth
</aside>

## clubs_destroy

<a id="opIdclubs_destroy"></a>

`DELETE /clubs/{id}/`

<h3 id="clubs_destroy-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|id|path|integer|true|none|

<h3 id="clubs_destroy-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|204|[No Content](https://tools.ietf.org/html/rfc7231#section-6.3.5)|No response body|None|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth, tokenAuth
</aside>

## clubs_leave_update

<a id="opIdclubs_leave_update"></a>

`PUT /clubs/{id}/leave/`

> Body parameter

```json
{
  "join_datetime": "2019-08-24T14:15:22Z",
  "leave_datetime": "2019-08-24T14:15:22Z"
}
```

```yaml
join_datetime: 2019-08-24T14:15:22Z
leave_datetime: 2019-08-24T14:15:22Z

```

<h3 id="clubs_leave_update-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|id|path|integer|true|none|
|body|body|[ClubMembership](#schemaclubmembership)|false|none|

> Example responses

> 200 Response

```json
{
  "id": 0,
  "join_datetime": "2019-08-24T14:15:22Z",
  "leave_datetime": "2019-08-24T14:15:22Z",
  "user": 0,
  "club": 0
}
```

<h3 id="clubs_leave_update-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[ClubMembership](#schemaclubmembership)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth, tokenAuth
</aside>

## clubs_leave_partial_update

<a id="opIdclubs_leave_partial_update"></a>

`PATCH /clubs/{id}/leave/`

> Body parameter

```json
{
  "join_datetime": "2019-08-24T14:15:22Z",
  "leave_datetime": "2019-08-24T14:15:22Z"
}
```

```yaml
join_datetime: 2019-08-24T14:15:22Z
leave_datetime: 2019-08-24T14:15:22Z

```

<h3 id="clubs_leave_partial_update-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|id|path|integer|true|none|
|body|body|[PatchedClubMembership](#schemapatchedclubmembership)|false|none|

> Example responses

> 200 Response

```json
{
  "id": 0,
  "join_datetime": "2019-08-24T14:15:22Z",
  "leave_datetime": "2019-08-24T14:15:22Z",
  "user": 0,
  "club": 0
}
```

<h3 id="clubs_leave_partial_update-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[ClubMembership](#schemaclubmembership)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth, tokenAuth
</aside>

## clubs_members_list

<a id="opIdclubs_members_list"></a>

`GET /clubs/{id}/members/`

<h3 id="clubs_members_list-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|id|path|integer|true|none|
|ordering|query|string|false|Which field to use when ordering the results.|

> Example responses

> 200 Response

```json
[
  {
    "id": 0,
    "join_datetime": "2019-08-24T14:15:22Z",
    "leave_datetime": "2019-08-24T14:15:22Z",
    "user": 0,
    "club": 0
  }
]
```

<h3 id="clubs_members_list-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

<h3 id="clubs_members_list-responseschema">Response Schema</h3>

Status Code **200**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|*anonymous*|[[ClubMembership](#schemaclubmembership)]|false|none|none|
|» id|integer|true|read-only|none|
|» join_datetime|string(date-time)|false|none|none|
|» leave_datetime|string(date-time)¦null|false|none|none|
|» user|integer|true|read-only|none|
|» club|integer|true|read-only|none|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth, tokenAuth, None
</aside>

## clubs_members_create

<a id="opIdclubs_members_create"></a>

`POST /clubs/{id}/members/`

> Body parameter

```json
{
  "join_datetime": "2019-08-24T14:15:22Z",
  "leave_datetime": "2019-08-24T14:15:22Z"
}
```

```yaml
join_datetime: 2019-08-24T14:15:22Z
leave_datetime: 2019-08-24T14:15:22Z

```

<h3 id="clubs_members_create-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|id|path|integer|true|none|
|body|body|[ClubMembership](#schemaclubmembership)|false|none|

> Example responses

> 201 Response

```json
{
  "id": 0,
  "join_datetime": "2019-08-24T14:15:22Z",
  "leave_datetime": "2019-08-24T14:15:22Z",
  "user": 0,
  "club": 0
}
```

<h3 id="clubs_members_create-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|201|[Created](https://tools.ietf.org/html/rfc7231#section-6.3.2)|none|[ClubMembership](#schemaclubmembership)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth, tokenAuth
</aside>

## clubs_me_list

<a id="opIdclubs_me_list"></a>

`GET /clubs/me/`

<h3 id="clubs_me_list-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|active|query|boolean|false|none|
|ordering|query|string|false|Which field to use when ordering the results.|

> Example responses

> 200 Response

```json
[
  {
    "id": 0,
    "club": {
      "id": 0,
      "name": "string",
      "country": 0,
      "city": 0,
      "contact_user": 0
    },
    "join_datetime": "2019-08-24T14:15:22Z",
    "leave_datetime": "2019-08-24T14:15:22Z",
    "user": 0
  }
]
```

<h3 id="clubs_me_list-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

<h3 id="clubs_me_list-responseschema">Response Schema</h3>

Status Code **200**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|*anonymous*|[[MyClubMemberShip](#schemamyclubmembership)]|false|none|none|
|» id|integer|true|read-only|none|
|» club|[Club](#schemaclub)|true|read-only|none|
|»» id|integer|true|read-only|none|
|»» name|string|true|none|none|
|»» country|integer¦null|false|none|none|
|»» city|integer¦null|false|none|none|
|»» contact_user|integer¦null|false|none|none|
|» join_datetime|string(date-time)|false|none|none|
|» leave_datetime|string(date-time)¦null|false|none|none|
|» user|integer|true|read-only|none|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth, tokenAuth
</aside>

<h1 id="api-countries">countries</h1>

## countries_list

<a id="opIdcountries_list"></a>

`GET /countries/`

<h3 id="countries_list-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|ordering|query|string|false|Which field to use when ordering the results.|

> Example responses

> 200 Response

```json
[
  {
    "id": 0,
    "name": "string"
  }
]
```

<h3 id="countries_list-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

<h3 id="countries_list-responseschema">Response Schema</h3>

Status Code **200**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|*anonymous*|[[Country](#schemacountry)]|false|none|none|
|» id|integer|true|read-only|none|
|» name|string|true|none|none|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth, tokenAuth
</aside>

## countries_create

<a id="opIdcountries_create"></a>

`POST /countries/`

> Body parameter

```json
{
  "name": "string"
}
```

```yaml
name: string

```

<h3 id="countries_create-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[Country](#schemacountry)|true|none|

> Example responses

> 201 Response

```json
{
  "id": 0,
  "name": "string"
}
```

<h3 id="countries_create-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|201|[Created](https://tools.ietf.org/html/rfc7231#section-6.3.2)|none|[Country](#schemacountry)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth, tokenAuth
</aside>

## countries_retrieve

<a id="opIdcountries_retrieve"></a>

`GET /countries/{id}/`

<h3 id="countries_retrieve-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|id|path|integer|true|none|

> Example responses

> 200 Response

```json
{
  "id": 0,
  "name": "string",
  "cities": [
    "string"
  ],
  "clubs": [
    "string"
  ],
  "mountains": [
    "string"
  ]
}
```

<h3 id="countries_retrieve-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[CountryDetail](#schemacountrydetail)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth, tokenAuth
</aside>

## countries_update

<a id="opIdcountries_update"></a>

`PUT /countries/{id}/`

> Body parameter

```json
{
  "name": "string"
}
```

```yaml
name: string

```

<h3 id="countries_update-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|id|path|integer|true|none|
|body|body|[CountryDetail](#schemacountrydetail)|true|none|

> Example responses

> 200 Response

```json
{
  "id": 0,
  "name": "string",
  "cities": [
    "string"
  ],
  "clubs": [
    "string"
  ],
  "mountains": [
    "string"
  ]
}
```

<h3 id="countries_update-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[CountryDetail](#schemacountrydetail)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth, tokenAuth
</aside>

## countries_partial_update

<a id="opIdcountries_partial_update"></a>

`PATCH /countries/{id}/`

> Body parameter

```json
{
  "name": "string"
}
```

```yaml
name: string

```

<h3 id="countries_partial_update-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|id|path|integer|true|none|
|body|body|[PatchedCountryDetail](#schemapatchedcountrydetail)|false|none|

> Example responses

> 200 Response

```json
{
  "id": 0,
  "name": "string",
  "cities": [
    "string"
  ],
  "clubs": [
    "string"
  ],
  "mountains": [
    "string"
  ]
}
```

<h3 id="countries_partial_update-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[CountryDetail](#schemacountrydetail)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth, tokenAuth
</aside>

## countries_destroy

<a id="opIdcountries_destroy"></a>

`DELETE /countries/{id}/`

<h3 id="countries_destroy-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|id|path|integer|true|none|

<h3 id="countries_destroy-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|204|[No Content](https://tools.ietf.org/html/rfc7231#section-6.3.5)|No response body|None|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth, tokenAuth
</aside>

<h1 id="api-mountains">mountains</h1>

## mountains_list

<a id="opIdmountains_list"></a>

`GET /mountains/`

<h3 id="mountains_list-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|country|query|integer|false|none|
|ordering|query|string|false|Which field to use when ordering the results.|

> Example responses

> 200 Response

```json
[
  {
    "id": 0,
    "name": "string",
    "elevation": 32767,
    "region": "string",
    "country": {
      "id": 0,
      "name": "string"
    },
    "routes": [
      {
        "id": 0,
        "name": "string",
        "description": "string",
        "duration_days": 32767,
        "mountain": 0
      }
    ]
  }
]
```

<h3 id="mountains_list-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

<h3 id="mountains_list-responseschema">Response Schema</h3>

Status Code **200**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|*anonymous*|[[MountainDetail](#schemamountaindetail)]|false|none|none|
|» id|integer|true|read-only|none|
|» name|string|true|none|none|
|» elevation|integer|true|none|none|
|» region|string¦null|false|none|none|
|» country|[Country](#schemacountry)|true|read-only|none|
|»» id|integer|true|read-only|none|
|»» name|string|true|none|none|
|» routes|[[Route](#schemaroute)]|true|read-only|none|
|»» id|integer|true|read-only|none|
|»» name|string|true|none|none|
|»» description|string¦null|false|none|none|
|»» duration_days|integer¦null|false|none|none|
|»» mountain|integer¦null|false|none|none|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth, tokenAuth
</aside>

## mountains_create

<a id="opIdmountains_create"></a>

`POST /mountains/`

> Body parameter

```json
{
  "name": "string",
  "elevation": 32767,
  "region": "string",
  "country": 0
}
```

```yaml
name: string
elevation: 32767
region: string
country: 0

```

<h3 id="mountains_create-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[Mountain](#schemamountain)|true|none|

> Example responses

> 201 Response

```json
{
  "id": 0,
  "name": "string",
  "elevation": 32767,
  "region": "string",
  "country": 0
}
```

<h3 id="mountains_create-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|201|[Created](https://tools.ietf.org/html/rfc7231#section-6.3.2)|none|[Mountain](#schemamountain)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth, tokenAuth
</aside>

## mountains_retrieve

<a id="opIdmountains_retrieve"></a>

`GET /mountains/{id}/`

<h3 id="mountains_retrieve-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|id|path|integer|true|none|

> Example responses

> 200 Response

```json
{
  "id": 0,
  "name": "string",
  "elevation": 32767,
  "region": "string",
  "country": {
    "id": 0,
    "name": "string"
  },
  "routes": [
    {
      "id": 0,
      "name": "string",
      "description": "string",
      "duration_days": 32767,
      "mountain": 0
    }
  ]
}
```

<h3 id="mountains_retrieve-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[MountainDetail](#schemamountaindetail)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth, tokenAuth
</aside>

## mountains_update

<a id="opIdmountains_update"></a>

`PUT /mountains/{id}/`

> Body parameter

```json
{
  "name": "string",
  "elevation": 32767,
  "region": "string",
  "country": 0
}
```

```yaml
name: string
elevation: 32767
region: string
country: 0

```

<h3 id="mountains_update-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|id|path|integer|true|none|
|body|body|[Mountain](#schemamountain)|true|none|

> Example responses

> 200 Response

```json
{
  "id": 0,
  "name": "string",
  "elevation": 32767,
  "region": "string",
  "country": 0
}
```

<h3 id="mountains_update-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[Mountain](#schemamountain)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth, tokenAuth
</aside>

## mountains_partial_update

<a id="opIdmountains_partial_update"></a>

`PATCH /mountains/{id}/`

> Body parameter

```json
{
  "name": "string",
  "elevation": 32767,
  "region": "string",
  "country": 0
}
```

```yaml
name: string
elevation: 32767
region: string
country: 0

```

<h3 id="mountains_partial_update-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|id|path|integer|true|none|
|body|body|[PatchedMountain](#schemapatchedmountain)|false|none|

> Example responses

> 200 Response

```json
{
  "id": 0,
  "name": "string",
  "elevation": 32767,
  "region": "string",
  "country": 0
}
```

<h3 id="mountains_partial_update-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[Mountain](#schemamountain)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth, tokenAuth
</aside>

## mountains_destroy

<a id="opIdmountains_destroy"></a>

`DELETE /mountains/{id}/`

<h3 id="mountains_destroy-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|id|path|integer|true|none|

<h3 id="mountains_destroy-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|204|[No Content](https://tools.ietf.org/html/rfc7231#section-6.3.5)|No response body|None|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth, tokenAuth
</aside>

<h1 id="api-routes">routes</h1>

## routes_list

<a id="opIdroutes_list"></a>

`GET /routes/`

<h3 id="routes_list-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|mountain|query|integer|false|none|
|ordering|query|string|false|Which field to use when ordering the results.|

> Example responses

> 200 Response

```json
[
  {
    "id": 0,
    "name": "string",
    "description": "string",
    "duration_days": 32767,
    "mountain": {
      "id": 0,
      "name": "string",
      "elevation": 32767,
      "region": "string",
      "country": 0
    },
    "ascents": [
      {
        "id": 0,
        "planned_start_datetime": "2019-08-24T14:15:22Z",
        "planned_end_datetime": "2019-08-24T14:15:22Z",
        "actual_start_datetime": "2019-08-24T14:15:22Z",
        "actual_end_datetime": "2019-08-24T14:15:22Z",
        "is_successful": true,
        "summary": "string",
        "route": 0
      }
    ]
  }
]
```

<h3 id="routes_list-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

<h3 id="routes_list-responseschema">Response Schema</h3>

Status Code **200**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|*anonymous*|[[RouteDetail](#schemaroutedetail)]|false|none|none|
|» id|integer|true|read-only|none|
|» name|string|true|none|none|
|» description|string¦null|false|none|none|
|» duration_days|integer¦null|false|none|none|
|» mountain|[Mountain](#schemamountain)|true|read-only|none|
|»» id|integer|true|read-only|none|
|»» name|string|true|none|none|
|»» elevation|integer|true|none|none|
|»» region|string¦null|false|none|none|
|»» country|integer|true|none|none|
|» ascents|[[Ascent](#schemaascent)]|true|read-only|none|
|»» id|integer|true|read-only|none|
|»» planned_start_datetime|string(date-time)|true|none|none|
|»» planned_end_datetime|string(date-time)|true|none|none|
|»» actual_start_datetime|string(date-time)¦null|false|none|none|
|»» actual_end_datetime|string(date-time)¦null|false|none|none|
|»» is_successful|boolean|false|none|none|
|»» summary|string¦null|false|none|none|
|»» route|integer|true|none|none|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth, tokenAuth
</aside>

## routes_create

<a id="opIdroutes_create"></a>

`POST /routes/`

> Body parameter

```json
{
  "name": "string",
  "description": "string",
  "duration_days": 32767,
  "mountain": 0
}
```

```yaml
name: string
description: string
duration_days: 32767
mountain: 0

```

<h3 id="routes_create-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[Route](#schemaroute)|true|none|

> Example responses

> 201 Response

```json
{
  "id": 0,
  "name": "string",
  "description": "string",
  "duration_days": 32767,
  "mountain": 0
}
```

<h3 id="routes_create-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|201|[Created](https://tools.ietf.org/html/rfc7231#section-6.3.2)|none|[Route](#schemaroute)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth, tokenAuth
</aside>

## routes_retrieve

<a id="opIdroutes_retrieve"></a>

`GET /routes/{id}/`

<h3 id="routes_retrieve-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|id|path|integer|true|none|

> Example responses

> 200 Response

```json
{
  "id": 0,
  "name": "string",
  "description": "string",
  "duration_days": 32767,
  "mountain": {
    "id": 0,
    "name": "string",
    "elevation": 32767,
    "region": "string",
    "country": 0
  },
  "ascents": [
    {
      "id": 0,
      "planned_start_datetime": "2019-08-24T14:15:22Z",
      "planned_end_datetime": "2019-08-24T14:15:22Z",
      "actual_start_datetime": "2019-08-24T14:15:22Z",
      "actual_end_datetime": "2019-08-24T14:15:22Z",
      "is_successful": true,
      "summary": "string",
      "route": 0
    }
  ]
}
```

<h3 id="routes_retrieve-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[RouteDetail](#schemaroutedetail)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth, tokenAuth
</aside>

## routes_update

<a id="opIdroutes_update"></a>

`PUT /routes/{id}/`

> Body parameter

```json
{
  "name": "string",
  "description": "string",
  "duration_days": 32767,
  "mountain": 0
}
```

```yaml
name: string
description: string
duration_days: 32767
mountain: 0

```

<h3 id="routes_update-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|id|path|integer|true|none|
|body|body|[Route](#schemaroute)|true|none|

> Example responses

> 200 Response

```json
{
  "id": 0,
  "name": "string",
  "description": "string",
  "duration_days": 32767,
  "mountain": 0
}
```

<h3 id="routes_update-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[Route](#schemaroute)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth, tokenAuth
</aside>

## routes_partial_update

<a id="opIdroutes_partial_update"></a>

`PATCH /routes/{id}/`

> Body parameter

```json
{
  "name": "string",
  "description": "string",
  "duration_days": 32767,
  "mountain": 0
}
```

```yaml
name: string
description: string
duration_days: 32767
mountain: 0

```

<h3 id="routes_partial_update-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|id|path|integer|true|none|
|body|body|[PatchedRoute](#schemapatchedroute)|false|none|

> Example responses

> 200 Response

```json
{
  "id": 0,
  "name": "string",
  "description": "string",
  "duration_days": 32767,
  "mountain": 0
}
```

<h3 id="routes_partial_update-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[Route](#schemaroute)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth, tokenAuth
</aside>

## routes_destroy

<a id="opIdroutes_destroy"></a>

`DELETE /routes/{id}/`

<h3 id="routes_destroy-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|id|path|integer|true|none|

<h3 id="routes_destroy-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|204|[No Content](https://tools.ietf.org/html/rfc7231#section-6.3.5)|No response body|None|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
cookieAuth, tokenAuth
</aside>

# Schemas

<h2 id="tocS_Activation">Activation</h2>
<!-- backwards compatibility -->
<a id="schemaactivation"></a>
<a id="schema_Activation"></a>
<a id="tocSactivation"></a>
<a id="tocsactivation"></a>

```json
{
  "uid": "string",
  "token": "string"
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|uid|string|true|none|none|
|token|string|true|none|none|

<h2 id="tocS_Ascent">Ascent</h2>
<!-- backwards compatibility -->
<a id="schemaascent"></a>
<a id="schema_Ascent"></a>
<a id="tocSascent"></a>
<a id="tocsascent"></a>

```json
{
  "id": 0,
  "planned_start_datetime": "2019-08-24T14:15:22Z",
  "planned_end_datetime": "2019-08-24T14:15:22Z",
  "actual_start_datetime": "2019-08-24T14:15:22Z",
  "actual_end_datetime": "2019-08-24T14:15:22Z",
  "is_successful": true,
  "summary": "string",
  "route": 0
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|id|integer|true|read-only|none|
|planned_start_datetime|string(date-time)|true|none|none|
|planned_end_datetime|string(date-time)|true|none|none|
|actual_start_datetime|string(date-time)¦null|false|none|none|
|actual_end_datetime|string(date-time)¦null|false|none|none|
|is_successful|boolean|false|none|none|
|summary|string¦null|false|none|none|
|route|integer|true|none|none|

<h2 id="tocS_AscentDetail">AscentDetail</h2>
<!-- backwards compatibility -->
<a id="schemaascentdetail"></a>
<a id="schema_AscentDetail"></a>
<a id="tocSascentdetail"></a>
<a id="tocsascentdetail"></a>

```json
{
  "id": 0,
  "route": {
    "id": 0,
    "name": "string",
    "description": "string",
    "duration_days": 32767,
    "mountain": 0
  },
  "mountain": {
    "id": 0,
    "name": "string",
    "elevation": 32767,
    "region": "string",
    "country": 0
  },
  "participants": [
    {
      "id": 0,
      "user": "string",
      "is_successful": true,
      "incident_type": "INJ",
      "incident_details": "string",
      "ascent": 0
    }
  ],
  "planned_start_datetime": "2019-08-24T14:15:22Z",
  "planned_end_datetime": "2019-08-24T14:15:22Z",
  "actual_start_datetime": "2019-08-24T14:15:22Z",
  "actual_end_datetime": "2019-08-24T14:15:22Z",
  "is_successful": true,
  "summary": "string"
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|id|integer|true|read-only|none|
|route|[Route](#schemaroute)|true|read-only|none|
|mountain|[Mountain](#schemamountain)|true|read-only|none|
|participants|[[AscentParticipation](#schemaascentparticipation)]|true|read-only|none|
|planned_start_datetime|string(date-time)|true|none|none|
|planned_end_datetime|string(date-time)|true|none|none|
|actual_start_datetime|string(date-time)¦null|false|none|none|
|actual_end_datetime|string(date-time)¦null|false|none|none|
|is_successful|boolean|false|none|none|
|summary|string¦null|false|none|none|

<h2 id="tocS_AscentParticipation">AscentParticipation</h2>
<!-- backwards compatibility -->
<a id="schemaascentparticipation"></a>
<a id="schema_AscentParticipation"></a>
<a id="tocSascentparticipation"></a>
<a id="tocsascentparticipation"></a>

```json
{
  "id": 0,
  "user": "string",
  "is_successful": true,
  "incident_type": "INJ",
  "incident_details": "string",
  "ascent": 0
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|id|integer|true|read-only|none|
|user|string|true|read-only|none|
|is_successful|boolean|false|none|none|
|incident_type|any|false|none|none|

oneOf

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|[IncidentTypeEnum](#schemaincidenttypeenum)|false|none|* `INJ` - Injured<br>* `MIS` - Missing<br>* `FAT` - Fatality|

xor

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|[BlankEnum](#schemablankenum)|false|none|none|

xor

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|[NullEnum](#schemanullenum)|false|none|none|

continued

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|incident_details|string¦null|false|none|none|
|ascent|integer|true|read-only|none|

<h2 id="tocS_BlankEnum">BlankEnum</h2>
<!-- backwards compatibility -->
<a id="schemablankenum"></a>
<a id="schema_BlankEnum"></a>
<a id="tocSblankenum"></a>
<a id="tocsblankenum"></a>

```json
""

```

### Properties

*None*

<h2 id="tocS_City">City</h2>
<!-- backwards compatibility -->
<a id="schemacity"></a>
<a id="schema_City"></a>
<a id="tocScity"></a>
<a id="tocscity"></a>

```json
{
  "id": 0,
  "name": "string",
  "country": 0
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|id|integer|true|read-only|none|
|name|string|true|none|none|
|country|integer¦null|true|none|none|

<h2 id="tocS_CityDetail">CityDetail</h2>
<!-- backwards compatibility -->
<a id="schemacitydetail"></a>
<a id="schema_CityDetail"></a>
<a id="tocScitydetail"></a>
<a id="tocscitydetail"></a>

```json
{
  "id": 0,
  "name": "string",
  "country": {
    "id": 0,
    "name": "string"
  }
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|id|integer|true|read-only|none|
|name|string|true|none|none|
|country|[Country](#schemacountry)|true|read-only|none|

<h2 id="tocS_Club">Club</h2>
<!-- backwards compatibility -->
<a id="schemaclub"></a>
<a id="schema_Club"></a>
<a id="tocSclub"></a>
<a id="tocsclub"></a>

```json
{
  "id": 0,
  "name": "string",
  "country": 0,
  "city": 0,
  "contact_user": 0
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|id|integer|true|read-only|none|
|name|string|true|none|none|
|country|integer¦null|false|none|none|
|city|integer¦null|false|none|none|
|contact_user|integer¦null|false|none|none|

<h2 id="tocS_ClubDetail">ClubDetail</h2>
<!-- backwards compatibility -->
<a id="schemaclubdetail"></a>
<a id="schema_ClubDetail"></a>
<a id="tocSclubdetail"></a>
<a id="tocsclubdetail"></a>

```json
{
  "id": 0,
  "members": [
    {
      "id": 0,
      "join_datetime": "2019-08-24T14:15:22Z",
      "leave_datetime": "2019-08-24T14:15:22Z",
      "user": 0,
      "club": 0
    }
  ],
  "country": {
    "id": 0,
    "name": "string"
  },
  "city": {
    "id": 0,
    "name": "string",
    "country": 0
  },
  "name": "string",
  "contact_user": 0
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|id|integer|true|read-only|none|
|members|[[ClubMembership](#schemaclubmembership)]|true|read-only|none|
|country|[Country](#schemacountry)|true|read-only|none|
|city|[City](#schemacity)|true|read-only|none|
|name|string|true|none|none|
|contact_user|integer¦null|false|none|none|

<h2 id="tocS_ClubMembership">ClubMembership</h2>
<!-- backwards compatibility -->
<a id="schemaclubmembership"></a>
<a id="schema_ClubMembership"></a>
<a id="tocSclubmembership"></a>
<a id="tocsclubmembership"></a>

```json
{
  "id": 0,
  "join_datetime": "2019-08-24T14:15:22Z",
  "leave_datetime": "2019-08-24T14:15:22Z",
  "user": 0,
  "club": 0
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|id|integer|true|read-only|none|
|join_datetime|string(date-time)|false|none|none|
|leave_datetime|string(date-time)¦null|false|none|none|
|user|integer|true|read-only|none|
|club|integer|true|read-only|none|

<h2 id="tocS_Country">Country</h2>
<!-- backwards compatibility -->
<a id="schemacountry"></a>
<a id="schema_Country"></a>
<a id="tocScountry"></a>
<a id="tocscountry"></a>

```json
{
  "id": 0,
  "name": "string"
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|id|integer|true|read-only|none|
|name|string|true|none|none|

<h2 id="tocS_CountryDetail">CountryDetail</h2>
<!-- backwards compatibility -->
<a id="schemacountrydetail"></a>
<a id="schema_CountryDetail"></a>
<a id="tocScountrydetail"></a>
<a id="tocscountrydetail"></a>

```json
{
  "id": 0,
  "name": "string",
  "cities": [
    "string"
  ],
  "clubs": [
    "string"
  ],
  "mountains": [
    "string"
  ]
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|id|integer|true|read-only|none|
|name|string|true|none|none|
|cities|[string]|true|read-only|none|
|clubs|[string]|true|read-only|none|
|mountains|[string]|true|read-only|none|

<h2 id="tocS_IncidentTypeEnum">IncidentTypeEnum</h2>
<!-- backwards compatibility -->
<a id="schemaincidenttypeenum"></a>
<a id="schema_IncidentTypeEnum"></a>
<a id="tocSincidenttypeenum"></a>
<a id="tocsincidenttypeenum"></a>

```json
"INJ"

```

* `INJ` - Injured
* `MIS` - Missing
* `FAT` - Fatality

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|*anonymous*|string|false|none|* `INJ` - Injured<br>* `MIS` - Missing<br>* `FAT` - Fatality|

#### Enumerated Values

|Property|Value|
|---|---|
|*anonymous*|INJ|
|*anonymous*|MIS|
|*anonymous*|FAT|

<h2 id="tocS_Mountain">Mountain</h2>
<!-- backwards compatibility -->
<a id="schemamountain"></a>
<a id="schema_Mountain"></a>
<a id="tocSmountain"></a>
<a id="tocsmountain"></a>

```json
{
  "id": 0,
  "name": "string",
  "elevation": 32767,
  "region": "string",
  "country": 0
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|id|integer|true|read-only|none|
|name|string|true|none|none|
|elevation|integer|true|none|none|
|region|string¦null|false|none|none|
|country|integer|true|none|none|

<h2 id="tocS_MountainDetail">MountainDetail</h2>
<!-- backwards compatibility -->
<a id="schemamountaindetail"></a>
<a id="schema_MountainDetail"></a>
<a id="tocSmountaindetail"></a>
<a id="tocsmountaindetail"></a>

```json
{
  "id": 0,
  "name": "string",
  "elevation": 32767,
  "region": "string",
  "country": {
    "id": 0,
    "name": "string"
  },
  "routes": [
    {
      "id": 0,
      "name": "string",
      "description": "string",
      "duration_days": 32767,
      "mountain": 0
    }
  ]
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|id|integer|true|read-only|none|
|name|string|true|none|none|
|elevation|integer|true|none|none|
|region|string¦null|false|none|none|
|country|[Country](#schemacountry)|true|read-only|none|
|routes|[[Route](#schemaroute)]|true|read-only|none|

<h2 id="tocS_MyAscentParticipation">MyAscentParticipation</h2>
<!-- backwards compatibility -->
<a id="schemamyascentparticipation"></a>
<a id="schema_MyAscentParticipation"></a>
<a id="tocSmyascentparticipation"></a>
<a id="tocsmyascentparticipation"></a>

```json
{
  "id": 0,
  "user": "string",
  "ascent": {
    "id": 0,
    "route": {
      "id": 0,
      "name": "string",
      "description": "string",
      "duration_days": 32767,
      "mountain": 0
    },
    "mountain": {
      "id": 0,
      "name": "string",
      "elevation": 32767,
      "region": "string",
      "country": 0
    },
    "participants": [
      {
        "id": 0,
        "user": "string",
        "is_successful": true,
        "incident_type": "INJ",
        "incident_details": "string",
        "ascent": 0
      }
    ],
    "planned_start_datetime": "2019-08-24T14:15:22Z",
    "planned_end_datetime": "2019-08-24T14:15:22Z",
    "actual_start_datetime": "2019-08-24T14:15:22Z",
    "actual_end_datetime": "2019-08-24T14:15:22Z",
    "is_successful": true,
    "summary": "string"
  },
  "is_successful": true,
  "incident_type": "INJ",
  "incident_details": "string"
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|id|integer|true|read-only|none|
|user|string|true|read-only|none|
|ascent|[AscentDetail](#schemaascentdetail)|true|read-only|none|
|is_successful|boolean|false|none|none|
|incident_type|any|false|none|none|

oneOf

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|[IncidentTypeEnum](#schemaincidenttypeenum)|false|none|* `INJ` - Injured<br>* `MIS` - Missing<br>* `FAT` - Fatality|

xor

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|[BlankEnum](#schemablankenum)|false|none|none|

xor

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|[NullEnum](#schemanullenum)|false|none|none|

continued

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|incident_details|string¦null|false|none|none|

<h2 id="tocS_MyClubMemberShip">MyClubMemberShip</h2>
<!-- backwards compatibility -->
<a id="schemamyclubmembership"></a>
<a id="schema_MyClubMemberShip"></a>
<a id="tocSmyclubmembership"></a>
<a id="tocsmyclubmembership"></a>

```json
{
  "id": 0,
  "club": {
    "id": 0,
    "name": "string",
    "country": 0,
    "city": 0,
    "contact_user": 0
  },
  "join_datetime": "2019-08-24T14:15:22Z",
  "leave_datetime": "2019-08-24T14:15:22Z",
  "user": 0
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|id|integer|true|read-only|none|
|club|[Club](#schemaclub)|true|read-only|none|
|join_datetime|string(date-time)|false|none|none|
|leave_datetime|string(date-time)¦null|false|none|none|
|user|integer|true|read-only|none|

<h2 id="tocS_NullEnum">NullEnum</h2>
<!-- backwards compatibility -->
<a id="schemanullenum"></a>
<a id="schema_NullEnum"></a>
<a id="tocSnullenum"></a>
<a id="tocsnullenum"></a>

```json
null

```

### Properties

*None*

<h2 id="tocS_PasswordResetConfirm">PasswordResetConfirm</h2>
<!-- backwards compatibility -->
<a id="schemapasswordresetconfirm"></a>
<a id="schema_PasswordResetConfirm"></a>
<a id="tocSpasswordresetconfirm"></a>
<a id="tocspasswordresetconfirm"></a>

```json
{
  "uid": "string",
  "token": "string",
  "new_password": "string"
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|uid|string|true|none|none|
|token|string|true|none|none|
|new_password|string|true|none|none|

<h2 id="tocS_PatchedAscent">PatchedAscent</h2>
<!-- backwards compatibility -->
<a id="schemapatchedascent"></a>
<a id="schema_PatchedAscent"></a>
<a id="tocSpatchedascent"></a>
<a id="tocspatchedascent"></a>

```json
{
  "id": 0,
  "planned_start_datetime": "2019-08-24T14:15:22Z",
  "planned_end_datetime": "2019-08-24T14:15:22Z",
  "actual_start_datetime": "2019-08-24T14:15:22Z",
  "actual_end_datetime": "2019-08-24T14:15:22Z",
  "is_successful": true,
  "summary": "string",
  "route": 0
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|id|integer|false|read-only|none|
|planned_start_datetime|string(date-time)|false|none|none|
|planned_end_datetime|string(date-time)|false|none|none|
|actual_start_datetime|string(date-time)¦null|false|none|none|
|actual_end_datetime|string(date-time)¦null|false|none|none|
|is_successful|boolean|false|none|none|
|summary|string¦null|false|none|none|
|route|integer|false|none|none|

<h2 id="tocS_PatchedAscentParticipation">PatchedAscentParticipation</h2>
<!-- backwards compatibility -->
<a id="schemapatchedascentparticipation"></a>
<a id="schema_PatchedAscentParticipation"></a>
<a id="tocSpatchedascentparticipation"></a>
<a id="tocspatchedascentparticipation"></a>

```json
{
  "id": 0,
  "user": "string",
  "is_successful": true,
  "incident_type": "INJ",
  "incident_details": "string",
  "ascent": 0
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|id|integer|false|read-only|none|
|user|string|false|read-only|none|
|is_successful|boolean|false|none|none|
|incident_type|any|false|none|none|

oneOf

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|[IncidentTypeEnum](#schemaincidenttypeenum)|false|none|* `INJ` - Injured<br>* `MIS` - Missing<br>* `FAT` - Fatality|

xor

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|[BlankEnum](#schemablankenum)|false|none|none|

xor

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|[NullEnum](#schemanullenum)|false|none|none|

continued

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|incident_details|string¦null|false|none|none|
|ascent|integer|false|read-only|none|

<h2 id="tocS_PatchedCity">PatchedCity</h2>
<!-- backwards compatibility -->
<a id="schemapatchedcity"></a>
<a id="schema_PatchedCity"></a>
<a id="tocSpatchedcity"></a>
<a id="tocspatchedcity"></a>

```json
{
  "id": 0,
  "name": "string",
  "country": 0
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|id|integer|false|read-only|none|
|name|string|false|none|none|
|country|integer¦null|false|none|none|

<h2 id="tocS_PatchedClub">PatchedClub</h2>
<!-- backwards compatibility -->
<a id="schemapatchedclub"></a>
<a id="schema_PatchedClub"></a>
<a id="tocSpatchedclub"></a>
<a id="tocspatchedclub"></a>

```json
{
  "id": 0,
  "name": "string",
  "country": 0,
  "city": 0,
  "contact_user": 0
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|id|integer|false|read-only|none|
|name|string|false|none|none|
|country|integer¦null|false|none|none|
|city|integer¦null|false|none|none|
|contact_user|integer¦null|false|none|none|

<h2 id="tocS_PatchedClubMembership">PatchedClubMembership</h2>
<!-- backwards compatibility -->
<a id="schemapatchedclubmembership"></a>
<a id="schema_PatchedClubMembership"></a>
<a id="tocSpatchedclubmembership"></a>
<a id="tocspatchedclubmembership"></a>

```json
{
  "id": 0,
  "join_datetime": "2019-08-24T14:15:22Z",
  "leave_datetime": "2019-08-24T14:15:22Z",
  "user": 0,
  "club": 0
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|id|integer|false|read-only|none|
|join_datetime|string(date-time)|false|none|none|
|leave_datetime|string(date-time)¦null|false|none|none|
|user|integer|false|read-only|none|
|club|integer|false|read-only|none|

<h2 id="tocS_PatchedCountryDetail">PatchedCountryDetail</h2>
<!-- backwards compatibility -->
<a id="schemapatchedcountrydetail"></a>
<a id="schema_PatchedCountryDetail"></a>
<a id="tocSpatchedcountrydetail"></a>
<a id="tocspatchedcountrydetail"></a>

```json
{
  "id": 0,
  "name": "string",
  "cities": [
    "string"
  ],
  "clubs": [
    "string"
  ],
  "mountains": [
    "string"
  ]
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|id|integer|false|read-only|none|
|name|string|false|none|none|
|cities|[string]|false|read-only|none|
|clubs|[string]|false|read-only|none|
|mountains|[string]|false|read-only|none|

<h2 id="tocS_PatchedMountain">PatchedMountain</h2>
<!-- backwards compatibility -->
<a id="schemapatchedmountain"></a>
<a id="schema_PatchedMountain"></a>
<a id="tocSpatchedmountain"></a>
<a id="tocspatchedmountain"></a>

```json
{
  "id": 0,
  "name": "string",
  "elevation": 32767,
  "region": "string",
  "country": 0
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|id|integer|false|read-only|none|
|name|string|false|none|none|
|elevation|integer|false|none|none|
|region|string¦null|false|none|none|
|country|integer|false|none|none|

<h2 id="tocS_PatchedRoute">PatchedRoute</h2>
<!-- backwards compatibility -->
<a id="schemapatchedroute"></a>
<a id="schema_PatchedRoute"></a>
<a id="tocSpatchedroute"></a>
<a id="tocspatchedroute"></a>

```json
{
  "id": 0,
  "name": "string",
  "description": "string",
  "duration_days": 32767,
  "mountain": 0
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|id|integer|false|read-only|none|
|name|string|false|none|none|
|description|string¦null|false|none|none|
|duration_days|integer¦null|false|none|none|
|mountain|integer¦null|false|none|none|

<h2 id="tocS_PatchedUser">PatchedUser</h2>
<!-- backwards compatibility -->
<a id="schemapatcheduser"></a>
<a id="schema_PatchedUser"></a>
<a id="tocSpatcheduser"></a>
<a id="tocspatcheduser"></a>

```json
{
  "id": 0,
  "username": "string",
  "first_name": "string",
  "last_name": "string",
  "email": "user@example.com",
  "is_superuser": true,
  "is_staff": true,
  "phone_number": "string",
  "city": 0,
  "club": {
    "id": 0,
    "name": "string",
    "country": 0,
    "city": 0,
    "contact_user": 0
  }
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|id|integer|false|read-only|none|
|username|string|false|none|Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.|
|first_name|string|false|none|none|
|last_name|string|false|none|none|
|email|string(email)|false|none|none|
|is_superuser|boolean|false|none|Designates that this user has all permissions without explicitly assigning them.|
|is_staff|boolean|false|none|Designates whether the user can log into this admin site.|
|phone_number|string¦null|false|none|none|
|city|integer¦null|false|none|none|
|club|[Club](#schemaclub)|false|read-only|none|

<h2 id="tocS_Route">Route</h2>
<!-- backwards compatibility -->
<a id="schemaroute"></a>
<a id="schema_Route"></a>
<a id="tocSroute"></a>
<a id="tocsroute"></a>

```json
{
  "id": 0,
  "name": "string",
  "description": "string",
  "duration_days": 32767,
  "mountain": 0
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|id|integer|true|read-only|none|
|name|string|true|none|none|
|description|string¦null|false|none|none|
|duration_days|integer¦null|false|none|none|
|mountain|integer¦null|false|none|none|

<h2 id="tocS_RouteDetail">RouteDetail</h2>
<!-- backwards compatibility -->
<a id="schemaroutedetail"></a>
<a id="schema_RouteDetail"></a>
<a id="tocSroutedetail"></a>
<a id="tocsroutedetail"></a>

```json
{
  "id": 0,
  "name": "string",
  "description": "string",
  "duration_days": 32767,
  "mountain": {
    "id": 0,
    "name": "string",
    "elevation": 32767,
    "region": "string",
    "country": 0
  },
  "ascents": [
    {
      "id": 0,
      "planned_start_datetime": "2019-08-24T14:15:22Z",
      "planned_end_datetime": "2019-08-24T14:15:22Z",
      "actual_start_datetime": "2019-08-24T14:15:22Z",
      "actual_end_datetime": "2019-08-24T14:15:22Z",
      "is_successful": true,
      "summary": "string",
      "route": 0
    }
  ]
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|id|integer|true|read-only|none|
|name|string|true|none|none|
|description|string¦null|false|none|none|
|duration_days|integer¦null|false|none|none|
|mountain|[Mountain](#schemamountain)|true|read-only|none|
|ascents|[[Ascent](#schemaascent)]|true|read-only|none|

<h2 id="tocS_SendEmailReset">SendEmailReset</h2>
<!-- backwards compatibility -->
<a id="schemasendemailreset"></a>
<a id="schema_SendEmailReset"></a>
<a id="tocSsendemailreset"></a>
<a id="tocssendemailreset"></a>

```json
{
  "email": "user@example.com"
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|email|string(email)|true|none|none|

<h2 id="tocS_SetPassword">SetPassword</h2>
<!-- backwards compatibility -->
<a id="schemasetpassword"></a>
<a id="schema_SetPassword"></a>
<a id="tocSsetpassword"></a>
<a id="tocssetpassword"></a>

```json
{
  "new_password": "string",
  "current_password": "string"
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|new_password|string|true|none|none|
|current_password|string|true|none|none|

<h2 id="tocS_SetUsername">SetUsername</h2>
<!-- backwards compatibility -->
<a id="schemasetusername"></a>
<a id="schema_SetUsername"></a>
<a id="tocSsetusername"></a>
<a id="tocssetusername"></a>

```json
{
  "current_password": "string",
  "new_username": "string"
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|current_password|string|true|none|none|
|new_username|string|true|none|Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.|

<h2 id="tocS_TokenCreate">TokenCreate</h2>
<!-- backwards compatibility -->
<a id="schematokencreate"></a>
<a id="schema_TokenCreate"></a>
<a id="tocStokencreate"></a>
<a id="tocstokencreate"></a>

```json
{
  "password": "string",
  "username": "string"
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|password|string|false|none|none|
|username|string|false|none|none|

<h2 id="tocS_User">User</h2>
<!-- backwards compatibility -->
<a id="schemauser"></a>
<a id="schema_User"></a>
<a id="tocSuser"></a>
<a id="tocsuser"></a>

```json
{
  "id": 0,
  "username": "string",
  "first_name": "string",
  "last_name": "string",
  "email": "user@example.com",
  "is_superuser": true,
  "is_staff": true,
  "phone_number": "string",
  "city": 0,
  "club": {
    "id": 0,
    "name": "string",
    "country": 0,
    "city": 0,
    "contact_user": 0
  }
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|id|integer|true|read-only|none|
|username|string|true|none|Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.|
|first_name|string|true|none|none|
|last_name|string|true|none|none|
|email|string(email)|true|none|none|
|is_superuser|boolean|false|none|Designates that this user has all permissions without explicitly assigning them.|
|is_staff|boolean|false|none|Designates whether the user can log into this admin site.|
|phone_number|string¦null|false|none|none|
|city|integer¦null|false|none|none|
|club|[Club](#schemaclub)|true|read-only|none|

<h2 id="tocS_UserCreate">UserCreate</h2>
<!-- backwards compatibility -->
<a id="schemausercreate"></a>
<a id="schema_UserCreate"></a>
<a id="tocSusercreate"></a>
<a id="tocsusercreate"></a>

```json
{
  "username": "string",
  "password": "string",
  "first_name": "string",
  "last_name": "string",
  "email": "user@example.com",
  "phone_number": "string",
  "city": 0
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|username|string|true|none|Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.|
|password|string|true|none|none|
|first_name|string|true|none|none|
|last_name|string|true|none|none|
|email|string(email)|true|none|none|
|phone_number|string¦null|false|none|none|
|city|integer¦null|false|none|none|

<h2 id="tocS_UsernameResetConfirm">UsernameResetConfirm</h2>
<!-- backwards compatibility -->
<a id="schemausernameresetconfirm"></a>
<a id="schema_UsernameResetConfirm"></a>
<a id="tocSusernameresetconfirm"></a>
<a id="tocsusernameresetconfirm"></a>

```json
{
  "new_username": "string"
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|new_username|string|true|none|Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.|

