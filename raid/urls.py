from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.new_raid, name='new_raid'),
    path('<int:raid_id>/', views.get_raid, name='raid'),
]