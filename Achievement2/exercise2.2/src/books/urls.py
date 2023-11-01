from django.urls import path
from .views import BookListView
from .views import BookDetailView

app_name = "books"

urlpatterns = [
    path("", BookListView.as_view(), name="list"),
    path('list/<pk>', BookDetailView.as_view(), name='detail')
]
