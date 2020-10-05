from django.urls import path
from . import views

urlpatterns = [
    path("", views.update_detail_view),
    path("cbv", views.UpdateView.as_view()),
    path("mixin", views.UpdateView_with_mixin.as_view()),
    path("serialize", views.SerializedDetailView.as_view()),
    path("serialize/list", views.SerializedListView.as_view()),
]
