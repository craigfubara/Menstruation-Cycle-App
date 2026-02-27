"""StainStrong URL Configuration"""

from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', include('Home.urls')),
    path('', views.index, name='index'),
    path('account/', include('App_Login.urls')),
    path('blog/', include('App_Blog.urls')),
    path('tracker/', include('App_Tracker.urls')),
    path('community/', include('App_Community.urls')),
    path('lifestyle/', include('App_Lifestyle.urls')),
    path('api/', include('App_Tracker.api_urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
