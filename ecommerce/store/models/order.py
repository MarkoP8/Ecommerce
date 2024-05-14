from django.db import models
from . import user

class Order(models.Model):
    user = models.ForeignKey(user.User, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now=True)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"Order: {str(self.id)} for {self.user} - {self.user.email}"