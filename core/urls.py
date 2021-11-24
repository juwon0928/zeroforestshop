
from django.urls import path

from . import views
from .views import (
    ItemDetailView,
    CheckoutView,
    HomeView,
    OrderSummaryView,
    AddToCart,
    process_order,
    remove_from_cart,
    remove_single_item_from_cart,
    PaymentView,
    AddCouponView,
    index,
    create,
)


app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('add-to-cart/<slug>/', AddToCart.as_view(), name='add-to-cart'),
    path('add-coupon/', AddCouponView.as_view(), name='add-coupon'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart,
         name='remove-single-item-from-cart'),
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
    path('process-order/', process_order, name='process-order'),
    path('index/', index, name = "index"),
    path('create/', create, name="create"),
    path('delete/<int:board_id>', views.delete, name="delete"),
    
]
