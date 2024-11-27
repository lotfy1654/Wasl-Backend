from django.shortcuts import render

# Create your views here.
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Service, ServiceOrder, ServiceOrderStep
from .serializers import ServiceSerializer, ServiceOrderSerializer , ServiceOrderStepSerializer ,OrderSerializer
from rest_framework.response import Response 
from rest_framework import status
from rest_framework.views import APIView


# Admin Views for Services
class ServiceCreateView(generics.CreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAdminUser]

class ServiceListView(generics.ListAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAdminUser]

class ServiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAdminUser]
    

class ServiceDeleteView(generics.DestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAdminUser]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()

        message = {
            "message": "Service deleted successfully"
        }
        
        return Response(status=status.HTTP_204_NO_CONTENT , data=message)

# Order Views
class ServiceOrderCreateView(generics.CreateAPIView):
    queryset = ServiceOrder.objects.all()
    serializer_class = ServiceOrderSerializer
    permission_classes = [IsAuthenticated]

class ServiceOrderListView(generics.ListAPIView):
    queryset = ServiceOrder.objects.all()
    serializer_class = ServiceOrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return ServiceOrder.objects.filter(user=user)

class ServiceOrderDetailView(generics.RetrieveUpdateAPIView):
    queryset = ServiceOrder.objects.all()
    serializer_class = ServiceOrderSerializer
    permission_classes = [IsAuthenticated]

class ServiceOrderStepUpdateView(generics.UpdateAPIView):
    queryset = ServiceOrderStep.objects.all()
    serializer_class = ServiceOrderStepSerializer
    permission_classes = [IsAuthenticated]

class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Get service_id from the request body
        service_id = request.data.get("service_id")
        if not service_id:
            return Response({"detail": "Service ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch the service using the provided ID
        try:
            service = Service.objects.get(id=service_id)
        except Service.DoesNotExist:
            return Response({"detail": "Service not found."}, status=status.HTTP_404_NOT_FOUND)

        print(service)
            
        # Create the order with the service ID and user ID (passing only the primary keys)
        order_data = {
            'service': service,  
            'user': request.user.id,  # Pass the ID of the user
        }

        # Use the OrderSerializer to create the order
        serializer = OrderSerializer(data=order_data, context={'request': request})
        if serializer.is_valid():
            order = serializer.save()  # This will automatically create the order and steps
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
