from django.shortcuts import render

from . import models

from . import serializers

from rest_framework.generics import ListAPIView,RetrieveAPIView

from rest_framework import generics, permissions,viewsets,pagination

from rest_framework.views import APIView

from django.db.models import Avg

from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken

from django.core.exceptions import PermissionDenied

# Create your views here.


# below vendorregisterview is view for vendorregister
class VendorRegisterView(generics.CreateAPIView):
    queryset = models.Vendor.objects.all()
    serializer_class = serializers.VendorSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        response_data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return Response(response_data)
    
# below view is for vendor login    


class VendorLoginView(generics.CreateAPIView):
    serializer_class = serializers.VendorLoginSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')
        user = models.Vendor.objects.filter(username=username).first()
        if user is None or not user.check_password(password):
            return Response({'detail': 'Invalid credentials'}, status=400)
        refresh = RefreshToken.for_user(user)
        response_data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return Response(response_data)
    
# below view is for customer register

class CustomerRegisterView(generics.CreateAPIView):
    queryset = models.Vendor.objects.all()
    serializer_class = serializers.CustomerSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        response_data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return Response(response_data)

 # below view is for customer login 
class CustomerLoginView(generics.CreateAPIView):
    serializer_class = serializers.CustomerLoginSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')
        user = models.Customer.objects.filter(username=username).first()
        if user is None or not user.check_password(password):
            return Response({'detail': 'Invalid credentials'}, status=400)
        refresh = RefreshToken.for_user(user)
        response_data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return Response(response_data)
    
# below view is for list of servicecategories

class CategoryList(generics.ListCreateAPIView):
    queryset = models.serviceCategory.objects.all()
    serializer_class = serializers.CategorySerializer

# below view is for detail view of single category    
class SingleCategoryView(generics.RetrieveAPIView):
    queryset = models.serviceCategory.objects.all()
    serializer_class = serializers.CategorydetailSerializer
    


# below view is for where vendor can add service

class AddService(generics.CreateAPIView):
    queryset = models.Service.objects.all()
    serializer_class = serializers.AddServiceSerializer
    

# below view is to show list of services in the service model
class serviceList(generics.ListCreateAPIView):
    queryset = models.Service.objects.all()
    serializer_class = serializers.ServiceListSerializer
    pagination_class = pagination.PageNumberPagination

    def get_queryset(self):
        qs=super().get_queryset()
        category=self.request.GET['category']
        category=models.serviceCategory.objects.get(id=category)
        qs=qs.filter(category=category)
        return qs

    

# below view is to show details of single service in the service model
class ServiceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Service.objects.all()
    serializer_class = serializers.ServiceDetailSerializer  


#below view is to show services which containg same tags

class TagServiceList(generics.ListAPIView):
    queryset = models.Service.objects.all()
    serializer_class = serializers.ServiceListSerializer
    pagination_class = pagination.PageNumberPagination

    def get_queryset(self):
        qs = super().get_queryset()
        tag = self.kwargs['tag']
        qs=qs.filter(tags__icontains=tag)
        return qs

   #below view is to show list of services in the particular location

class LocationServiceList(generics.ListAPIView):
    queryset = models.Service.objects.all()
    serializer_class = serializers.ServiceListSerializer
    pagination_class = pagination.PageNumberPagination

    def get_queryset(self):
        qs = super().get_queryset()
        location = self.kwargs['location']
        qs=qs.filter(location__icontains=location)
        return qs 

#below view is show list of reviews given bt customers to services
class ServiceRatingViewSet(viewsets.ModelViewSet):
    queryset = models.Rating.objects.all()
    serializer_class = serializers.serviceRatingReviewSerializer 


 

#below view is used to show related-services
class RelatedServicesView(generics.ListAPIView):
    queryset = models.Service.objects.all()
    serializer_class = serializers.ServiceListSerializer
    pagination_class = pagination.PageNumberPagination

    def get_queryset(self):
        qs=super().get_queryset()
        # sourcery skip: inline-immediately-returned-variable
        service_id = self.kwargs['pk']  # Assuming you pass the product_id in the URL
        service =models.Service.objects.get(id=service_id)
        qs=qs.filter(category=service.category).exclude(id=service_id)# Assuming your Product model has a 'category' field
        return qs
          

#below view is used for vendor add address
class VendorAddAddressViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.VendorAddAddressSerializer
    queryset=models.vendorAddAddress.objects.all()

class VendorAddAddressListAPIView(generics.ListAPIView):
    serializer_class = serializers.CustomerAddAddressSerializer
    queryset=models.vendorAddAddress.objects.all()
   

    def get_queryset(self):
        vendor_id = self.kwargs['pk']
        return models.vendorAddAddress.objects.filter(Vendor__id=vendor_id)    

#below view is used for customer add address
class CustomerAddAddressViewSet(viewsets.ModelViewSet):
    serializer_class=serializers.CustomerAddAddressSerializer
    queryset=models.customerAddAddress.objects.all()

class CustomerAddAddressListAPIView(generics.ListAPIView):
    serializer_class = serializers.CustomerAddAddressSerializer
    queryset=models.customerAddAddress.objects.all()
   

    def get_queryset(self):
        customer_id = self.kwargs['pk']
        return models.customerAddAddress.objects.filter(Customer__id=customer_id)  


class OrderList(generics.ListCreateAPIView):
    queryset =models.Order.objects.all()
    serializer_class =serializers.OrderSerializer
   # pagination_class=pagination.LimitOffsetPagination

class serviceimage (generics.CreateAPIView):
    queryset =models.ServiceImage.objects.all()
    serializer_class= serializers.serviceImageSerializer   


# OrderDetail returns all the details of the Customers
class OrderDetail(generics.ListAPIView):
    #queryset = models.OrderItems.objects.all()
    serializer_class =serializers.OrderDetailSerializer

    def get_queryset(self):
        order_id=self.kwargs['pk']
        order=models.Order.objects.get(id=order_id)
        order_items=models.OrderItems.objects.filter(order=order)

        return order_items                          