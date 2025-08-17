from django.urls import path, include

urlpatterns = [
    path('app/', include('src.app.urls')),
    path('users/', include('src.users.urls')),
]