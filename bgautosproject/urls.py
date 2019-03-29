"""bgautosproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from bgautosapp import views
from django.conf.urls import url,include
from django.apps import AppConfig
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('', views.homes),
    path('login/',views.index,name='index'),
    path('homes/',views.homes,name='homes'),
    path('update/',views.update,name='update'),
    path('myorders/',views.myorders,name='myorders'),

    url(r'^$', views.index, name = 'index'),
    # url(r'^bgautosapp/',include('bgautosapp.urls')),
    path('register',views.register,name='register'),
    path('logout',views.ulogout,name="logout"),
    path('shopping/',views.shopping,name='shopping'),
    path('register/',views.register,name='register'),
    path('admin/', admin.site.urls),
    # path('success/',success,name='success'),
    path('', include('bgautosapp.urls')),
    path('index/$',views.index,name='index'),
    path('checkout/',views.checkout,name='checkout'),
    path('ordersuccess/',views.ordersuccess,name='ordersuccess'),
    path('tracker/',views.tracker,name='tracker'),
    path('products/<int:myid>', views.productview, name="productview"),
    path('accounts/',views.accounts,name='accounts'),
    path('contact/',views.contact,name='contact'),

    path('invoice/',views.invoice,name='invoice'),
    path('feedback/',views.feedback,name='feedback'),
    path('feedbacksuccessful/',views.feedbacksuccessful,name='feedbacksuccessful'),

    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='bgautosapp/password_reset.html'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='bgautosapp/password_reset_done.html'
         ),
         name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/>',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='bgautosapp/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),

    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='bgautosapp/password_reset_complete.html'
         ),
         name='password_reset_complete'),



    #
    # path('password-reset/',
    # auth_views.PasswordResetView.as_view(template_name='bgautosapp/password_reset.html'),
    # name='password_reset'),
    #
    # path('password-reset/done/',
    # auth_views.PasswordResetDoneView.as_view(template_name='bgautosapp/password_reset_done.html'),
    # name='password_reset_done'),
    #
    #
    # path('password-reset-confirm/',
    # auth_views.PasswordResetConfirmView.as_view(template_name='bgautosapp/password_reset_confirm.html'),
    # name='password_reset_confirm'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
  # + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
