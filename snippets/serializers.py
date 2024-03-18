from rest_framework import serializers
from snippets.models import Snippet,LANGUAGE_CHOICES,STYLE_CHOICES
from django.contrib.auth.models import User, Group



class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ['id', 'title','linenos', 'code', 'language', 'style','owner']
    
    
    def create(self, validated_data):
        owner = serializers.ReadOnlyField(source='owner.username')
        return Snippet.objects.create(**validated_data) 
    
    def update(self,instance,validated_data):
        
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance
    
    
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model =  User
        fields = ['url','username','email','groups']
        

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields =  ['url','name']
        

class UserSerializer(serializers.ModelSerializer):
    snippets = serializers.PrimaryKeyRelatedField(queryset= Snippet.objects.all(),many=True,)
    
    class Meta:
        model = User
        fields = ['id','username','snippets']