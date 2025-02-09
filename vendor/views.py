from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify
from .models import Vendor
from product.models import Product, ProductImage
from .forms import ProductForm, ProductImageForm

def become_vendor(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            vendor = Vendor.objects.create(name=user.username, created_by=user)
            return redirect('frontpage')
    else:
        form = UserCreationForm()
        
    return render(request, 'vendor/become_vendor.html', {'form':form})

@login_required
def vendor_admin(request):
    vendor = request.user.vendor
    products = vendor.products.all()
    orders = vendor.orders.all()
    
    for order in orders:
        order.vendor_amount = 0
        order.vendor_paid_amount = 0
        order.fully_paid = True
    
        for item in order.items.all():
            if item.vendor == request.user.vendor:
                if item.vendor_paid:
                    order.vendor_paid_amount += item.get_total_price()
                else:
                    order.vendor_amount += item.get_total_price()
                    order.fully_paid = False
        
    return render(request, 'vendor/vendor_admin.html', {'vendor':vendor, 'products':products, 'orders':orders})

@login_required
def add_product(request):
    if request.method == 'POST':
        product_form = ProductForm(request.POST)
        image_form = ProductImageForm(request.POST, request.FILES)

        if product_form.is_valid() and image_form.is_valid():
            product = product_form.save(commit=False)
            product.vender = request.user.vendor
            product.slug = slugify(product.title)
            product.save()
            
            images = image_form.cleaned_data['images']
            for image in images:
                ProductImage.objects.create(product=product, image=image)
            
            return redirect('vendor_admin')
    else:
        product_form = ProductForm()
        image_form = ProductImageForm()
    return render(request, 'vendor/add_product.html', {'product_form':product_form, 'image_form':image_form})

@login_required
def edit_product(request, pk):
    vendor = request.user.vendor
    product = vendor.products.get(pk=pk)
    
    if request.method == 'POST':
        product_form = ProductForm(request.POST, instance=product)
        image_form = ProductImageForm(request.POST, request.FILES)
        
        if product_form.is_valid() and image_form.is_valid():
            product_form.save()
            images = image_form.cleaned_data['images']
            for image in images:
                ProductImage.objects.create(product=product, image=image)
                
            return redirect('vendor_admin')

    else:
        product_form = ProductForm(instance=product)
        image_form = ProductImageForm()
    
    return render(request, 'vendor/edit_product.html', {'product_form':product_form, 'image_form':image_form, 'product':product})

@login_required
def edit_vendor(request):
    vendor = request.user.vendor
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        
        if name:
            vendor.created_by.email = email
            vendor.created_by.save()
            
            vendor.name = name
            vendor.save()
            return redirect('vendor_admin')
    return render(request, 'vendor/edit_vendor.html', {'vendor':vendor})

def vendors(request):
    vendors = Vendor.objects.all()
    return render(request, 'vendor/vendors.html', {'vendors':vendors})

def vendor(request, vendor_id):
    vendor = get_object_or_404(Vendor, pk=vendor_id)
    return render(request, 'vendor/vendor.html', {'vendor':vendor})
