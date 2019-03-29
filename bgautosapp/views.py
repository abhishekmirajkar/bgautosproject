from django.shortcuts import render,HttpResponseRedirect, get_object_or_404
from django.contrib.auth import authenticate, logout , login
from django.urls import reverse
from bgautosapp.models import customer
from django.db.models import Q
from bgautosapp.forms import UserForm, UserProfileInfoForm
from django import forms
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import product, Contact, category , order , orderupdate ,customer ,comment,report
from math import ceil
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
import json
from django.views.generic import View
from django.template.loader import get_template
from .utils import render_to_pdf
from django.template.loader import render_to_string
from .forms import*
from django.conf import settings
# Create your views here.
global str
import requests


logins = False
def myorders(request):
    response = ''
    if 'search' in request.GET:
        search_term = request.GET['search']
        prod_list = product.objects.filter( Q(producttitle__icontains=search_term)| Q(brandname__icontains=search_term) |  Q(productprice__icontains=search_term)).distinct()
        params = {'prod_list' : prod_list}
        return render(request , 'bgautosapp/shopping.html' , params)


    email=request.session['email']
    Orders = order.objects.filter(email=email)

    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        print(orderId)
        email=request.session['email']
        print(email)

        try:
            Orders = order.objects.filter(order_id=orderId, email=email)
            if len(Orders)>0:
                update = orderupdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps([updates, Orders[0].items_json], default=str)
                return HttpResponse(response)
            else:
                return HttpResponse(response)
        except Exception as e:
            return HttpResponse('{}')

        return render(request, 'bgautosapp/tracker.html')


    return render(request, 'bgautosapp/myorders.html',{'Orders':Orders})




def update(request):
    registered = False
    email=request.session['email']
    print(email)
    Customers = customer.objects.get(email=email)


    if request.method=="POST":
        name = request.POST.get('name', 'HELLLLL')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        phone = request.POST.get('phone', '')
        address = request.POST.get('address', '')
        pincode = request.POST.get('pincode', '')
        password=request.session['password']

        Customer = customer.objects.get(email=email)
        Customer.name = name
        Customer.city = city
        Customer.state = state
        Customer.phone = phone
        Customer.address = address
        Customer.pincode = pincode
        Customer.save()
        registered = True

    return render(request, 'bgautosapp/update.html',{'registered':registered ,'Customers':Customers })


def contact(request):
    registered = False

    if request.method=="POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        registered = True

    return render(request, 'bgautosapp/contact.html',{'registered':registered})


