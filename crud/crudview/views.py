# -------------------------------------------
#                  APIView
# ---------------------------------------------

# 
#  from django.shortcuts import render
# from rest_framework.views import APIView
# from .serializers import EmployeeSerializer
# from rest_framework.response import Response
# from rest_framework  import status
# from .models import Employee
# # Create your views here.

# class EmployeeAPIView(APIView):

#     # create Employee
#     def post(self,request):
#         serializer = EmployeeSerializer(data=request.data)

#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_201_CREATED)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
#     # Get All The Employee
#     def get(self,request,id=None):
#         if id is not None:
#             employees = Employee.objects.get(id = id)
#             serializer = EmployeeSerializer(employees)
#             return Response(serializer.data)
        
#         employees = Employee.objects.all()
#         serializer = EmployeeSerializer(employees,many=True)
#         return  Response(serializer.data)
    
#     #  Update the data
#     def put(self,request,id):
#         employee = Employee.objects.get(id=id)
#         print(employee)
#         serializer = EmployeeSerializer(employee,data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
        
#     def patch(self,request,id):
#         employee = Employee.objects.get(id = id)
#         print(employee)
#         serializer = EmployeeSerializer(employee,data = request.data,partial=True)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response(serializer.data)
    
#     def delete(self,request,id):
#         employee = Employee.objects.get(id =id)
#         print(employee)
#         # serializer = EmployeeSerializer(employee,request.data)
#         # serializer.delete()
#         employee.delete()
#         return Response({'message':'successfully delete'})

#  dono same hi hai

# from django.shortcuts import get_object_or_404

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status

# from .models import Employee
# from .serializers import EmployeeSerializer


# class EmployeeAPIView(APIView):

#     # Create Employee
#     def post(self, request):
#         serializer = EmployeeSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(
#                 serializer.data,
#                 status=status.HTTP_201_CREATED
#             )
#         return Response(
#             serializer.errors,
#             status=status.HTTP_400_BAD_REQUEST
#         )

#     # Get All Employee / Get Single Employee
#     def get(self, request, id=None):
#         if id is not None:
#             employee = get_object_or_404(Employee, id=id)
#             serializer = EmployeeSerializer(employee)
#             return Response(serializer.data)
        
#         employees = Employee.objects.all()
#         serializer = EmployeeSerializer(
#             employees,
#             many=True
#         )
#         return Response(serializer.data)

#     # Full Update
#     def put(self, request, id):
#         employee = get_object_or_404(Employee, id=id)

#         serializer = EmployeeSerializer(employee,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)

#         return Response(
#             serializer.errors,
#             status=status.HTTP_400_BAD_REQUEST
#         )

#     # Partial Update
#     def patch(self, request, id):
#         employee = get_object_or_404(Employee, id=id)
#         serializer = EmployeeSerializer(
#             employee,
#             data=request.data,
#             partial=True
#         )

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)

#         return Response(
#             serializer.errors,
#             status=status.HTTP_400_BAD_REQUEST
#         )

#     # Delete Employee
#     def delete(self, request, id):
#         employee = get_object_or_404(Employee, id=id)
#         employee.delete()
#         return Response(
#             {
#                 "message": "Employee deleted successfully."
#             },
#             status=status.HTTP_204_NO_CONTENT
#         )
    
#-------------------------------------------
                # End APIView
# ---------------------------------------------


#-------------------------------------------
#                    Generic
# ---------------------------------------------
# from rest_framework import generics, mixins

# from .models import Employee
# from .serializers import EmployeeSerializer


# class EmployeeListCreateAPI(
#     generics.GenericAPIView,
#     mixins.ListModelMixin,
#     mixins.CreateModelMixin
# ):

#     queryset = Employee.objects.all()
#     serializer_class = EmployeeSerializer

#     def get(self, request):
#         return self.list(request)

#     def post(self, request):
#         return self.create(request)
    
# class EmployeeDetailAPI(
#     generics.GenericAPIView,
#     mixins.RetrieveModelMixin,
#     mixins.UpdateModelMixin,
#     mixins.DestroyModelMixin
# ):

#     queryset = Employee.objects.all()
#     serializer_class = EmployeeSerializer
#     lookup_field = "id"

#     def get(self, request, id):
#         return self.retrieve(request, id=id)

#     def put(self, request, id):
#         return self.update(request, id=id)

#     def patch(self, request, id):
#         return self.partial_update(request, id=id)

#     def delete(self, request, id):
#         return self.destroy(request, id=id)


#---------------------------------------
#                 GeericView
#-----------------------------------------
from rest_framework import generics

from .models import Employee
from .serializers import EmployeeSerializer


class EmployeeListCreateAPIView(generics.ListCreateAPIView):

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class EmployeeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    lookup_field = "id"