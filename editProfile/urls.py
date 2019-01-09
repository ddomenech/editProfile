"""editProfile URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from extupf.views import UserViewSet, UserProfileViewSet, GetUserProfileView
from django.urls import path, include
from rest_framework.documentation import  include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token 

router = DefaultRouter()
router.register(r'users',UserViewSet)
router.register(r'profile', UserProfileViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    #path('upload/<str:filename>/', CargarArchivoView.as_view(), name="upload"),
    path('api/v1/api-token-auth/', obtain_jwt_token),
    path('api/v1/api-token-refresh/', refresh_jwt_token),
    path('api/v1/api-auth/',include('rest_framework.urls')),
    path('api/v1/docs', include_docs_urls(title='Mi Api')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
