
from django.urls import path



from .views import AboutUsList , AboutUsDetail , AboutUsUpdate , AboutUsCreate , AboutUsDelete



urlpatterns = [
    path('', AboutUsList.as_view() , name='about_us_list'),
    path('detail/<int:pk>/', AboutUsDetail.as_view() , name='about_us_detail'),
    path('update/<int:pk>', AboutUsUpdate.as_view() , name='about_us_update'),
    path('create', AboutUsCreate.as_view() , name='about_us_create'),
    path('delete/<int:pk>', AboutUsDelete.as_view() , name='about_us_delete'),
]