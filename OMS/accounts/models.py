from django.contrib.auth.models import User
from django.db import models

class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Complete', 'Complete'),
        ('Attention Required', 'Attention Required')
    )

    PRIORITY = (
        ('Urgent', 'Urgent'),
        ('Normal', 'Normal')
    )
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='media/')
    description = models.TextField(null=True, blank=True)
    priority = models.CharField(max_length=50, choices=PRIORITY)
    status = models.CharField(max_length=50, choices=STATUS, default='Pending')
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_by')
    order_assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assigned_orders', blank=True)
    
    def __str__(self):
        return str(self.title)


class Comment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='comments')
    comment_text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.comment_text} - {self.user}"
