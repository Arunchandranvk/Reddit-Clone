from django.db import models
from  accounts import models as user_models
from images import models as image_models



class Notification(image_models.TimeStampedModel):

    TYPE_CHOICES = (
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('follow', 'Follow')
    )

    creator = models.ForeignKey(user_models.CustomUser, related_name='creator',on_delete=models.CASCADE)
    to = models.ForeignKey(user_models.CustomUser, related_name='to',on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    image = models.ForeignKey(image_models.Image, null=True, blank=True,on_delete=models.CASCADE)
    comment = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return 'From: {} - To: {}'.format(self.creator, self.to)