from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('api/token/', views.obtain_token, name='token_obtain_pair'),
    path("job/add/", views.add_job, name="addjob"),
    path("job/query/", views.query_job, name="queryjob"),
    path("live/", views.live, name="live"),
]