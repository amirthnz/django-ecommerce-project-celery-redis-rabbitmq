from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created, send_sms
from shop.recommender import Recommender

# Create your views here.
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            products = []
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
                products.append(item['product'])

            r = Recommender()
            r.products_bought(products)
            cart.clear()
            # launch asynchronous task
            order_created.delay(order.id)
            send_sms.delay()
            return render(request,
                'orders/order/created.html',
                    {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html',{'cart':cart, 'form':form})


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,
        'admin/orders/order/detail.html',
        {'order': order}
    )
