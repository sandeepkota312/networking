from django.db import models
from django.contrib.auth.models import AbstractUser
from networking.models import BaseModel

from django.contrib.auth import get_user_model



class User(AbstractUser):
    email = models.EmailField(unique=True, db_index=True)
    username = models.CharField(max_length=150, unique=True, db_index=True)

class FriendsNetwork(BaseModel):
    user = models.OneToOneField(get_user_model(),on_delete=models.CASCADE,related_name="friends_network",db_index=True)
    friends = models.ManyToManyField(get_user_model(),symmetrical=False,blank=True)

class FriendRequest(BaseModel):
    STATUS_CHOICES = [
        ("sent", "Sent"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    ]

    from_user = models.ForeignKey(get_user_model(), related_name="sent_requests", on_delete=models.CASCADE)
    to_user = models.ForeignKey(get_user_model(), related_name="received_requests", on_delete=models.CASCADE,db_index=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=10, default="sent",db_index=True)
    def __str__(self):
        return f"{self.from_user.email} - {self.to_user.email}"
