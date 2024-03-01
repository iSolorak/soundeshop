import oscar.apps.catalogue.apps as apps
from django.urls import include, path

class CatalogueConfig(apps.CatalogueConfig):
    name = 'catalogue'



    def ready(self):
        from .views import FilterView
        super().ready()
        self.filtered_view = FilterView

    def get_urls(self):
        urls = super().get_urls()
        urls += [
            path('filtered_view/', self.filtered_view.as_view(), name='filtered_view'),
        ]
        return self.post_process_urls(urls)
