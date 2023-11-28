from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Avg
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


# the below model is for vendor 
class Vendor(AbstractUser):
    # Fields you mentioned
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=12)
    
    def __str__(self):
        return self.username

    class Meta:
        permissions = [
            ("can_view_sensitive_data", "Can view sensitive data"),
            # Add any custom permissions you need here
        ]

    # Use related_name to resolve the clashes
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='vendors',
        related_query_name='vendor',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='vendors',
        related_query_name='vendor',
        blank=True,
    )

# below model is for customer
class Customer(AbstractUser):
    # Fields you mentioned
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=12)
    
    def __str__(self):
        return self.username

    class Meta:
        permissions = [
            ("can_view_sensitive_data", "Can view sensitive data"),
            # Add any custom permissions you need here
        ]

    # Use related_name to resolve the clashes
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customers',
        related_query_name='customer',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customers',
        related_query_name='customer',
        blank=True,
    )

# below model is for servicecategory

class serviceCategory(models.Model):
    # whenevr you use charfiled the max length is compulsary
    title=models.CharField(max_length=200)
    # This details field can be null
    detail=models.TextField(null=True)

    # whenever we call this fuction it returns,this magic methog __str__, self.title
    def __str__(self):
        return self.title

# below model is for service

class Service(models.Model):
    # the vendor has to select what kind of category his ervice belongs to
    category=models.ForeignKey(serviceCategory,on_delete=models.SET_NULL,null=True,related_name='category_product')
    # Who is adding the product
    vendor=models.ForeignKey(Vendor,on_delete=models.SET_NULL,null=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    slug = models.CharField(max_length=300,unique=True,null=True)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    price_per_service = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    price_per_sq_feet = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    location = models.CharField(max_length=200)
    contact_number = models.CharField(max_length=20)
    tags=models.TextField(null=True)
    image=models.ImageField(upload_to='service_imgs',null=True)
    demo_url=models.URLField(null=True,blank=True)

    def __str__(self):
        return self.title 
    
    #below function is for tags
    def tag_list(self):
        # sourcery skip: assign-if-exp, inline-immediately-returned-variable, reintroduce-else 
        tagList = self.tags.split(',')
        return tagList
     
    
    #below function is for location
    def location_list(self):
        locationList = self.location.split(',')
        return locationList
    
    #below function is to show average_rating of service 
    def average_rating(self):
        return self.reviews.aggregate(Avg('rating'))['rating__avg']
    


class ServiceImage(models.Model):
     
    service=models.ForeignKey(Service,on_delete=models.CASCADE,related_name='service_imgs')
    # we define null because we have already existing rows
    image=models.ImageField(upload_to='service_imgs/',null=True)


    # we will return address
    def __str__(self):
        return self.image.url   
    
# below model is give reviews and ratings to a service by customer

class Rating(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='reviews')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='reviews')
    reviews = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.reviews    

# below model used for vendor ad-address
class vendorAddAddress(models.Model):
    Vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    address= models.TextField(max_length=500,null=True)
    phone_number = PhoneNumberField(null=True)
    default_address=models.BooleanField(default=False)   

# below model used for customer ad-address
class customerAddAddress(models.Model):
    Customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    address= models.TextField(max_length=500,null=True)
    phone_number = PhoneNumberField(null=True)
    default_address=models.BooleanField(default=False)


class Order(models.Model):
    # who made this order, using cascade if we delete the customer, order data will  be deleted
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    # order time
    order_time=models.DateTimeField(auto_now_add=True)


class OrderItems(models.Model):
    # Specific order num which have multiple items
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='order_items')
    # which product the customer ordered
    Service=models.ForeignKey(Service,on_delete=models.CASCADE)

    # we will return product title
    def __str__(self):
        return self.product.title         