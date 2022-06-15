from django.urls import path

from .views import (
    savollar,
    savol_detail,
    check_answer,
    create_question,
    create_group,
    groups,
    remove_group,
    edit_group,
    create_choice
)

app_name = 'poll'
urlpatterns = [
    path('', savollar, name="savollar"),
    path('savol/<int:id>/', savol_detail, name="savol"),
    path('check/<int:variant_id>/', check_answer, name="check_answer"),
    path('create-question/', create_question, name="create"),
    path('create-proup/', create_group, name="create_group"),
    path('groups/', groups, name="groups"),
    path('remove-group/<int:id>/', remove_group, name="remove_group"),
    path('edti-group/<int:id>/', edit_group, name="edit_group"),
    path('tanlov-yaratish/', create_choice, name="tanlov_yaratish")
]
