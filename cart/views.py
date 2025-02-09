import stripe
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from .cart import Cart
from .forms import CheckoutForm
from order.utilities import checkout, notify_vendor, notify_customer

def cart_detail(request):
    cart = Cart(request)
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            stripe.api_key = settings.STRIPE_SECRET_KEY
            stripe_token = form.cleaned_data['stripe_token']
            
            try:
                charge = stripe.Charge.create(
                    amount = int(cart.get_total_cost()*100),
                    currency = 'USD',
                    description = 'Charge from InteriorShop',
                    source = stripe_token
                )
                
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                email = form.cleaned_data['email']
                address = form.cleaned_data['address']
                zipcode = form.cleaned_data['zipcode']
                phone = form.cleaned_data['phone']
                place = form.cleaned_data['place']
                
                order = checkout(request, first_name, last_name, email, address, zipcode, phone, place, cart.get_total_cost())
                
                cart.clear()
                
                notify_customer(order)
                notify_vendor(order)
                return redirect('success')
            except Exception as e:
                messages.error(request, f'There was something wrong with the payment\n{e}')
    else:
        form = CheckoutForm()
    
    remove_from_cart = request.GET.get('remove_from_cart', '')
    change_quantity = request.GET.get('change_quantity', 0)
    quantity = request.GET.get('quantity', '')
    if remove_from_cart:
        cart.remove(remove_from_cart)
        return redirect('cart')
    
    if change_quantity:
        cart.add(change_quantity, quantity, True)
        return redirect('cart')
    
    return render(request, 'cart/cart.html', {'form':form, 'stripe_pub_key': settings.STRIPE_PUB_KEY})

def success(request):
    return render(request, 'cart/success.html')