def feedback(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phoneno = request.POST.get('phone', '')
        feedback = request.POST.get('feedback', '')
        feed = review(name=name,email=email,phoneno=phoneno,feedback=feedback)
        feed.save()

        return render(request,'bgautosapp/feedbacksuccessful.html')

    return render(request,'bgautosapp/feedback.html')

def feedbacksuccessful(request):
    return render(request,'bgautosapp/feedbacksuccessful.html',)



def index(request):
    context={}

    if request.method == "POST":
         # ''' Begin reCAPTCHA validation '''
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()
            # ''' End reCAPTCHA validation '''

            if result['success']:

                username = request.POST.get('cusername')
                # ['cusername']
                # get('cusername')

                password = request.POST.get('ccpassword')
                # ['ccpassword']
                # get('ccpassword')
                user = authenticate( username = username, password = password )
                request.session['email'] = username
                request.session['password'] = password

                print(request.session['email'])

                if user:
                    if user.is_active:
                        login(request,user)
                        logins =True
                        return HttpResponseRedirect(reverse('shopping'))
                    else:
                        context["error"] = "provide valid credentials !!"
                        return HttpResponse("Account Not Active ")
                        # return render(request,'bgautosapp/index.html')
                else:
                    print("SOMEONE TIRED TO LOGIN AND FAILED")
                    print("They used username: {} and password: {}".format(username,password))

                    context["error"] = "provide valid credentials !!"
                    return render(request ,'bgautosapp/index.html', {'error_message':'Invalid Credentials'})
            else:
                return render(request,'bgautosapp/index.html')

    return render(request,'bgautosapp/index.html')


def register(request):
    # form = UserCreationForm()
    # return render(request,'bgautosapp/register.html')
    register=False
    registered=False
    if request.method =="POST" :
        email = request.POST.get('email', '')
        name = request.POST.get('name', '')
        password = request.POST.get('password', '')

        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        phoneno = request.POST.get('phone', '')
        address = request.POST.get('address', '')
        pincode = request.POST.get('pin', '')

        if customer.objects.filter(email=email):
            register=True
            return render(request,'bgautosapp/register.html',{'register':register})


        customer.objects.create_user(email=email,name=name,password=password,city=city,state=state,phoneno=phoneno,address=address,pincode=pincode)



    #     user_form = UserForm(data=request.POST)
    #     profile_form = UserProfileInfoForm(data = request.POST)
    #
    #
    #     if user_form.is_valid() and profile_form.is_valid():
    #         user = user_form.save()
    #         user.set_password(user.password)
    #         user.save()
    #
    #         profile= profile_form.save(commit=False)
    #         profile.user=user
    #
    #         if 'image' in request.FILES:
    #             profile.image = request.FILES['image']
    #
    #
    #         profile.save()
    #
    #         registered = True
    #
    #     else:
    #         print(user_form.errors,profile_form.errors)
    # else:
    # ,{'user_form':user_form,'profile_form':profile_form,'registered':registered}
    #     user_form = UserForm()
    #     profile_form = UserProfileInfoForm()

        registered=True
        return render(request,'bgautosapp/register.html',{'registered':registered})
    return render(request,'bgautosapp/register.html')



def shopping(request):
    search_term = '';
    allProds = []
    context={}
    nSlides=0
    prod_list=''
    context['user'] = request.user

    if 'search' in request.GET:
        search_term = request.GET['search']
        prod_list = product.objects.filter( Q(brandname__icontains=search_term) |  Q(brandname__icontains=search_term) | Q(producttitle__icontains=search_term) |  Q(productprice__icontains=search_term)).distinct()
        params = {'prod_list' : prod_list}
        return render(request , 'bgautosapp/shopping.html' , params)
    else:


        catprods = product.objects.values('catname')
        print(catprods)
        cats = {item['catname'] for item in catprods}
        print(cats)
        for cat in cats:
            prod = product.objects.filter(catname=cat)
            print(prod)
            n = len(prod)
            nSlides = n // 4 + ceil((n / 4) - (n // 4))
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds':allProds, 'search_term':search_term}



    return render(request , 'bgautosapp/shopping.html' , params)



def ulogout(request):
    if request.method == "POST":
        logout(request)
        logins = False
        return HttpResponseRedirect(reverse('homes'))

def productview(request, myid):
    # Fetch the product using the id
    productid=myid
    user = get_user_model()
    if user.is_active:
        print(myid)
        prod = product.objects.filter(productid=myid)

        comments = comment.objects.filter(productid=myid).order_by('-commentid')

        if request.method == 'POST':
            comment_form = CommentForm(request.POST or None)
            if comment_form.is_valid():
                id = product.objects.get(productid=myid)
                content = request.POST.get('content')
                Comment = comment.objects.create(productid=id, content=content)
                Comment.save()
        else:
                comment_form = CommentForm()

        if 'search' in request.GET:
            search_term = request.GET['search']
            print(search_term)
            prod_list = product.objects.filter( Q(brandname__icontains=search_term) |  Q(producttitle__icontains=search_term) |  Q(productprice__icontains=search_term)).distinct()

            print("THIS IS SOMETHING")
            print(prod_list)
            print("THIS IS SOMETHING")

            params = {'prod_list' : prod_list}
            print(params)

            return render(request , 'bgautosapp/shopping.html' , params)
        return render(request, 'bgautosapp/productview.html', {'prod':prod[0] , 'comments':comments, 'comment_form':comment_form, },myid)


        # return HttpResponseRedirect(reverse('index'))
@login_required(login_url="/login/")
def checkout(request):
    email=request.session['email']
    Customers = customer.objects.get(email=email)


    id=0;
    user = get_user_model()
    if 'search' in request.GET:
        search_term = request.GET['search']
        print(search_term)
        prod_list = product.objects.filter( Q(producttitle__icontains=search_term) |  Q(brandname__icontains=search_term) |  Q(productprice__icontains=search_term)).distinct()

        print("THIS IS SOMETHING")
        print(prod_list)
        print("THIS IS SOMETHING")

        params = {'prod_list' : prod_list}
        print(params)
        return render(request , 'bgautosapp/shopping.html' , params)

    if request.method=="POST":

        user = get_user_model()

        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        price =request.POST.get('smname','')
        rname = request.POST.get('rname', '')


        print(price)
        print("HELLP")
        Orders = order(items_json=items_json, name=name, email=email, address=address, city=city,
                       state=state, zip_code=zip_code, phone=phone,total=price)
        Orders.save()

        Reports = report(Items=rname, Name=name, Email=email, Address=address, City=city,
                               State=state, Zip_code=zip_code, Phone=phone,Total=price)


        Reports.save()

        thank = True
        id1 = Orders.order_id
        id=id1;
        print(id);
        thank = True
        id = Orders.order_id
        update = orderupdate(order_id=Orders.order_id, update_desc="The order has been successfully placed")
        update.save()

        # return render(request, 'bgautosapp/checkout.html', {'thank':thank, 'id': id})
        return render(request, 'bgautosapp/ordersuccess.html', {'thank':thank, 'id': id})

    return render(request, 'bgautosapp/checkout.html', {'id': id ,'Customers':Customers })


def password_rest(request):
    return render(request,'bgautosapp/password_reset.html')


def password_rest_confrim(request):
    return render(request,'bgautosapp/password_reset_confirm.html')

@login_required(login_url="/login/")
def accounts(request):
    return render(request,'bgautosapp/accounts.html')


def ordersuccess(request):
    if 'search' in request.GET:
        search_term = request.GET['search']
        print(search_term)
        prod_list = product.objects.filter( Q(producttitle__icontains=search_term) | Q(brandname__icontains=search_term) |   Q(productprice__icontains=search_term)).distinct()

        print("THIS IS SOMETHING")
        print(prod_list)
        print("THIS IS SOMETHING")

        params = {'prod_list' : prod_list}
        print(params)
        return render(request , 'bgautosapp/shopping.html' , params)


    return render(request,'bgautosapp/ordersuccess.html')


def tracker(request):
    response = ''
    if 'search' in request.GET:
        search_term = request.GET['search']
        print(search_term)
        prod_list = product.objects.filter( Q(producttitle__icontains=search_term)| Q(brandname__icontains=search_term) |  Q(productprice__icontains=search_term)).distinct()
        print("THIS IS SOMETHING")
        print(prod_list)
        print("THIS IS SOMETHING")
        params = {'prod_list' : prod_list}
        print(params)
        return render(request , 'bgautosapp/shopping.html' , params)


    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            Orders = order.objects.filter(order_id=orderId, email=email)
            if len(Orders)>0:
                update = orderupdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps([updates, Orders[0].items_json], default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')

    return render(request, 'bgautosapp/tracker.html')

def invoice(request, *args, **kwargs):
    user= get_user_model();
    if 'search' in request.GET:
        search_term = request.GET['search']
        print(search_term)
        prod_list = product.objects.filter(  Q(brandname__icontains=search_term) | Q(producttitle__icontains=search_term) |  Q(productprice__icontains=search_term) | Q(productdesc__icontains=search_term) ).distinct()
        print("THIS IS SOMETHING")
        print(prod_list)
        print("THIS IS SOMETHING")
        params = {'prod_list' : prod_list}
        print(params)
        return render(request , 'bgautosapp/shopping.html' , params)


    if request.method=="POST":
        orderId = request.POST.get('orderid', '')
        eemail = request.POST.get('email', '')
        odata = order.objects.filter(order_id=orderId, email=eemail)

        orders_data={'odata':odata}
        template = get_template('invoice.html')

        print(odata)
        html = template.render(orders_data)
        pdf = render_to_pdf('invoice.html', orders_data)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s.pdf" %("12341231")
            download = request.GET.get("download")
            content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            # return response
            return render(request,'bgautosapp/invoice.html',orders_data)


    return render(request,'bgautosapp/invoice.html')



def homes(request):

    search_term = '';
    allProds = []
    context={}
    nSlides=0
    prod_list=''
    context['user'] = request.user

    if 'search' in request.GET:
        search_term = request.GET['search']
        prod_list = product.objects.filter( Q(brandname__icontains=search_term) |  Q(brandname__icontains=search_term) | Q(producttitle__icontains=search_term) |  Q(productprice__icontains=search_term)).distinct()
        params = {'prod_list' : prod_list}
        return render(request , 'bgautosapp/shopping.html' , params)
    else:


        catprods = product.objects.values('catname')
        print(catprods)
        cats = {item['catname'] for item in catprods}
        print(cats)
        for cat in cats:
            prod = product.objects.filter(catname=cat)
            print(prod)
            n = len(prod)
            nSlides = n // 4 + ceil((n / 4) - (n // 4))
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds':allProds, 'search_term':search_term}

    return render(request,'bgautosapp/home.html', params)



@login_required(login_url="/login/")
def buynow(request):
    return render (request,'bgautosapp/checkout.html')
