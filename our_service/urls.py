from django.urls import path
from .views import (
    ServiceCreateView,
    ServiceListView,
    ServiceDetailView,
    ServiceDeleteView,
    ServiceOrderCreateView,
    ServiceOrderListView,
    ServiceOrderDetailView,
    ServiceOrderStepUpdateView, 
    CreateOrderView
)

urlpatterns = [
    # Services
    path('create', ServiceCreateView.as_view(), name='service-create'),
    path('', ServiceListView.as_view(), name='service-list'),
    path('<int:pk>', ServiceDetailView.as_view(), name='service-detail'),
    path('<int:pk>/delete', ServiceDeleteView.as_view(), name='service-delete'),

    # Orders
    path('orders/create/', CreateOrderView.as_view(), name='order-create'),
    path('orders/', ServiceOrderListView.as_view(), name='order-list'),
    path('orders/<int:pk>/', ServiceOrderDetailView.as_view(), name='order-detail'),
    
    # Order Steps
    path('order-steps/<int:pk>/update/', ServiceOrderStepUpdateView.as_view(), name='order-step-update'),
]

