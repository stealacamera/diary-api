from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Folder, Tag, Entry


class FolderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    folder_entries = serializers.HyperlinkedRelatedField(many=True, read_only=True,
                                                         view_name='entry-detail')
    
    class Meta:
        model = Folder
        fields = ['id', 'user', 'name', 'folder_entries']
        validators = [
            UniqueTogetherValidator(queryset=Folder.objects.all(),
                                    fields=['user', 'name'],
                                    message='No duplicate folders allowed.')
        ]

class TagSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    tag_entries = serializers.HyperlinkedRelatedField(many=True, read_only=True,
                                                      view_name='entry-detail')
    
    class Meta:
        model = Tag
        fields = ['id', 'user', 'name', 'tag_entries']
        validators = [
            UniqueTogetherValidator(queryset=Tag.objects.all(),
                                    fields=['user', 'name'],
                                    message='No duplicate tags allowed.')
        ]

class TagRelatedField(serializers.SlugRelatedField):
    def get_queryset(self):
        queryset = self.queryset
        return queryset.filter(user=self.context['request'].user)

class FolderRelatedField(serializers.SlugRelatedField):    
    def get_queryset(self):
        queryset = self.queryset
        return queryset.filter(user=self.context['request'].user)

class EntrySerializer(serializers.ModelSerializer):        
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    folder = FolderRelatedField(queryset=Folder.objects.all(), allow_null=True, slug_field='name')
    tags = TagRelatedField(queryset=Tag.objects.all(), many=True, allow_null=True, slug_field='name')
    
    class Meta:
        model = Entry
        exclude = ['created_on', 'edited_on']
        extra_kwargs = {'deleted': {'write_only': True},
                        'pinned': {'write_only': True}}

class DeletedEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = ['id', 'title', 'created_on', 'deleted', 'text']
        read_only_fields = ['title', 'created_on', 'text']