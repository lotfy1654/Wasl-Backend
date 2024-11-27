from django.db import models
from auth_flow.models import AllUsers as User

STATUS_CHOICES_Step = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('in_progress', 'In Progress'),  
]

Order_Status = [
    ('new', 'New'),
    ('in_progress', 'In Progress'),
    ('completed', 'Completed'),
]

payment_status = [
    ('pending', 'Pending'),
    ('paid', 'Paid'),
    ('unpaid', 'Unpaid'),
]

class Service(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    sub_description = models.TextField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class ServiceStep(models.Model):
    order = models.ForeignKey(ServiceOrder, related_name="steps_order", on_delete=models.CASCADE)
    service = models.ForeignKey(Service, related_name="steps", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES_Step, default="pending")
    requirements_files = models.TextField(null=True, blank=True)
    files = models.FileField(upload_to="service_steps/", null=True, blank=True)
    data_req_user = models.TextField(null=True, blank=True)
    step_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_status = models.CharField(max_length=255, choices=payment_status, default="unpaid")

    def __str__(self):
        return f"Step {self.name} of {self.service.name}"

class ServiceOrder(models.Model):
    user = models.ForeignKey(User, related_name="service_orders", on_delete=models.CASCADE)
    service = models.ForeignKey(Service, related_name="orders", on_delete=models.CASCADE)
    status = models.CharField(max_length=255, choices=Order_Status, default="new")
    assigned_employee = models.ForeignKey(User, related_name="assigned_orders", on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"
    



class ServiceOrderStep(models.Model):
    order = models.ForeignKey(ServiceOrder, related_name="steps", on_delete=models.CASCADE)
    step = models.ForeignKey(ServiceStep, related_name="order_steps", on_delete=models.CASCADE)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES_Step, default="pending")
    files = models.FileField(upload_to="order_steps/", null=True, blank=True)
    payment_status = models.CharField(max_length=255, choices=payment_status, default="unpaid")

    def __str__(self):
        return f"Step {self.step.name} for Order {self.order.id}"
