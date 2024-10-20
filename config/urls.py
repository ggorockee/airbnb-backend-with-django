from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from drf_yasg.generators import OpenAPISchemaGenerator

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from .views import HelathCheck

class BothHttpAndHttpsSchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        schema.schemes = ["http", "https"]
        return schema



schema_view = get_schema_view(
    openapi.Info(
        title="Airbnb API by ggorockee",
        default_version="v1.0.0",
        description="Airbnb API by ggorockee",
        # terms_of_service="https://www.google.com/policies/terms/",
        # contact=openapi.Contact(name="test", email="test@test.com"),
        # license=openapi.License(name="Test License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    generator_class=BothHttpAndHttpsSchemaGenerator,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("healthz/ready", HelathCheck.as_view()),
    # path("api/v1/categories/", include("categories.urls")),
    # path("api/v1/rooms/", include("rooms.urls")),
    # path("api/v1/experiences/", include("experiences.urls")),
    # path("api/v1/medias/", include("medias.urls")),
    # path("api/v1/wishlists/", include("wishlists.urls")),
    path("api/v1/users/", include("users.urls")),
]

if settings.DEBUG:
    urlpatterns += [
        # other user API end-point URL
        re_path(
            r"^docs(?P<format>\.json|\.yaml)$",
            schema_view.without_ui(cache_timeout=0),
            name="schema-json",
        ),
        re_path(
            r"^docs/$",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
        re_path(
            r"^redoc/$",
            schema_view.with_ui("redoc", cache_timeout=0),
            name="schema-redoc",
        ),
    ]