from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.generic import DetailView, ListView
from home_page.models import Product, ProductBrand, ProductType


class DescribeProduct(DetailView):
    product_types = ProductType.objects.all()
    product_brands = ProductBrand.objects.all()

    model = Product
    template_name = "product_details.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['product_types'] = self.product_types
        context['product_brands'] = self.product_brands
        self.products = Product.objects.filter(slug=self.kwargs['slug'])
        product = self.products[0]
        rated = []
        for x in range (0, product.product_rating):
            rated.append("*")
        unrated = []
        for x in range (0, 5-product.product_rating):
            unrated.append("x")
        context['rated'] = rated
        context['unrated'] = unrated
        return context


class DisplayTypeProducts(ListView):
    product_types = ProductType.objects.all()
    product_brands = ProductBrand.objects.all()

    template_name = "products_display.html"

    def get_queryset(self):
        self.product_type = get_object_or_404(ProductType, slug=self.kwargs['slug'])
        filter_word = self.kwargs['value']
        if filter_word == "high":
            return Product.objects.filter(product_type=self.product_type).order_by('-product_price')
        elif filter_word == "low":
            return Product.objects.filter(product_type=self.product_type).order_by('product_price')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_types'] = self.product_types
        context['product_brands'] = self.product_brands
        context['slug_name'] = self.kwargs['slug']
        context['url_to_access'] = "product_detail:DisplayTypeProducts"
        filter_word = self.kwargs['value']
        if filter_word == "high":
            context['filter'] = "high"
        elif filter_word == "low":
            context['filter'] = "low"
        return context


class DisplayBrandProducts(ListView):
    product_types = ProductType.objects.all()
    product_brands = ProductBrand.objects.all()

    template_name = "products_display.html"

    def get_queryset(self):
        self.product_brand = get_object_or_404(ProductBrand, slug=self.kwargs['slug'])
        filter_word = self.kwargs['value']
        if filter_word == "high":
            return Product.objects.filter(product_brand=self.product_brand).order_by("-product_price")
        elif filter_word == "low":
            return Product.objects.filter(product_brand=self.product_brand).order_by("product_price")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_types'] = self.product_types
        context['product_brands'] = self.product_brands
        context['slug_name'] = self.kwargs['slug']
        context['url_to_access'] = "product_detail:DisplayBrandProducts"
        filter_word = self.kwargs['value']
        if filter_word == "high":
            context['filter'] = "high"
        elif filter_word == "low":
            context['filter'] = "low"
        return context

