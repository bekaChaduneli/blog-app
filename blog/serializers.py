from rest_framework import serializers
from .models import Blog
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

class BlogSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='blog-highlight', format='html')
    
    class Meta:
        model = Blog
        fields = ['url', 'id', 'highlight', 'author', 'title', 'content',  'linenos', 'language', 'style']


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    blog = serializers.HyperlinkedRelatedField(many=True, view_name='blog-detail', read_only=True)

    class Meta:
        model = User
        fields = ['url', 'id', 'blog', 'username',]

