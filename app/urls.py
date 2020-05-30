from app.views import homepage, ajax_request
from django.urls import path
urlpatterns = [
    path('', homepage, name="homepage"),
    path('get_rate', ajax_request, name="rate"),
]
