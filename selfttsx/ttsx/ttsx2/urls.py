from django.conf.urls import url
import views
urlpatterns = [
    url(r'^$',views.index),
    url(r'^list(\d+)_(\d+)/$',views.goods_list),
    url(r'^detail(\d+)_(\d+)/$',views.detail),
]
