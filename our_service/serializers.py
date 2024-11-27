from rest_framework import serializers
from .models import Service, ServiceStep, ServiceOrder, ServiceOrderStep
from auth_flow.models import AllUsers as User

class ServiceStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceStep
        fields = ['id', 'name', 'status', 'requirements_files', 'files', 'data_req_user', 'step_price', 'payment_status']

class ServiceSerializer(serializers.ModelSerializer):
    steps = ServiceStepSerializer(many=True)

    class Meta:
        model = Service
        fields = ['id', 'name', 'description', 'sub_description', 'total_price', 'steps']
        
    
    def create(self, validated_data):
        # Extract the steps data
        steps_data = validated_data.pop('steps')
        
        # Create the Service instance
        service = Service.objects.create(**validated_data)
        
        # Create each step and associate it with the service
        for step_data in steps_data:
            ServiceStep.objects.create(service=service, **step_data)
        return service
    
    
    def update(self, instance, validated_data):
        # Extract the steps data
        steps_data = validated_data.pop('steps', None)

        # Update basic service data
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.sub_description = validated_data.get('sub_description', instance.sub_description)
        instance.total_price = validated_data.get('total_price', instance.total_price)
        instance.save()

        # Update the steps if they are provided
        if steps_data is not None:
            # First, delete existing steps if they are not included in the request
            instance.steps.all().delete()

            # Then, create new steps
            for step_data in steps_data:
                ServiceStep.objects.create(service=instance, **step_data)

        return instance


class ServiceOrderStepSerializer(serializers.ModelSerializer):
    step = ServiceStepSerializer()

    class Meta:
        model = ServiceOrderStep
        fields = ['id', 'step', 'status', 'files', 'payment_status']

class ServiceOrderSerializer(serializers.ModelSerializer):
    steps = ServiceOrderStepSerializer(many=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    assigned_employee = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)

    class Meta:
        model = ServiceOrder
        fields = ['id', 'user', 'service', 'status', 'assigned_employee', 'created_at', 'steps']

    def create(self, validated_data):
        steps_data = validated_data.pop('steps')
        order = ServiceOrder.objects.create(**validated_data)
        for step_data in steps_data:
            step = ServiceStep.objects.get(id=step_data['step'].id)
            ServiceOrderStep.objects.create(order=order, step=step, **step_data)
        return order

    def update(self, instance, validated_data):
        steps_data = validated_data.pop('steps', [])
        instance.status = validated_data.get('status', instance.status)
        instance.assigned_employee = validated_data.get('assigned_employee', instance.assigned_employee)
        instance.save()

        for step_data in steps_data:
            step = ServiceStep.objects.get(id=step_data['step'].id)
            ServiceOrderStep.objects.create(order=instance, step=step, **step_data)

        return instance
    
    
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceOrder
        fields = ['id', 'service', 'user', 'status', 'created_at']

    def create(self, validated_data):
        # Get the user from the request context
        user = self.context['request'].user
        
        # Get the service from the validated data (service ID)
        service_id = validated_data['service']  # Ensure this is the ID, not the object
        try:
            service = Service.objects.get(id=service_id)  # This retrieves the service by ID
        except Service.DoesNotExist:
            raise serializers.ValidationError("Service not found")

        # Create the order and associate it with the user and service
        order = ServiceOrder.objects.create(
            service=service,  # Pass the Service object
            user=user, 
            status="new"
        )

        # Import steps from the service to the order
        for step in service.steps.all():
            # Associate each step with the new order
            ServiceStep.objects.create(
                order=order,
                service=service,
                name=step.name,
                status=step.status,
                requirements_files=step.requirements_files,
                files=step.files,
                data_req_user=step.data_req_user,
                step_price=step.step_price,
                payment_status=step.payment_status
            )

        return order
