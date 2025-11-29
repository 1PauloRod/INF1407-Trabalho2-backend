from django.urls import path 
from .views import LivroListView

urlpatterns = [
    path("", LivroListView.as_view())
]
