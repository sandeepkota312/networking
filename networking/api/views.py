from datetime import timedelta
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.authentication import SessionAuthentication


from api.models import User, FriendsNetwork, FriendRequest
from api.permission import IsOnlinePermission
from api.serializers import FriendRequestSerializer,UserSerializer


DEFAULT_AUTH_CLASSES = [SessionAuthentication]

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    authentication_classes = DEFAULT_AUTH_CLASSES
    permission_classes = [IsOnlinePermission]
    http_method_names = ["get"]

    def get_queryset(self):
        queryset = self.queryset
        data = self.request.query_params
        query = data.get('query',None)
        page_number = data.get('page', 1)
        if query:
            if '@' in query:
                queryset = queryset.filter(email__iexact=query)
            else:
                queryset = queryset.filter(username__icontains=query)
            return queryset,page_number
        else:
            return [],page_number

    def list(self, request, *args, **kwargs):
        queryset,page_number = self.filter_queryset(self.get_queryset())
        paginator = Paginator(queryset, 10)
        page_obj = paginator.get_page(page_number)

        users_list = [{"id":user.id,"email": user.email, "name": user.username} for user in page_obj]
        response = {
            "total_users": paginator.count,
            "total_pages": paginator.num_pages,
            "current_page": page_obj.number,
            "users": users_list
        }
        return Response(response,status=status.HTTP_200_OK)

class FriendRequestViewSet(ModelViewSet):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    authentication_classes = DEFAULT_AUTH_CLASSES
    permission_classes = [IsOnlinePermission]

    def get_queryset(self):
        queryset = self.queryset
        return queryset.filter(to_user=self.request.user, status='sent')
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        user_list = [{"name":query.from_user.username,"email":query.from_user.email} for query in queryset]
        response = {
            "requests":user_list,
            "instructions":{
                "accept":"To accept the friend request use 'http://127.0.0.1:7000/api/friend-requests/<username>/accept/'",
                "reject":"To Reject the friend request use 'http://127.0.0.1:7000/api/friend-requests/<username>/reject/'"
            }
            }
        return Response(response,status=status.HTTP_200_OK)


    def create(self, request, *args, **kwargs):
        # Throttle requests: limit to 3 requests per minute
        one_minute_ago = timezone.now() - timedelta(minutes=1)
        recent_requests = FriendRequest.objects.filter(from_user=request.user, datetime_created__gte=one_minute_ago).count()
        if recent_requests >= 3:
            return Response({"detail": "You can only send 3 friend requests per minute."}, status=status.HTTP_429_TOO_MANY_REQUESTS)
        data={}
        data['to_user'] = int(self.request.data['to_user'])
        data['from_user'] = self.request.user.id
        if data['to_user']!=data['from_user']:
            # checking for duplicates
            data_duplicate_check = self.queryset.filter(
                from_user__id=data['from_user'],
                to_user__id=data['to_user']
                ).filter(
                    Q(status='sent') | Q(status='accepted')
                    )
            if data_duplicate_check:
                return Response({'detail':'Request for this user is already accepted/sent'},status=status.HTTP_208_ALREADY_REPORTED)

            # adding it into database
            request_obj=FriendRequest.objects.create(from_user=User.objects.get(id=data['from_user']),to_user=User.objects.get(id=data['to_user']))
            # request_serializer = self.serializer_class(request_obj)
            return Response(
                {
                    "success":f"Friend request sent to {request_obj.to_user.username} - {request_obj.to_user.email}",
                    "details":{
                        "username":request_obj.to_user.username,
                        "email":request_obj.to_user.email,
                        }
                    },
                status=status.HTTP_201_CREATED
                )
        else:
            return Response(
                {"detail":"you can't send request to yourself"},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['post'])
    def accept(self, request,pk):
        friend_request = self.queryset.get(from_user__username=pk,to_user__id=self.request.user.id,status='sent')
        if friend_request.to_user != request.user:
            return Response({"detail": "You cannot accept this friend request."}, status=status.HTTP_403_FORBIDDEN)
        
        friend_request.status = 'accepted'
        friend_request.save()
        
        friend_request.from_user.friends_network.friends.add(friend_request.to_user)
        friend_request.to_user.friends_network.friends.add(friend_request.from_user)
        
        return Response({"status": "Friend request accepted"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        try:
            friend_request = self.queryset.get(from_user__username=pk, to_user__id=request.user.id,status='sent')
            if friend_request.to_user != request.user:
                return Response({"detail": "You cannot reject this friend request."}, status=status.HTTP_403_FORBIDDEN)
            friend_request.status = 'rejected'
            friend_request.save()
            return Response({"status": "Friend request rejected"}, status=status.HTTP_200_OK)
        except self.queryset.model.DoesNotExist:
            return Response({"detail": "Friend request not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class FriendsNetworkViewSet(ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    authentication_classes = DEFAULT_AUTH_CLASSES
    permission_classes = [IsOnlinePermission]

    def get_queryset(self):
        return self.request.user.friends_network.friends.all()

# class PendingFriendRequestsViewSet(ReadOnlyModelViewSet):
#     queryset = FriendRequest.objects.all()
#     serializer_class = FriendRequestSerializer
#     authentication_classes = DEFAULT_AUTH_CLASSES

#     def get_queryset(self):
#         return self.queryset.filter(to_user=self.request.user, status='sent')

