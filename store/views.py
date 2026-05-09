from django.shortcuts import render
from .models import Product
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required

def home(request):
    products = Product.objects.all()
    return render(request, 'store/index.html', {'products': products})
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'store/product_detail.html', {'product': product})
def add_to_cart(request, id):

    cart = request.session.get('cart', [])

    cart.append(id)

    request.session['cart'] = cart

    return redirect('cart')


def cart(request):

    cart = request.session.get('cart', [])

    products = Product.objects.filter(id__in=cart)

    return render(request, 'store/cart.html', {'products': products})
def register(request):

    form = RegisterForm()

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')

    return render(request, 'store/register.html', {'form': form})
@login_required
def place_order(request):

    cart = request.session.get('cart', [])

    products = Product.objects.filter(id__in=cart)

    for product in products:

        Order.objects.create(
            user=request.user,
            product=product
        )

    request.session['cart'] = []

    return render(request, 'store/order_success.html')