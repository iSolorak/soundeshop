from django.shortcuts import render
from django.http import HttpResponse
from oscar.core.loading import get_model

Product = get_model('catalogue','Product')
ProductClass = get_model("catalogue", "ProductClass")

Category = get_model('catalogue','Category')
# Create your views here.
def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    product_types = ProductClass.objects.values_list('name',flat=True).distinct()
    return render(request,'home.html',{'products':products,'categories':categories,'product_types':product_types})