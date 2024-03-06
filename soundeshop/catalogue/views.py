from oscar.apps.catalogue.views import CatalogueView as CoreCatalogueView
from urllib.parse import quote

from django.contrib import messages
from django.core.paginator import InvalidPage
from django.http import Http404, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, TemplateView

from oscar.apps.catalogue.signals import product_viewed
from oscar.core.loading import get_class, get_model
from django.template.loader import render_to_string
from django.http import JsonResponse
from .search_handlers import SimpleProductFilteredHandler
import json


Product = get_model("catalogue", "product")
Category = get_model("catalogue", "category")
ProductAlert = get_model("customer", "ProductAlert")
ProductAlertForm = get_class("customer.forms", "ProductAlertForm")
get_product_search_handler_class = get_class(
    "catalogue.search_handlers", "get_product_search_handler_class"
)
ProductClass = get_model("catalogue", "ProductClass")

class CatalogueView(CoreCatalogueView):
    """
    Browse all products in the catalogue
    """

    context_object_name = "products"
    template_name = "oscar/catalogue/browse.html"

    def get(self, request, *args, **kwargs):
        try:
            # pylint: disable=attribute-defined-outside-init
            self.search_handler = self.get_search_handler(
                self.request.GET, request.get_full_path(), []
            )
            response = super().get(request, *args, **kwargs)
        except InvalidPage:
            # Redirect to page one.
            messages.error(request, _("The given page number was invalid."))
            return redirect("catalogue:index")
        return response

    def get_search_handler(self, *args, **kwargs):
        return get_product_search_handler_class()(*args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = {}
        ctx["summary"] = _("All products")
        search_context = self.search_handler.get_search_context_data(
            self.context_object_name
        )
        ctx.update(search_context)
        ctx['categories'] = Category.objects.prefetch_related()
        ctx['product_types'] = ProductClass.objects.all()
        return ctx
    
class FilterView(CoreCatalogueView):

    """
    Browse all products in the catalogue
    """

    context_object_name = "products"
    template_name = "oscar/catalogue/hello.html"

    def get(self, request, *args, **kwargs):
        try:
            # pylint: disable=attribute-defined-outside-init
            # post_data = json.loads(self.request.body.decode("utf-8"))
            # print(self.request.GET)
            self.search_handler = self.get_search_handler(
                self.request.GET, request.get_full_path(), []
            )
            response = super().get(request, *args, **kwargs)
        except InvalidPage:
            # Redirect to page one.
            messages.error(request, _("The given page number was invalid."))
            return redirect("catalogue:index")
        # print(dir(response))
        # print(dir(response.render()))
        # print(response.render().rendered_content)
        rd_content = response.render().rendered_content
        return JsonResponse({'inner_HTML':rd_content,},safe=False)


    def get_search_handler(self, *args, **kwargs):
        return SimpleProductFilteredHandler(*args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = {}
        ctx["summary"] = _("All products")
        search_context = self.search_handler.get_search_context_data(
            self.context_object_name
        )
        ctx.update(search_context)
        ctx['categories'] = Category.objects.prefetch_related()
        ctx['product_types'] = ProductClass.objects.all()
        return ctx
