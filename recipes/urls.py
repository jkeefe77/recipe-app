from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import welcome_view, RecipeListView, RecipeDetailView, records_view, create_view, about_view

app_name = 'recipes'

urlpatterns = [
    path('', welcome_view, name='welcome'),
    path('welcome/', welcome_view, name='welcome'),
    path('list/', RecipeListView.as_view(), name='list'),
    path('detail/<pk>', RecipeDetailView.as_view(), name='detail'),
    path('records/', records_view, name='records'),
    path('create/', create_view, name='create'),
    path('about/', about_view, name='about'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)