from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .cart import Cart
from products.models import Product
from .forms import CartAddForm, CouponApplyForm, AddressForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Order, OrderItem, Coupon
import requests
import json
from django.conf import settings
from django.contrib import messages
import datetime


class CartView(View):
    def get(self, request):
        cart = Cart(request)
        return render(request, 'orders/cart.html', {'cart': cart})


class CartAddView(View):
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        form = CartAddForm(request.POST)
        if form.is_valid():
            size = form.cleaned_data['size']
            variant = product.variants.filter(size=size).first()
            if not variant:
                messages.error(request, 'سایز انتخاب شده نامعتبر است')
                return redirect('orders:cart')
            cart.add(product, form.cleaned_data['quantity'], size)
        return redirect('orders:cart')


class CartRemoveView(View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        cart = Cart(request)
        cart.remove(product)
        return redirect('orders:cart')


class OrderDetailView(LoginRequiredMixin, View):
    form_class = CouponApplyForm
    address_form_class = AddressForm

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)
        form = self.form_class()
        address_form = self.address_form_class()
        return render(request, 'orders/order.html', {
            'order': order,
            'form': form,
            'address_form': address_form,
        })

    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)
        address_form = self.address_form_class(request.POST)

        if address_form.is_valid():
            order.receiver_name = address_form.cleaned_data['receiver_name']
            order.receiver_phone = address_form.cleaned_data['receiver_phone']
            order.address = address_form.cleaned_data['address']
            order.postal_code = address_form.cleaned_data.get('postal_code', '')
            order.save()

            messages.success(request, 'آدرس با موفقیت ثبت شد', 'success')
            return redirect('orders:order_detail', order_id)
        else:
            form = self.form_class()
            return render(request, 'orders/order.html', {
                'order': order,
                'form': form,
                'address_form': address_form,
            })


class OrderCreateView(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(request)

        if len(cart) == 0:
            messages.error(request, 'سبد خرید شما خالی است! لطفاً ابتدا محصولی اضافه کنید.', 'danger')
            return redirect('orders:cart')

        order = Order.objects.create(user=request.user)
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                size=item['size'],
                price=item['price'],
                quantity=item['quantity']
            )
        cart.clear()
        return redirect('orders:order_detail', order.id)


class OrderPayView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)

        if order.get_total_price() <= 0:
            messages.error(request, 'امکان پرداخت با مبلغ صفر وجود ندارد!', 'danger')
            return redirect('orders:order_detail', order_id)

        if not order.address:
            messages.error(request, 'لطفاً ابتدا آدرس تحویل را ثبت کنید', 'danger')
            return redirect('orders:order_detail', order_id)
        
        request.session["order_pay"] = {"order_id": order.id}
        zp_req_headers = {'accept': 'application/json', 'content-type': 'application/json'}
        zp_req_data = {"merchant_id": settings.ZP_MERCHANT_ID,
                       "amount": order.get_total_price(),
                       "description": f"{order.user} - {order.updated}",
                       "metadata": {"mobile": f"{request.user.phone_number}", "email": f"{request.user.email}"},
                       "callback_url": "https://example.ir/orders/verify/"}
        zp_req = requests.post(settings.ZP_API_REQUEST, data=json.dumps(zp_req_data), headers=zp_req_headers)

        if zp_req.json()["data"]["code"] == 100:
            zp_authority = zp_req.json()["data"]["authority"]
            return redirect(f"https://payment.zarinpal.com/pg/StartPay/{zp_authority}")
        else:
            messages.error(request, "تراکنش ناموفق ", "danger")
            return redirect("home:home")


class OrderVerifyView(LoginRequiredMixin, View):
    def get(self, request):
        order_id = request.session['order_pay']['order_id']
        order = get_object_or_404(Order, id=order_id)
        zp_authority = request.GET.get("Authority")
        zp_status = request.GET.get("Status")
        if zp_status == "OK":
            zp_req_headers = {'accept': 'application/json', 'content-type': 'application/json'}
            zp_req_data = {"merchant_id": settings.ZP_MERCHANT_ID, "amount": order.get_total_price(),
                           "authority": zp_authority}
            zp_verity_req = requests.post(settings.ZP_API_VERIFY, data=json.dumps(zp_req_data), headers=zp_req_headers)

            if len(zp_verity_req.json()["error"]) == 0 and zp_verity_req.json()["data"]["code"] == 100:
                order.paid = True
                order.save()
                messages.success(request, "پرداخت با موفقیت انجام شد", "success")
                return redirect("home:home")
            else:
                zp_error_code = zp_verity_req.json()["errors"]["code"]
                zp_error_message = zp_verity_req.json()["errors"]["message"]
                messages.error(request, f"Error {zp_error_code}, {zp_error_message}..!", "danger")
                return redirect("home:home")
        else:
            messages.error(request, "تراکنش نا موفق", "danger")
            return redirect("home:home")


class CouponApplyView(LoginRequiredMixin, View):
    form_class = CouponApplyForm

    def post(self, request, order_id):
        naw = datetime.datetime.now()
        form = self.form_class(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                coupon = Coupon.objects.get(code__exact=code, valid_from__lte=naw, valid_to__gte=naw, active=True)
            except Coupon.DoesNotExist:
                messages.error(request,'کد تخفیف معتبر نیست', 'danger')
                return redirect("orders:order_detail", order_id)
            order = Order.objects.get(id=order_id)
            order.discount = coupon.discount
            order.save()
        return redirect("orders:order_detail", order_id)