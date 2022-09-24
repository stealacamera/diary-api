from datetime import date, timedelta
from django.core.management import call_command
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import mixins
from rest_framework.filters import SearchFilter

from users.models import Profile
from .models import Folder, Tag, Entry
from . import serializers
from .paginations import EntryPagination


class FolderDisplay(ModelViewSet):
    serializer_class = serializers.FolderSerializer
    
    def get_queryset(self):
        return Folder.objects.filter(user=self.request.user)

class TagDisplay(ModelViewSet):
    serializer_class = serializers.TagSerializer
    
    def get_queryset(self):
        return Tag.objects.filter(user=self.request.user)


# Entry model views

class EntryDisplay(ModelViewSet):
    serializer_class = serializers.EntrySerializer
    
    pagination_class = EntryPagination
    filter_backends = [SearchFilter]
    search_fields = ['title', 'text']
    
    def get_queryset(self):
        return Entry.objects.filter(user=self.request.user, deleted=False).order_by('-pinned')
    
    def get_serializer_context(self):
        context = super(EntryDisplay, self).get_serializer_context()
        context.update({"request": self.request})
        return context
    
    def perform_create(self, serializer):
        profile = Profile.objects.get(user=self.request.user)
        user_entries = Entry.objects.filter(user=self.request.user)
        yesterday = date.today() - timedelta(days=1)
        
        if user_entries.filter(created_on__date=date.today()).exists():
            pass
        elif user_entries.filter(created_on__date=yesterday).exists() or user_entries.count() == 0:
            profile.current_streak += 1
        else:
            profile.current_streak = 0
        
        if profile.current_streak > profile.best_streak:
            profile.best_streak = profile.current_streak
        
        profile.save()
        serializer.save()
    
class PinnedEntryDisplay(mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin,
                         GenericViewSet):
    serializer_class = serializers.EntrySerializer
    
    pagination_class = EntryPagination
    filter_backends = [SearchFilter]
    search_fields = ['title', 'text']
    
    def get_queryset(self):
        return Entry.objects.filter(user=self.request.user, pinned=True, deleted=False)
    
    def get_serializer_context(self):
        context = super(PinnedEntryDisplay, self).get_serializer_context()
        context.update({"request": self.request})
        return context

class DeletedEntryDisplay(mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.UpdateModelMixin,
                          mixins.DestroyModelMixin,
                          GenericViewSet):
    serializer_class = serializers.DeletedEntrySerializer
    
    pagination_class = EntryPagination
    filter_backends = [SearchFilter]
    search_fields = ['title', 'text']
    
    def get_queryset(self):
        return Entry.objects.filter(user=self.request.user, deleted=True)
    
    def list(self, request, *args, **kwargs):
        call_command('deleteentries')
        return super().list(request, *args, **kwargs)