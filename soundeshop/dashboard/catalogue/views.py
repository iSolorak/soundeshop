# pylint: disable=attribute-defined-outside-init
from django.conf import settings
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views import generic
from django_tables2 import SingleTableMixin, SingleTableView

from oscar.core.loading import get_class, get_classes, get_model
from oscar.views.generic import ObjectLookupView
from oscar.apps.dashboard.catalogue.views import ProductListView as CoreProductListView
