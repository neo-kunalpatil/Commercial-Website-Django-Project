from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from apps.accounts.decorators import seller_required
from .models import Product, Category
from .forms import ProductForm
from django.db.models import Q

@seller_required
def seller_product_list(request):
    products = Product.objects.filter(seller=request.user).order_by('-created_at')
    return render(request, 'products/seller_product_list.html', {'products': products})

@seller_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            messages.success(request, 'Product created successfully!')
            return redirect('seller_product_list')
    else:
        form = ProductForm()
    return render(request, 'products/product_form.html', {'form': form, 'action': 'Create'})

@seller_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('seller_product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/product_form.html', {'form': form, 'action': 'Update'})

@seller_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('seller_product_list')
    return render(request, 'products/product_confirm_delete.html', {'product': product})

# ==========================================
# BUYER-FACING VIEWS
# ==========================================

def product_list(request):
    """
    Main product browsing view with search and filter functionality.
    """
    products = Product.objects.filter(available=True).order_by('-created_at')
    
    # Search Query
    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query)
        )
    
    # Category Filter
    category_slug = request.GET.get('category')
    if category_slug:
        products = products.filter(category__slug=category_slug)
        
    # Sorting
    sort_by = request.GET.get('sort')
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
        
    categories = Category.objects.all()
    
    context = {
        'products': products,
        'categories': categories,
        'search_query': query,
        'current_category': category_slug,
        'current_sort': sort_by,
    }
    return render(request, 'products/product_list.html', context)

def product_detail(request, pk):
    """
    Individual product detail page.
    """
    product = get_object_or_404(Product, pk=pk, available=True)
    categories = Category.objects.all()

    # Session tracking for Recently Viewed
    recently_viewed = request.session.get('recently_viewed', [])
    if pk in recently_viewed:
        recently_viewed.remove(pk)
    recently_viewed.insert(0, pk)
    request.session['recently_viewed'] = recently_viewed[:8] # Keep last 8

    # Recommendations
    related_products = Product.objects.filter(category=product.category, available=True).exclude(pk=pk)[:6]
    seller_products = Product.objects.filter(seller=product.seller, available=True).exclude(pk=pk)[:6]

    return render(request, 'products/product_detail.html', {
        'product': product,
        'categories': categories,
        'related_products': related_products,
        'seller_products': seller_products,
    })

def category_products(request, slug):
    """
    Browse products by a specific category slug.
    """
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, available=True).order_by('-created_at')
    
    context = {
        'category': category,
        'products': products,
        'categories': Category.objects.all(), # for sidebar
    }
    return render(request, 'products/category_products.html', context)
