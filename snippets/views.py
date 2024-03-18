"""
ViewSets define the view behavior.
"""

from django.contrib.auth.models import User,Group
# from django.http import Http404
from rest_framework.parsers import JSONParser
from rest_framework import  viewsets
from rest_framework.decorators import api_view,APIView
from rest_framework import status
from rest_framework.response import Response
# from rest_framework import mixins
from rest_framework import generics
from rest_framework import permissions
from snippets.models import Snippet
from snippets.serializers import GroupSerializer, SnippetSerializer, UserSerializer


@api_view(['GET','POST'])
def snippet_list(request,format=None):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
def snippet_detail(request, pk,format=None):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data,status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
 

class UserViewSet(viewsets.ModelViewSet):
    
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAuthenticated]
    
    
class GroupViewSet(viewsets.ModelViewSet):
    
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    # permission_classes = [permissions.IsAuthenticated]


# class based views

# class SnippetList(APIView):
    
#     def get(self,request,format=None):
#         snippets = Snippet.objects.all()
#         serializer = SnippetSerializer(snippets,many=True)
#         return Response(serializer.data,status=status.HTTP_200_OK)
    
#     def post(self,request,format=None):
#         serializer = SnippetSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_201_CREATED)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        
        
# class SnippetDetail(APIView):
    
#     def get_object(self,pk):
#         try:
#             return Snippet.objects.get(pk=pk)
#         except Snippet.DoesNotExist:
#             raise Http404
        
#     def get(self,request,pk,format=None):
#         snippet = self.get_object(pk)
#         serializer = SnippetSerializer(snippet)
#         return Response(serializer.data)
    
#     def put(self,request,pk,format=None):
#         snippet = self.get_object(pk)
#         serializer = SnippetSerializer(snippet,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_200_OK)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    
#     def delete(self,request,pk,format=None):
#         snippet = self.get_object(pk)
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    
    
#  Mixin's

# class SnippetList(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):
    
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
    
#     def get(self,request,*args,**kwargs):
#         return self.list(request,*args,**kwargs)
    
#     def post(self,request,*args,**kwargs):
#         return self.create(request,*args,**kwargs)
    
    
# class SnippetDetail(mixins.RetrieveModelMixin,
#                     mixins.UpdateModelMixin,
#                     mixins.DestroyModelMixin,
#                     generics.GenericAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
    
#     def get(self,request,*args, **kwargs):
#         return self.retrieve(request,*args, **kwargs)
    
#     def put(self,request,*args, **kwargs):
#         return self.update(request,*args, **kwargs)
    
#     def delete(self,request,*args, **kwargs):
#         return self.destroy(request,*args, **kwargs)
    
    
    
    
# Generic class-based views 


class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        
    
    
class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
