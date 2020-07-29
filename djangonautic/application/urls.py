from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.activity_log, name='activity-log'),
    path('player-database/', views.player_database, name='player-database'),
    path('afcon/', views.afcon, name='afcon'),
    path('caf/', views.caf, name='caf'),
    path('profile/', views.profile_view, name='profile'),
    path('blank/', views.blank_view, name='blank')
]