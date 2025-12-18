from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .models import Product
from .filters import ProductFilter
from .forms import ProductForm
from .decorators import role_required


@login_required
@role_required(allowed_roles=['admin'])
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'shop/product_form.html', {'form': form})

@login_required
@role_required(allowed_roles=['admin'])
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'shop/product_form.html', {'form': form})

@login_required
@role_required(allowed_roles=['admin'])
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if product.orderitem_set.exists():
        return render(request, 'shop/product_confirm_delete.html', {'product': product, 'error': 'Этот товар нельзя удалить, так как он присутствует в заказах.'})
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'shop/product_confirm_delete.html', {'product': product})


def product_list(request):
    products = Product.objects.all()
    
    sort_by = request.GET.get('sort')
    if sort_by:
        products = products.order_by(sort_by)

    product_filter = ProductFilter(request.GET, queryset=products)
    products = product_filter.qs

    return render(request, 'shop/product_list.html', {'products': products, 'filter': product_filter})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('product_list')
    else:
        form = AuthenticationForm()
    return render(request, 'shop/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('product_list')