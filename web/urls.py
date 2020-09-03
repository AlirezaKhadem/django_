from django.urls import path
from . import views

urlpatterns = [
    path("submit/expense/", views.submit_expense),
    path("submit/income/", views.submit_income),
    path("account/register/", views.register),
]
