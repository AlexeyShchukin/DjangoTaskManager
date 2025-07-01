from django.urls import path, include

urlpatterns = [
    path('app/', include('src.app.urls')),
]