from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.new_raid, name='new_raid'),
    path('<int:raid_id>/', views.get_raid, name='raid'),
    path('<int:raid_id>/complete/', views.complete_raid, name='complete'),
    path('<int:raid_id>/pause/', views.pause_raid, name='pause'),
    path('<int:raid_id>/fail/', views.fail_raid, name='fail'),
    path('<int:raid_id>/give/', views.give_item, name='give_item'),
    path('<int:raid_id>/delete/<int:loot_id>/', views.delete_loot, name='delete_loot'),
    path('<int:raid_id>/remove/<int:raider_id>/', views.remove_raider, name='remove_raider'),
]