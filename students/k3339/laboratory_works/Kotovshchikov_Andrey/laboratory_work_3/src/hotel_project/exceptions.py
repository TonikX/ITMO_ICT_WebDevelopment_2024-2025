from rest_framework.exceptions import APIException


class BadRequest(APIException):
    status_code = 400
    default_detail = "Bad request params"
    default_code = "bad_request"


class Conflict(APIException):
    status_code = 409
    default_detail = "Conflict request params"
    default_code = "conflict"
