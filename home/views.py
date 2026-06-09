from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from products.models import Product
from . import tasks
from django.contrib import messages


class HomeView(View):
    def get(self, request):
        products = Product.objects.filter(available=True)
        return render(request, 'home/index.html', {'products': products})


class ProductDetailView(View):
    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        return render(request, 'home/product_detail.html', {'product': product})


class BucketHomeView(View):
    template_name = 'home/bucket.html'

    def get(self, request):
        objects = tasks.get_all_bucket_objects()
        return render(request, self.template_name, {'objects': objects})


class DeleteBucketObjectView(View):
    def get(self, request, key):
        tasks.delete_object_task.delay(key)
        messages.success(request, 'Bucket Object will be Deleted Soon', 'info')
        return redirect('home:bucket')