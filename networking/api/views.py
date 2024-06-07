from django.shortcuts import render
from django.core.paginator import Paginator

from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication


from api.models import User
# from api.serializers import

# Create your views here.

DEFAULT_AUTH_CLASSES = [SessionAuthentication]

class UserViewset(ModelViewSet):
    queryset = User.objects.all()
    authentication_classes = DEFAULT_AUTH_CLASSES
    http_method_names = ["get"]

    def get_queryset(self):
        queryset = self.queryset
        data = self.request.data
        query = data['query']
        page_number = data.get('page', 1)
        if '@' in query:
            queryset = queryset.filter(email__iexact=query)
        else:
            queryset = queryset.filter(name__icontains=query)
        return queryset,page_number

    def list(self, request, *args, **kwargs):
        queryset,page_number = self.filter_queryset(self.get_queryset())
        paginator = Paginator(queryset, 10)
        page_obj = paginator.get_page(page_number)

        users_list = [{"email": user.email, "name": user.name} for user in page_obj]
        response = {
            "total_users": paginator.count,
            "total_pages": paginator.num_pages,
            "current_page": page_obj.number,
            "users": users_list
        }
        return Response(response,status=status.HTTP_200_OK)

