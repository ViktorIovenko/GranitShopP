from django.shortcuts import render
from .models import Product
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product/product_detail.html', {'product': product})

def index(request):
    all_products = Product.objects.all()
    paginator = Paginator(all_products, 6)  # Определяем, сколько товаров отображать на каждой странице
    page = request.GET.get('page')  # Получаем номер текущей страницы из параметров GET
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)  # Если параметр page не является целым числом, показываем первую страницу
    except EmptyPage:
        products = paginator.page(paginator.num_pages)  # Если параметр page превышает общее количество страниц, показываем последнюю страницу
    return render(request, 'index.html', {'products': products})
