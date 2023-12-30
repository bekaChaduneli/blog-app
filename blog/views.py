from .models import Blog
from .serializers import BlogSerializer, AuthorSerializer, UserSerializer
from .permissions import IsAuthorOrReadOnly
from rest_framework import permissions
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import renderers
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

class UserRegistrationView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        user = User.objects.get(username=serializer.data['username'])
        token, created = Token.objects.get_or_create(user=user)
        headers = self.get_success_headers(serializer.data)
        return Response({'token': token.key}, status=status.HTTP_201_CREATED, headers=headers)

class BlogList(generics.ListCreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class BlogHighlight(generics.GenericAPIView):
    queryset = Blog.objects.all()
    renderer_classes = [renderers.StaticHTMLRenderer]

    def get(self, request, *args, **kwargs):
        blog = self.get_object()
        return Response(blog.highlighted)
    
class BlogDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

class AuthorList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = AuthorSerializer

class AuthorDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = AuthorSerializer

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'authors': reverse('user-list', request=request, format=format),
        'blogs': reverse('blog-list', request=request, format=format)
    })