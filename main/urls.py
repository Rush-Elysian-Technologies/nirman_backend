from django.urls import path
from . import views
from rest_framework import routers



router=routers.DefaultRouter()

router.register('productrating',views.ServiceRatingViewSet)
router.register('customeraddaddress',views.CustomerAddAddressViewSet)
router.register('vendoraddaddress',views.VendorAddAddressViewSet)


urlpatterns = [

# below api is  used for vendor registration
path('vendor/register/', views.VendorRegisterView.as_view(), name='vendor-registration'),
# below api is used for vendor login
path('vendor/login/', views.VendorLoginView.as_view(), name='vendor-login'),
# below api is used for customer registration
path('customer/register/', views.CustomerRegisterView.as_view(), name='customer-registration'),
#below api is used for customer login
path('customer/login/', views.CustomerLoginView.as_view(), name='customer-login'),
# it will show all types of service categories
path('servicecategories/', views.CategoryList.as_view()),
# it will show all details of single category
path('category/<int:pk>/', views.SingleCategoryView.as_view()),
# below api is used to add service by vendor
path('add-service/', views.AddService.as_view(), name='add-service'),
#path('product-imgs/',views.ProductImageList.as_view()),
#below api is used for to show all services in service model
path('allservices/',views.serviceList.as_view()),
#below api is used for to show single service in service model
path('allservices/<int:pk>',views.ServiceDetail.as_view()),
#below api is used to show services having same tags
path('service/tag/<str:tag>/',views.TagServiceList.as_view()),
#below api is used to show services under particular location
path('service/<str:location>/',views.LocationServiceList.as_view()),
#below api is used to show related-services
path('related-services/<int:pk>/', views.RelatedServicesView.as_view()),
#below api used to show all details of single service from services under category
path('servicecategory/vendors/<int:pk>/', views.ServiceDetail.as_view()),
# to show all address related to particular vendor
path('vendor-addresses/<int:pk>/', views.VendorAddAddressListAPIView.as_view()),
# to show all address related to particular customer
path('customer-addresses/<int:pk>/', views.CustomerAddAddressListAPIView.as_view()),
# it will show  all orders of the paricular customer
path('orders/', views.OrderList.as_view()), 
# it will show full details of single order of the customer
path('order/<int:pk>/', views.OrderDetail.as_view()), 
     

]

urlpatterns+=router.urls