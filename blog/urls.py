from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^home/$', views.home, name='home'),
    url(r'^home-alt/$', views.homealt, name='home-alt'),
    url(r'^ftlon/$', views.blog_flton, name='blog_ftlon'),
    url(r'^nitn/$', views.blog_nitn, name='blog_nitn'),
    url(r'^ggb/$', views.blog_ggb, name='blog_ggb'),
    url(r'^lmk/$', views.blog_lmk, name='blog_lmk'),
    url(r'^sponsor/$', views.article_sponsor, name='article_sponsor'),
    url(r'^badlink/$', views.article_badlink, name='article_badlink'),
    url(r'^article/(?P<article_name>.*)/$', views.article_gen, name='article_gen'),
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
    url(r'^fact/(?P<permlink>.+)/$', views.fact_detail, name='fact_detail'),
    url(r'^convert/$', views.convert, name='convert'),
    url(r'^convert/answer/post$', views.conversion_answer_post, name='conversion_answer_post'),
    url(r'^convert/answer$', views.conversion_answer_get, name='conversion_answer_get'),
    url(r'^convert/base$', views.conversion_base, name='conversion_base'),
    url(r'^convert/unit$', views.conversion_unit, name='conversion_unit'),
    url(r'^quiz/$', views.quiz, name='quiz'),
    url(r'^ratio/$', views.ratio, name='ratio'),
    url(r'^ratio/answer/$', views.ratio, name='ratio'),
    url(r'^link/(?P<link>.*)/$', views.link_redirect, name="link-redirect"),
    url(r'^country/$', views.country, name="country"),
    url(r'^stat/(?P<stat>.+)$', views.stat, name='stat'),
    url(r'^links/save/$', views.links_save, name="links-save"),
    url(r'^ajax/comparison/$', views.comparison, name="comparison"),
    url(r'^ajax/quote/$', views.quote, name="quote"),
]