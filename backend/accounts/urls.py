from django.urls import path
from .views import CreateCustomerView, CreateEmployeeView

urlpatterns = [
    path("register/", CreateCustomerView.as_view(), name="register"),
    path("employees/", CreateEmployeeView.as_view(), name="create-employee"),
]