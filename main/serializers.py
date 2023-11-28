from . import models
from rest_framework import serializers



# below vendorserializer is for vendor registration
class VendorSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = models.Vendor
        fields = ('id', 'first_name', 'last_name', 'username', 'email' ,'phone_number','password', 'confirm_password')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password', None)  # Remove 'confirm_password' from validated data
        user = models.Vendor(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
    
# below serializer is for vendor login
class VendorLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30)
    password = serializers.CharField(write_only=True)

# below serializer is for customer registration
class CustomerSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = models.Customer
        fields = ('id', 'first_name', 'last_name', 'username', 'email' ,'phone_number','password', 'confirm_password')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password', None)  # Remove 'confirm_password' from validated data
        user = models.Customer(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

# below serializer is for customer login

class CustomerLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30)
    password = serializers.CharField(write_only=True)

# below serializer is used for list of servicecategories in the category table

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=models.serviceCategory
        # which fields we want to show
        fields=['id','title','detail']

        # use depth to fetch user data
    def __init__(self, *args, **kwargs):
        super(CategorySerializer, self).__init__(*args, **kwargs)
        # self.Meta.depth = 1


#below serializer is for service_images
class serviceImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ServiceImage
        fields = ['id','service','image']      

#this serializer is for giving raing and review
class serviceRatingReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Rating
        fields = [ 'id','service','customer','rating', 'reviews',  'created_at']          
    def __init__(self,*args,**kwargs):
        super(serviceRatingReviewSerializer,self).__init__(*args,**kwargs)
        self.Meta.depth = 1
        
# below serializer is to show all the list of services in service model
class ServiceListSerializer(serializers.ModelSerializer):
     
    average_rating = serializers.SerializerMethodField() 
    service_imgs=serviceImageSerializer(many=True, read_only=True)
    class Meta:
        model=models.Service
        # which fields we want to show, coming from product model
        fields=['id','image', 'category', 'vendor', 'title','average_rating','service_imgs']
        # use depth to fetch user data
    def __init__(self, *args, **kwargs):
        super(ServiceListSerializer, self).__init__(*args, **kwargs)
        # self.Meta.depth = 1  

    def get_average_rating(self, obj):
        return obj.average_rating()                  

# below serializer is used for detail of particular serializer
class CategorydetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.serviceCategory
        fields = ['id', 'title', 'detail'] 

        

# below serializer is to add service by vendor
class AddServiceSerializer(serializers.ModelSerializer):
    service_imgs=serviceImageSerializer(many=True, read_only=True)
    class Meta:
        model=models.Service
        # which fields we want to show, coming from product model
        fields=['id','category','vendor', 'title', 'description', 'price_per_day','price_per_hour','price_per_sq_feet','price_per_service','tags','location','contact_number','image','service_imgs']

        # use depth to fetch user data
    def __init__(self, *args, **kwargs):
        super(AddServiceSerializer, self).__init__(*args, **kwargs)

    def create(self, validated_data):
        service_imgs_data = validated_data.pop('service_imgs', [])
        service = models.Service.objects.create(**validated_data)
        
        for service_img_data in service_imgs_data:
            models.ServiceImage.objects.create(service=service, **service_img_data)

        return service     

         

# below serializer is to show details of single service

class ServiceDetailSerializer(serializers.ModelSerializer):

    
    reviews=serializers.StringRelatedField(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    service_imgs=serviceImageSerializer(many=True, read_only=True)

    class Meta:
        model = models.Service
        fields = ['id', 'category', 'vendor', 'title', 'description','slug', 'price_per_day', 'price_per_hour', 'price_per_sq_feet', 'price_per_service', 'location', 'contact_number', 'demo_url','image', 'tag_list', 'average_rating','reviews','service_imgs']

        # use 1depth to fetch user data
    def __init__(self, *args, **kwargs):
        super(ServiceDetailSerializer, self).__init__(*args, **kwargs)
        # self.Meta.depth =1

    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {key: value for key, value in data.items() if value is not None} 
    
    def get_average_rating(self, obj):
        return obj.average_rating()

#below serializer used where vendor can add address
class VendorAddAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.vendorAddAddress
        fields = ['id', 'Vendor', 'address', 'phone_number','default_address']

    def __init__(self,*args,**kwargs):
        super(VendorAddAddressSerializer,self).__init__(*args,**kwargs)
        self.Meta.depth = 1    

#below serializer used where customer can add address

class CustomerAddAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.customerAddAddress
        fields = ['id', 'Customer', 'address', 'phone_number','default_address']        
 
    def __init__(self,*args,**kwargs):
        super(CustomerAddAddressSerializer,self).__init__(*args,**kwargs)
        self.Meta.depth = 1

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Order
        # which fields we want to show
        fields=['id','customer']

        # use depth to fetch user data
    def __init__(self, *args, **kwargs):
        super(OrderSerializer, self).__init__(*args, **kwargs)
        self.Meta.depth = 1


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.OrderItems
        # which fields we want to show
        fields=['id','order','service']

        # use depth to fetch user data
    def __init__(self, *args, **kwargs):
        super(OrderDetailSerializer, self).__init__(*args, **kwargs)
        self.Meta.depth = 1 
