from django.db import models
from django.contrib.auth.models import User

from networking.models import BaseModel


class FriendsNetwork(BaseModel):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="friends_network")
    friends = models.ManyToManyField(User,symmetrical=False,blank=True)

class FriendRequest(BaseModel):
    STATUS_CHOICES = [
        ("sent", "Sent"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    ]

    from_user = models.ForeignKey(User, related_name="sent_requests", on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name="received_requests", on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS_CHOICES, max_length=10, default="sent")
    def __str__(self):
        return f"{self.from_user.email} - {self.to_user.email}"
