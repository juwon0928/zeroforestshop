from django.contrib import admin

from core.models import Category, Item, OrderItem, Order, Payment, Coupon, Address, UserProfile
from django_summernote.admin import SummernoteModelAdmin

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'ordered_date',
                    'shipping_address',
                    'payment',
                    'coupon'
                    ]
    list_display_links = [
        'user',
        'shipping_address',
        'payment',
        'coupon'
    ]
    list_filter = ['ordered',
                   'being_delivered',
                   'received',
                   ]
    search_fields = [
        'user__username',
    ]


class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'street_address',
        'apartment_address',
        'country',
        'zip',
        'default'
    ]
    list_filter = ['default', 'country']
    search_fields = ['user', 'street_address', 'apartment_address', 'zip']


class ItemAdmin(SummernoteModelAdmin):
    list_display = [
        'title',
        'price',
        'discount_price',
        'stock',
        'category',
        'slug',
    ]
    Summernote_fields = ('description',)
    list_editable = [
        'price',
        'stock',
    ]


admin.site.register(Item, ItemAdmin)
admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment)
admin.site.register(Coupon)
admin.site.register(Address, AddressAdmin)
admin.site.register(UserProfile)
admin.site.register(Category)