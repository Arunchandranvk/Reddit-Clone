from rest_framework import serializers
from .models import *

from django.contrib.auth import get_user_model

# class CommunitySerializer(serializers.ModelSerializer):
#     followers_count = serializers.ReadOnlyField()
    
#     class Meta:
#         model=Community
#         fields = [
#             'community_name',
#             'image',
#             'content',
#             'user',
#             'followers',
#             'followers_count'
#         ]



User = get_user_model()

class CommunitySerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    followers = serializers.SerializerMethodField()

    class Meta:
        model = Community
        fields = ['id', 'community_name', 'image', 'content', 'user', 'followers', 'user_name']
        extra_kwargs = {
            'followers': {'required': False}
        }

    def get_followers(self, obj):
        followers_data = []
        for follower in obj.followers.all():
            follower_data = {
                'user_id': follower.id,
                'username': follower.username
            }
            followers_data.append(follower_data)
        return followers_data

    def create(self, validated_data):
        followers_data = validated_data.pop('followers', [])
        community = Community.objects.create(**validated_data)
        community.followers.set(followers_data)
        return community