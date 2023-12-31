from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("settings", views.settings, name="settings"),

    # Characters
    path("add_character", views.add_character, name="add_character"),

    path("delete_character/<int:character_id>",
         views.delete_character,
         name="delete_character"),

    # Performances
    path("performance/<int:performance_id>",
            views.performance,
            name="performance"),

    path("create_performance",
         views.create_performance,
         name="create_performance"),

    path("delete_performance/<int:performance_id>",
            views.delete_performance,
            name="delete_performance"),

    path("start_performance/<int:performance_id>",
            views.start_performance,
            name="start_performance"),

    path("stop_performance/<int:performance_id>",
         views.stop_performance,
         name="stop_performance"),

    path("get_script/<int:performance_id>",
            views.get_script,
            name="get_script"),

    path("edit_script/<int:performance_id>",
            views.edit_script,
            name="edit_script"),

    path("get_performance_status",
         views.get_performance_status,
         name="get_performance_status"),

    # Performance Controls
    path("generate_dialogue/<int:performance_id>",
            views.generate_dialogue,
            name="generate_dialogue"),

    path("interrupt/<int:performance_id>",
            views.interrupt,
            name="interrupt"),

    path("toggle_microphone",
         views.toggle_microphone,
         name="toggle_microphone"),
]
