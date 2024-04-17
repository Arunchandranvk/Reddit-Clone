from django.db import models
from accounts.models import CustomUser
# Create your models here.

class Community(models.Model):
    community_name=models.CharField(max_length=100)
    image=models.FileField(upload_to="community_image")
    content=models.TextField(null=True)
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="c_user")
    followers = models.ManyToManyField(CustomUser, related_name="communities_following", blank=True)
    
    
    def _str_(self):
        return self.community_name

    @property
    def followers_count(self):
        return self.followers.all().count()
    

class CommunityPost(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name="posts")
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    image = models.FileField(upload_to="community_posts",null=True)
    caption = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"Post by {self.author.username} in {self.community.community_name}"
