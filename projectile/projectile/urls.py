"""
URL configuration for projectile project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path, include

from rest_framework import permissions

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

schema_view = get_schema_view(
    openapi.Info(
        title="AiTools",
        default_version="main",
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # Swagger
    re_path(
        r"^docs/swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=10),
        name="schema-json",
    ),
    re_path(
        r"^docs/swagger$",
        schema_view.with_ui("swagger", cache_timeout=10),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^docs/redoc$",
        schema_view.with_ui("redoc", cache_timeout=10),
        name="schema-redoc",
    ),
     # JWT Token
    path(
        "api/v1/token",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "api/v1/token/refresh",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path(
        "api/v1/token/verify",
        TokenVerifyView.as_view(),
        name="token_verify",
    ),
    path("api/v1/public", include("publicapi.rest.urls")),
    path("api/v1", include("core.rest.urls.users")),
    path("api/v1/we", include("weapi.rest.urls")),
    path("api/v1/me", include("meapi.rest.urls")),
    path("api/v1/posts", include("contentio.rest.urls")),
    path("api/v1/storage", include("meapi.rest.urls.storage")),
    path("adminium/", admin.site.urls),
    path("api/v1/sponsors", include("contentio.rest.urls.sponsors")),
    path("api/v1/faqs", include("contentio.rest.urls.faq")),
    # # social auth
    # path("auth/", include("drf_social_oauth2.urls")),
    # path("social/", include("social_django.urls")),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
