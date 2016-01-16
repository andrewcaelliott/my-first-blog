from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.itabn, name='itabn'),
    url(r'^itabn/$', views.itabn, name='itabn'),
    url(r'^itabn/answer/post$', views.query_answer_post, name='query_answer_post'),
    url(r'^itabn/answer$', views.query_answer_get, name='query_answer_get'),
    url(r'^itabn/compare$', views.query_compare, name='query_compare'),
    url(r'^itabn/api$', views.query_api, name='query_api'),
    url(r'^posts/$', views.post_list, name='post_list'),
    url(r'^facts/$', views.fact_list, name='fact_list'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail, name='post_detail'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^fact/new/$', views.fact_new, name='fact_new'),
    url(r'^fact/(?P<pk>[0-9]+)/$', views.fact_detail, name='fact_detail'),
    url(r'^convert/$', views.convert, name='convert'),
    url(r'^convert/answer/post$', views.conversion_answer_post, name='conversion_answer_post'),
    url(r'^convert/answer$', views.conversion_answer_get, name='conversion_answer_get'),
    url(r'^convert/base$', views.conversion_base, name='conversion_base'),
    url(r'^convert/unit$', views.conversion_unit, name='conversion_unit'),
]