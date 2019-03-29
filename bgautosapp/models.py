from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

class MyUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)

class customer(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(primary_key=True,unique=True,blank=True )
    name = models.CharField(max_length=255,blank=True)
    # cemail = models.EmailField(unique=True,max_length=255,blank=True)
    password = models.CharField(max_length=255,blank=True)
    city = models.CharField(max_length=255,blank=True)
    state = models.CharField(max_length=255,blank=True)
    phoneno = models.BigIntegerField(default=0)
    address =  models.CharField(max_length=255,blank=True)
    pincode =  models.IntegerField(default=0)



    is_staff = models.BooleanField(
        'staff status',
        default=False,
        help_text='Is the user allowed to have access to the admin',
    )
    is_active = models.BooleanField(
        'active',
        default=True,
        help_text= 'Is the user account currently active',
    )
    USERNAME_FIELD = 'email'
    objects = MyUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email


# class customer(models.Model):
    # customerid = models.AutoField(primary_key=True,default=1)
    # models.AutoField(primary_key=True)
    # models.IntegerField(unique=True,primary_key=True,blank=True)
    # REQUIRED_FIELDS = ('user',)



    # USERNAME_FIELD = 'cemail'

    # REQUIRED_FIELDS = ['cemail,cpassword,cphoneno,cpincode']

    # set_password='cpassword'
    #
    #
    # objects = CustomUserManager()

    # def __str__(self):
    #     return self.cname
    #
class report(models.Model):
    report_id = models.AutoField(primary_key=True)
    orderdate= models.DateField(default=timezone.now)
    Items = models.CharField(max_length=5000, default="")
    Name = models.CharField(max_length=90, default="")
    Email = models.CharField(max_length=111)
    Address = models.CharField(max_length=111, default="")
    City = models.CharField(max_length=111, default="")
    State = models.CharField(max_length=111, default="")
    Zip_code = models.CharField(max_length=111, default="")
    Phone = models.CharField(max_length=111, default="")
    Total = models.IntegerField(default="")
    Payment_mode= models.CharField(max_length=30, default="Cash On Delivery")

    

class brand(models.Model):
    brandid = models.AutoField(primary_key=True)
    brandname = models.CharField(max_length=255,default='empty')

    def __str__(self):
        return self.brandname


    # def __str__(self):
    #     return str(self.date)
    #



class category(models.Model):
    categoryid = models.AutoField(primary_key=True)
    catname = models.CharField(max_length=255,default='empty')

    def __str__(self):
        return self.catname

class product(models.Model):
    productid = models.AutoField(primary_key=True)

    catname = models.ForeignKey('category',on_delete=models.CASCADE,)
    # brandid = models.ForeignKey('brand',on_delete=models.CASCADE,)
    # reviewid = models.ForeignKey('review',on_delete=models.CASCADE,)
    brandname= models.CharField(max_length=30,default='empty')
    producttitle = models.CharField(max_length=255,default='empty')
    productimage1 =  models.ImageField(upload_to='shop/images',max_length=255,default='empty')
    productimage2 =  models.ImageField(upload_to='shop/images',max_length=255,default='empty')
    productimage3 =  models.ImageField(upload_to='shop/images',max_length=255,default='empty')
    productcolor = models.TextField(max_length=255,default='empty')
    productprice = models.IntegerField(default='empty')
    productdesc = models.TextField()

    def __str__(self):
        return self.producttitle


class comment(models.Model):
    commentid = models.AutoField(primary_key=True)
    # productid = models.ForeignKey('product',on_delete=models.CASCADE,)
    productid = models.ForeignKey('product',on_delete=models.CASCADE,)
    content = models.TextField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return self.content
















class cart(models.Model):
    cartid = models.AutoField(primary_key=True)
    email = models.ForeignKey('customer',on_delete=models.CASCADE,)
    productid = models.ForeignKey('product',on_delete=models.CASCADE,)
    qty = models.IntegerField(default='empty')

    def __str__(self):
        return self.email



class order(models.Model):
    order_id = models.AutoField(primary_key=True)
    orderdate= models.DateField(default=timezone.now)
    items_json = models.CharField(max_length=5000, default="")
    name = models.CharField(max_length=90, default="")
    email = models.CharField(max_length=111)
    address = models.CharField(max_length=111, default="")
    city = models.CharField(max_length=111, default="")
    state = models.CharField(max_length=111, default="")
    zip_code = models.CharField(max_length=111, default="")
    phone = models.CharField(max_length=111, default="")
    total = models.IntegerField(default="")
    payment_mode= models.CharField(max_length=30, default="Cash On Delivery")




    # orderid = models.IntegerField(unique=True,primary_key=True,default='empty')
    # email = models.ForeignKey('customer',on_delete=models.CASCADE,)
    # productid = models.ForeignKey('product',on_delete=models.CASCADE,)
    # cartid = models.ForeignKey('cart',on_delete=models.CASCADE,)
    # amount = models.IntegerField(default='empty')
    # invoiceno = models.IntegerField(default='empty')
    # orderdate = models.DateField()
    # orderstatus = models.CharField(max_length=255,default='empty')


# class tracking(models.Model):
#     trackingid = models.IntegerField(unique=True,primary_key=True,default='empty')
#     orderid = models.ForeignKey('order',on_delete=models.CASCADE,)
#     logisticname = models.CharField(max_length=255,default='empty')
#
#     def __str__(self):
#         return self.trackingid


class orderupdate(models.Model):
    update_id  = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:7] + "..."


class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=70, default="")
    phone = models.CharField(max_length=70, default="")
    desc = models.CharField(max_length=500, default="")


    def __str__(self):
        return self.name
