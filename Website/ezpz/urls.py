from django.conf.urls import include, url
from rest_framework import routers
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

# router for api routes
router = routers.SimpleRouter()
router.register(r'goods', views.GoodsViewSet)
router.register(r'services', views.ServicesViewSet)

urlpatterns = [
	url(r'^api/goods/(?P<category>.+)/$', views.GoodsManager.as_view()),
	url(r'^api/services/(?P<category>.+)/$', views.ServicesManager.as_view()),
	url('^api/', include(router.urls)),
	url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url('^.*$', views.IndexView.as_view(), name='index'),
]