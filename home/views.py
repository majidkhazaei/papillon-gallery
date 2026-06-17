from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from products.models import Product, Category
from . import tasks
from django.contrib import messages
from utils import IsAdminMixin
from orders.forms import CartAddForm


class HomeView(View):
    def get(self, request, category_slug=None):
        products = Product.objects.filter(available=True)
        categories = Category.objects.filter(is_sub=False)
        if category_slug:
            category = Category.objects.get(slug=category_slug)
            products = products.filter(category=category)
        return render(request, 'home/index.html', {'products': products, 'categories': categories})


class ProductDetailView(View):
    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        form = CartAddForm()
        variants = product.variants.all()
        return render(request, 'home/product_detail.html', {
            'product': product,
            'form': form,
            'variants': variants,
        })


class BucketHomeView(IsAdminMixin,View):
    template_name = 'home/bucket.html'

    def get(self, request):
        objects = tasks.get_all_bucket_objects()
        return render(request, self.template_name, {'objects': objects})


class DeleteBucketObjectView(IsAdminMixin, View):
    def get(self, request, key):
        tasks.delete_object_task.delay(key)
        messages.success(request, 'Bucket Object will be Deleted Soon', 'info')
        return redirect('home:bucket')


class DownloadBucketObjectView(IsAdminMixin, View):
    def get(self, request, key):
        tasks.download_object_task.delay(key)
        messages.success(request, 'Bucket Object will be Downloaded Soon', 'info')
        return redirect('home:bucket')