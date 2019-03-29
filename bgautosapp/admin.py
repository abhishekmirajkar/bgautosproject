from django.contrib import admin
from django.db import models
from bgautosapp.models import *
from django.contrib.auth.models import Group
from django.urls import path
from import_export.admin import ImportExportModelAdmin

admin.site.site_header = 'BG AUTOS'


class productAdmin(admin.ModelAdmin):
    list_filter = ('productid','catname')
    search_fields = ('catname',)
    fieldsets = (
    (None, {
        'fields': (
        'brandname',
        'catname',
        'producttitle',
        'productimage1',
        'productimage2',
        'productimage3',
        'productcolor',
        'productprice',
        'productdesc',
        )
    }),
    )

class orderAdmin(admin.ModelAdmin):
    list_filter = ('order_id','name','email')
    search_fields = ('name','email',)
    readonly_fields=('name','items_json','email','address','city','state','zip_code','phone','total',)
    def has_delete_permission(self, request, obj=None):
        return False
    fieldsets = (
    (None, {
        'fields': (
        'name',
        'items_json',
        'email',
        'address',
        'city',
        'state',
        'zip_code',
        'phone',
        'total',
        )
    }),
    )
class brandAdmin(admin.ModelAdmin):
    list_filter = ('brandname',)
    search_fields = ('brandname',)
    fieldsets = (
    (None, {
        'fields': (
        'brandname',
        )
    }),
    )
class cartAdmin(admin.ModelAdmin):
    list_filter = ('email','productid',)
    search_fields = ('cartid','email','productid','qty')
    fieldsets = (
    (None, {
        'fields': (
        'email',
        'productid',
        'qty',
        )
    }),
    )
class categoryAdmin(admin.ModelAdmin):
    list_filter = ('catname',)
    search_fields = ('categoryid','catname')
    fieldsets = (
    (None, {
        'fields': (
        'catname',
        )
    }),
    )
class customerAdmin(admin.ModelAdmin):
    list_filter = ('email','phoneno','pincode')
    search_fields = ('email','name','city','state','phoneno','address','pincode')
    readonly_fields=('email','name','city','state','phoneno','address','pincode','password',)
    def has_delete_permission(self, request, obj=None):
        return False
    fieldsets = (
    (None, {
        'fields': (
        'name',
        'city',
        'state',
        'phoneno',
        'address',
        'password',
        'pincode'
        )
    }),
    )

class orderupdateAdmin(admin.ModelAdmin):
    list_filter = ('update_desc','timestamp')
    search_fields = ('update_id','order_id','update_desc','timestamp')
    fieldsets = (
    (None, {
        'fields': (
        'order_id',
        'update_desc',
        )
    }),
    )
class commentAdmin(admin.ModelAdmin):
    list_filter = ('commentid','content',)
    search_fields = ('commentid','content','timestamp')
    readonly_fields=('commentid','content',)
    def has_delete_permission(self, request, obj=None):
        return False
    fieldsets = (
    (None, {
        'fields': (
        'content',
        )
    }),
    )

admin.site.register(product,productAdmin)
admin.site.register(order,orderAdmin)
admin.site.register(brand,brandAdmin)
admin.site.register(cart,cartAdmin)
admin.site.register(category,categoryAdmin)
admin.site.register(customer,customerAdmin)
admin.site.register(orderupdate,orderupdateAdmin)
admin.site.register(comment,commentAdmin)
admin.site.unregister(Group)
admin.site.register(Contact)
# admin.site.register(customer)


@admin.register(report)
class repostAdmin(ImportExportModelAdmin):
    pass

# admin.site.register(brand)
# admin.site.register(category)
# admin.site.register(review)
# admin.site.register(product)
# admin.site.register(cart)
# admin.site.register(order)
# admin.site.register(orderupdate)
# admin.site.register(tracking)
