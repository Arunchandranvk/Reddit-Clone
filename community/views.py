from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework import status
from notifications import views
from rest_framework.permissions import IsAuthenticated

# Create your views here.


# class CommunityView(APIView):
#     def get(self,request):
#         com=Community.objects.all()
#         ser=CommunitySerializer(com,many=True)
#         return Response({'status':1,'data':ser.data})
#     def post(self,request):
#         user=request.user
#         ser=CommunitySerializer(data=request.data)
#         if ser.is_valid():
#             ser.save(user=user)
#             response_data = {
#             'message': 'Community Created successfully',
#             'user': ser.data
#             }
#             return Response({'status':1,'data':response_data},status=status.HTTP_201_CREATED)
#         else:
#             return Response({'status':1,"Msg":ser.errors},status=status.HTTP_400_BAD_REQUEST)

# class MyCommunity(APIView):
#     def get(self,request):
#         user=request.user
#         com=Community.objects.filter(user=user)        
#         ser=CommunitySerializer(com)
#         return Response({'status':1,'data':ser.data})
#     def put(self,request):
#         user= request.user
#         try:
#             com=Community.objects.get(user=user)
#             ser=CommunitySerializer(data=request.data,instance=com) 
#             if ser.is_valid():
#                 ser.save()
#                 return Response({'status':1,"msg":"Community Updated"})
#             else:
#                 return Response({'status':0,"msg":ser.errors},status=status.HTTP_422_UNPROCESSABLE_ENTITY)
#         except:
#             return Response({'status':0,"msg":"Invalid ID"},status=status.HTTP_400_BAD_REQUEST)


# class FollowCommunity(APIView):

#     def post(self, request, **kwargs):

#         user = request.user
        
#         try:
#             id=kwargs.get('pk')
#             print(id)
#             community_to_follow = Community.objects.get(id=id)
#             print(community_to_follow)
#         except Community.DoesNotExist:
#             return Response({'status':0},status=status.HTTP_404_NOT_FOUND)

#         user.community.add(community_to_follow)
#         community_to_follow.followers.add(community_to_follow)
#         community_to_follow.save()
#         user.save()

#         views.create_notification(user, community_to_follow, 'follow')

#         return Response({'status':1},status=status.HTTP_200_OK)


# class UnFollowUser(APIView):

#     def post(self, request, user_id, format=None):

#         user = request.user

#         try:
#             user_to_follow = CustomUser.objects.get(id=user_id)
#         except CustomUser.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)

#         user.following.remove(user_to_follow)

#         user.save()

#         return Response(status=status.HTTP_200_OK)



class CommunityAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        communities = Community.objects.all()
        serializer = CommunitySerializer(communities, many=True)
        return Response({'status':1,"data":serializer.data})

    def post(self, request):
        serializer = CommunitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({'status':1,"data":serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'status':0,"data":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    

class CommunityDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, community_id):
        community = get_object_or_404(Community, pk=community_id)
        serializer = CommunitySerializer(community)
        return Response(serializer.data)

    def patch(self, request, community_id):
        community = get_object_or_404(Community, pk=community_id)
        serializer = CommunitySerializer(community, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, community_id):
        community = get_object_or_404(Community, pk=community_id)
        community.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class CommunityListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        communities = Community.objects.all()
        serializer = CommunitySerializer(communities, many=True)
        return Response({'status':1,"data":serializer.data})
    


from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

User = get_user_model()

class FollowCommunityAPIView(APIView):
    def post(self, request, community_id):
        community = get_object_or_404(Community, pk=community_id)
        
        # Add the current user to the followers of the community
        request.user.communities_following.add(community)
        
        return Response({'status':1,"data":{},"message": "You are now following the community"}, status=status.HTTP_200_OK)