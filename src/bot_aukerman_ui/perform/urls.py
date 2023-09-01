from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),

    path("add_character", views.add_character, name="add_character"),
    path("delete_character/<int:character_id>",
         views.delete_character,
         name="delete_character"),

    path("start_performance", views.start_performance, name="start_performance"),
    # path("stop_performance", views.stop_performance, name="stop_performance"),
    path("get_performance_status",
         views.get_performance_status,
         name="get_performance_status"),

    path("toggle_microphone", views.toggle_microphone, name="toggle_microphone"),
]
