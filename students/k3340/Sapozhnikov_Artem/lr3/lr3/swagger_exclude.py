from drf_spectacular.utils import extend_schema
from rest_framework.authtoken.views import ObtainAuthToken

ObtainAuthToken.schema = extend_schema(exclude=True)(ObtainAuthToken).schema
