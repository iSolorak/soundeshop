from oscar.apps.catalogue.search_handlers import SimpleProductSearchHandler as CoreSimpleProductSearchHandler
from django.conf import settings
from django.utils.module_loading import import_string
from django.views.generic.list import MultipleObjectMixin

from oscar.core.loading import get_class, get_classes, get_model
from django.db.models import Q
from decimal import Decimal as D


BrowseCategoryForm = get_class("search.forms", "BrowseCategoryForm")
SearchHandler, SearchResultsPaginationMixin = get_classes(
    "search.search_handlers", ("SearchHandler", "SearchResultsPaginationMixin")
)
is_solr_supported = get_class("search.features", "is_solr_supported")
is_elasticsearch_supported = get_class("search.features", "is_elasticsearch_supported")
Product = get_model("catalogue", "Product")

class SimpleProductSearchHandler(CoreSimpleProductSearchHandler):
    """
    A basic implementation of the full-featured SearchHandler that has no
    faceting support, but doesn't require a Haystack backend. It only
    supports category browsing.

    Note that is meant as a replacement search handler and not as a view
    mixin; the mixin just does most of what we need it to do.
    """

    paginate_by = settings.OSCAR_PRODUCTS_PER_PAGE

    # pylint: disable=unused-argument
    def __init__(self, request_data, full_path, categories=None):
        self.request_data = request_data
        self.categories = categories
        self.kwargs = {"page": request_data.get("page") or 1}
        self.object_list = self.get_queryset()

    def get_queryset(self):
        qs = Product.objects.browsable().base_queryset()
        if self.categories:
            qs = qs.filter(categories__in=self.categories).distinct()
        print(self.request_data)
        return qs

    def get_search_context_data(self, context_object_name):
        # Set the context_object_name instance property as it's needed
        # internally by MultipleObjectMixin
        self.context_object_name = context_object_name
        context = self.get_context_data(object_list=self.object_list)
        context[context_object_name] = context["page_obj"].object_list
        return context


class SimpleProductFilteredHandler(CoreSimpleProductSearchHandler):
    """
    A basic implementation of the full-featured SearchHandler that has no
    faceting support, but doesn't require a Haystack backend. It only
    supports category browsing.

    Note that is meant as a replacement search handler and not as a view
    mixin; the mixin just does most of what we need it to do.
    """

    paginate_by = settings.OSCAR_PRODUCTS_PER_PAGE

    # pylint: disable=unused-argument
    def __init__(self, request_data, full_path, categories=None):
        self.request_data = request_data
        self.categories = categories
        self.kwargs = {"page": request_data.get("page") or 1}
        self.object_list = self.get_queryset()

    def get_queryset(self):
        qs = Product.objects.browsable().base_queryset()
        filter_list = self.request_data.getlist('category')
        product_classfilter = self.request_data.getlist('product_class')
        price_min = self.request_data.get('min_price')
        price_max = self.request_data.get('max_price')
        if len(filter_list)>0:
            qs = qs.filter(categories__name__in=filter_list).distinct()
        if len(product_classfilter)>0:
            qs = qs.filter(product_class__name__in=product_classfilter)
        if len(price_min)>0:
            q = Q(stockrecords__price__range=(float(price_min),float(price_max)))
            qs = qs.filter(q)
        return qs

    def get_search_context_data(self, context_object_name):
        # Set the context_object_name instance property as it's needed
        # internally by MultipleObjectMixin
        self.context_object_name = context_object_name
        context = self.get_context_data(object_list=self.object_list)
        context[context_object_name] = context["page_obj"].object_list
        return context