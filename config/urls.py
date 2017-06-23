"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static

from widgets import views as widget_views

urlpatterns = [
    url(r'^$', auth_views.login, {'template_name': 'home.html', 'redirect_authenticated_user': True}, name='login'),
    url(r'^logout_user/$', auth_views.logout, name='logout'),
    url(r'^register_user/$', widget_views.RegistrationUserView.as_view(), name='register'),
    url(r'^personalized/$', widget_views.personalized, name='personalized'),
    url(r'^update_background/$', widget_views.update_background, name='update_background'),
    url(r'^users_widgets/$', widget_views.users_widgets, name='users_widgets'),
    url(r'^update_count/$', widget_views.update_count, name='update_count'),
    url(r'^admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
