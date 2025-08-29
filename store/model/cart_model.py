from django.db import models
from store.model.users import User
from django.contrib.postgres.fields import JSONField 

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')  
    products = models.JSONField(default=list)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'cart'
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'
    
    def __str__(self):
        return f"Cart of {self.user.username} - {len(self.products)} items"
