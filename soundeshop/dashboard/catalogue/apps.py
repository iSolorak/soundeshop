import oscar.apps.dashboard.catalogue.apps as apps
# from .views import ProductListView
from django.urls import path, re_path
from oscar.core.loading import get_class
# from .views import ProductListView
import django
# from .views import ProductListsView
class CatalogueDashboardConfig(apps.CatalogueDashboardConfig):
    name = 'dashboard.catalogue'

    # def ready(self):
    #     super().ready()
    #     from .views import ProductListView
    #     self.product_lists_view = ProductListView



    def get_urls(self):
        urls = super().get_urls()
        return self.post_process_urls(urls)