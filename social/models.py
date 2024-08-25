from django.db import models
from django.contrib.auth.models import User

# Model to manage follow relationships between users
class UserFollows(models.Model):
    # The user who is following another user
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,  # If the user is deleted, the follow relationship is also deleted
        related_name="following"  # Allows access to all users this user is following
    )
    
    # The user who is being followed
    followed_user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,  # If the followed user is deleted, the follow relationship is also deleted
        related_name="followers"  # Allows access to all users who follow this user
    )

    class Meta:
        # Ensures that each follow relationship between two users is unique
        unique_together = ("user", "followed_user")

    def __str__(self):
        # Returns a descriptive string indicating who follows whom
        return f"{self.user.username} follows {self.followed_user.username}"
