from django.shortcuts import render
from apps.products.models import Product, Category

def home(request):
    """
    Homepage for the Amazon Marketplace.
    Shows categories and the latest products.
    """
    # Fetch all categories to display on the homepage
    categories = Category.objects.all()
    
    # Fetch the latest available products (limit to 8 for a clear grid)
    latest_products = Product.objects.filter(available=True).order_by('-created_at')[:8]
    
    context = {
        'categories': categories,
        'latest_products': latest_products,
    }
    return render(request, 'core/home.html', context)
