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
from royalties.views.royalty import ShowRoyaltiesView
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
    path('royalties/show', ShowRoyaltiesView.as_view(), name='royalties'),
]


