from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import DetailView, ListView
from django.shortcuts import render, get_object_or_404
from home_page.models import Product, ProductType, ProductBrand
from django.shortcuts import reverse
from django.db.models.functions import Lower


def search(request):
    search_word = request.GET['search_word']
    return HttpResponseRedirect(reverse("search_and_suggest:SearchRelatedProducts",
                                        kwargs={'slug': search_word, 'value': "low"}))


class SearchRelatedProducts(ListView):
    product_types = ProductType.objects.all()
    product_brands = ProductBrand.objects.all()

    template_name = "products_display.html"

    def get_queryset(self):
        self.product_name = self.kwargs['slug']
        self.product_type = None
        self.product_brand = None
        try:
            self.product_type = ProductType.objects.filter(type__icontains=self.kwargs['slug'])
            """self.product_type = get_object_or_404(ProductType, type=self.kwargs['slug'])"""
        except:
            pass

        try:
            self.product_brand = ProductBrand.objects.filter(brand__icontains=self.kwargs['slug'])
            """self.product_brand = get_object_or_404(ProductBrand, brand=self.kwargs['slug'])"""
        except:
            pass
        """qs = Product.objects.filter(product_name=self.product_name).filter(product_type=self.product_type). \
            filter(product_brand=self.product_brand)"""

        qs = Product.objects.none()
        for p_type in self.product_type:
            qs = qs | Product.objects.filter(product_type=p_type)

        for p_brand in self.product_brand:
            qs = qs | Product.objects.filter(product_brand=p_brand)

        qs |= Product.objects.filter(product_name__icontains=self.product_name)
        filter_word = self.kwargs['value']
        if filter_word == "high":
            return qs.order_by("-product_price")
        elif filter_word == "low":
            return qs.order_by("product_price")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_types'] = self.product_types
        context['product_brands'] = self.product_brands
        context['slug_name'] = self.kwargs['slug']
        context['url_to_access'] = "search_and_suggest:SearchRelatedProducts"
        filter_word = self.kwargs['value']
        if filter_word == "high":
            context['filter'] = "high"
        elif filter_word == "low":
            context['filter'] = "low"
        return context
