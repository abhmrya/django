# from django.urls import path
# from .views import EmployeeAPIView




# urlpatterns = [
#     path("employees/", EmployeeAPIView.as_view()),
#     path("employees/<int:id>", EmployeeAPIView.as_view()),
# ]




# from django.urls import path
# from .views import EmployeeListCreateAPI, EmployeeDetailAPI

# urlpatterns = [
#     path("employees/", EmployeeListCreateAPI.as_view()),
#     path("employees/<int:id>/", EmployeeDetailAPI.as_view()),
# ]



from django.urls import path

from .views import (
    EmployeeListCreateAPIView,
    EmployeeDetailAPIView,
)

urlpatterns = [

    path(
        "employees/",
        EmployeeListCreateAPIView.as_view()
    ),

    path(
        "employees/<int:id>/",
        EmployeeDetailAPIView.as_view()
    ),

]