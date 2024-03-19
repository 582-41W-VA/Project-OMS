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
    #orderID = models.AutoField(primary_key=True)
    #userID = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='media/')
    description = models.TextField(null=True, blank=True)
    #orderAssignedTo = models.ForeignKey(User, on_delete=models.SET_NULL)
    priority = models.CharField(max_length=50, choices=PRIORITY)
    status = models.CharField(max_length=50, choices=STATUS, default='Pending')
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return str(self.title)


class Comment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    commentText = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    

    def __str__(self):
        return str(self.commentText)[:20]