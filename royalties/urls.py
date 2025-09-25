"""
URL configuration for royalties project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include

from royalties.admin.admin import admin_site
from royalties.views.home import HomeView
from royalties.views.royalty import (RoyaltyListView, RoyaltyDetailView, RoyaltyUpdateView, update_royalty,
                                     create_royalty)
from royalties.views.payment import PaymentUpdateView
from royalties.views.supplier import SupplierUpdateView
from royalties.views.diffusion import DiffusionUpdateView, DiffusionListView, DiffusionCreateView, DiffusionDetailView
from royalties.views.account import LoginView, LogoutView


# ADMIN
urlpatterns = [
    path('grappelli/', include('grappelli.urls')), # grappelli URLS
    # path('admin/', admin.site.urls),
    path('admin/', admin_site.urls),
]

# HOME

urlpatterns += [
    path('', HomeView.as_view(), name='home'),
]

# ACCOUNT
account_patterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

urlpatterns += [
    path('account/', include((account_patterns, 'account'))),
]


# SHOW ROYALTIES

urlpatterns += [
    path('royalties/show', RoyaltyListView.as_view(), name='royalty-list'),
    path('royalties/<int:pk>/', RoyaltyDetailView.as_view(), name='royalty-detail'),
    path('royalties/<int:pk>/edit', RoyaltyUpdateView.as_view(), name='royalty-edit'),
    # path('royalties/<int:pk>/edit', update_royalty, name='royalty-edit'),
    path('royalty/create', create_royalty, name='royalty-create'),
]


# SHOW PAYEMNT

urlpatterns += [
    path('payment/<int:pk>/edit', PaymentUpdateView.as_view(), name='payment-update')
]


# SHOW SUPPLIER

urlpatterns += [
    path('supplier/<int:pk>/edit', SupplierUpdateView.as_view(), name='supplier-update')
]

# SHOW DIFFUSION

urlpatterns += [
    path('diffusion/<int:pk>/edit', DiffusionUpdateView.as_view(), name='diffusion-edit'),
    path('diffusion/', DiffusionListView.as_view(), name='diffusion-list'),
    path('diffusion/create', DiffusionCreateView.as_view(), name='diffusion-create'),
    path('diffusion/<int:pk>/detail', DiffusionDetailView.as_view(), name='diffusion-detail'),
]