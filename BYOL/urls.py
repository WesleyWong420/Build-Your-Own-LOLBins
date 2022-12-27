"""
WESLEY WONG KEE HAN
TP059618 APU3F2205CS(CYB)

Project URLs Definition
"""

from django.contrib import admin
from django.urls import path, include
import debug_toolbar

urlpatterns = [
    path('admin/', admin.site.urls, name="admin"),
    path('', include('base.urls')),
]

handler404 = "base.views.notFound"