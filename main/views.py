from django.shortcuts import render
from product.models import Product

def frontpage(request):
    newest_products = Product.objects.all()[:8]
    return render(request, 'main/frontpage.html', {'newest_products':newest_products})

def contact(request):
    return render(request, 'main/contact.html')
