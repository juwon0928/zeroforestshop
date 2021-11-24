import random
import string
from django.http.response import JsonResponse
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.generic import ListView, DetailView, View
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from .forms import CheckoutForm, CouponForm, PaymentForm
from .models import Item, OrderItem, Order, Address, Payment, Coupon, UserProfile

from django.shortcuts import render, redirect

# Create your views here.
from .forms import *
from .models import *

def products(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, "products.html", context)


def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid


class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
                'form': form,
                'couponform': CouponForm(),
                'order': order,
                'DISPLAY_COUPON_FORM': True
            }

            shipping_address_qs = Address.objects.filter(
                user=self.request.user,
                default=True
            )
            if shipping_address_qs.exists():
                context.update(
                    {'default_shipping_address': shipping_address_qs[0]})
            return render(self.request, "checkout.html", context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "주문된 제품이 없습니다.")
            return redirect("core:checkout")

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():

                use_default_shipping = form.cleaned_data.get(
                    'use_default_shipping')
                if use_default_shipping:
                    print("기본 배송 주소 사용")
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        default=True
                    )
                    if address_qs.exists():
                        shipping_address = address_qs[0]
                        order.shipping_address = shipping_address
                        order.save()
                    else:
                        messages.warning(
                            self.request, "사용 가능한 기본 배송 주소가 없습니다.")
                        return redirect('core:checkout')
                else:
                    print("사용자가 새 배송 주소를 입력합니다.")
                    shipping_address1 = form.cleaned_data.get(
                        'shipping_address')
                    shipping_address2 = form.cleaned_data.get(
                        'shipping_address2')
                    shipping_country = form.cleaned_data.get(
                        'shipping_country')
                    shipping_zip = form.cleaned_data.get('shipping_zip')

                    if is_valid_form([shipping_address1, shipping_country, shipping_zip]):
                        shipping_address = Address(
                            user=self.request.user,
                            street_address=shipping_address1,
                            apartment_address=shipping_address2,
                            country=shipping_country,
                            zip=shipping_zip,
                        )
                        shipping_address.save()

                        order.shipping_address = shipping_address
                        order.save()

                        set_default_shipping = form.cleaned_data.get(
                            'set_default_shipping')
                        if set_default_shipping:
                            shipping_address.default = True
                            shipping_address.save()

                    else:
                        messages.warning(
                            self.request, "필수 배송 주소란을 작성하십시오.")

                
        except ObjectDoesNotExist:
            messages.warning(self.request, "주문된 제품이 없습니다.")
            return redirect("core:order-summary")


class PaymentView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
   
    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        form = PaymentForm(self.request.POST)
        userprofile = UserProfile.objects.get(user=self.request.user)
        if form.is_valid():
            save = form.cleaned_data.get('save')
            use_default = form.cleaned_data.get('use_default')

           
class HomeView(ListView):
    model = Item
    paginate_by = 12
    template_name = "home.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("query")
        category = self.request.GET.get("category")
        if query:
            queryset = queryset.filter(Q(title__icontains=query)
                                       | Q(description__icontains=query))
        if category:
            queryset = queryset.filter(category_id=category)
        return queryset


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "주문된 제품이 없습니다.")
            return redirect("/")


class ItemDetailView(DetailView):
    model = Item
    template_name = "product.html"

class AddToCart(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug')
        item = get_object_or_404(Item, slug=slug)
        order_item, created = OrderItem.objects.get_or_create(
            item=item,
            user=request.user,
            ordered=False #이미 구매한 제품은 가지지 않도록
        )
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            # 주문항목이 주문에 있는지 확인
            if order.items.filter(item__slug=item.slug).exists():
                order_item.quantity += 1
                order_item.save()
                messages.success(request, "제품 수량이 업데이트되었습니다.")
                return redirect("core:order-summary")
            else:
                order.items.add(order_item)
                messages.success(request, "제품이 장바구니에 추가되었습니다.")
                return redirect("core:order-summary")
        else:
            ordered_date = timezone.now()
            order = Order.objects.create(
                user=request.user, ordered_date=ordered_date)
            order.items.add(order_item)
            messages.success(request, "제품이 장바구니에 추가되었습니다.")
            return redirect("core:order-summary")


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # 주문 항목이 주문에 있는지 확인
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.success(request, "제품이 장바구니에서 제거되었습니다.")
            return redirect("core:order-summary")
        else:
            messages.warning(request, "제품이 장바구니에 없습니다.")
            return redirect("core:product", slug=slug)
    else:
        messages.warning(request, "주문된 제품이 없습니다.")
        return redirect("core:product", slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # 주문 항목이 주문에 있는지 확인
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.success(request, "제품 수량이 업데이트되었습니다.")
            return redirect("core:order-summary")
        else:
            messages.warning(request, "제품이 장바구니에 없습니다.")
            return redirect("core:product", slug=slug)
    else:
        messages.warning(request, "주문된 제품이 없습니다.")
        return redirect("core:product", slug=slug)


def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.warning(request, "쿠폰이 존재하지 않습니다.")
        return redirect("core:checkout")


class AddCouponView(View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(
                    user=self.request.user, ordered=False)
                order.coupon = get_coupon(self.request, code)
                order.save()
                messages.success(self.request, "쿠폰을 성공적으로 추가했습니다.")
                return redirect("core:checkout")
            except ObjectDoesNotExist:
                messages.warning(self.request, "주문된 제품이 없습니다.")
                return redirect("core:checkout")

@login_required
@csrf_exempt
def process_order(request):
    if request.method == "POST":
        order_id = request.POST.get('order')
        txn_id = request.POST.get('txn_id')
        order = Order.objects.get(id=order_id)
        order_items = order.items.all()
        order_items.update(ordered=True)
        for item in order_items:
            item.save()
        order.ordered = True
        order.save()

        return JsonResponse({"status": "success"})



from django.shortcuts import render,redirect,get_object_or_404
from .models import Board
from .forms import BoardForm

def index(request):
    return render(request,'index.html')

def create(request):
    if request.method == "POST":
        create_form = BoardForm(request.POST)
        if create_form.is_valid():
            create_form.save()
            return redirect('core:index') # 글 쓰고 인덱스로 감
    else:
        create_form = BoardForm()
    return render(request,'create.html',{'create_form':create_form})

def index(request):
    all_board = Board.objects.all()
    return render(request, 'index.html',{'all_board':all_board})



def delete(request, board_id):
    my_board = get_object_or_404(create,id=board_id)
    my_board.delete()
    return redirect('index')