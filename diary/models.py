from django.db import models
from django.contrib.auth.models import User


class Folder(models.Model):
    name = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='folders', null=True)
    
    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'name'], 
                                               name='unique_folder_per_user')]
    
    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tags', null=True)
    
    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'name'], 
                                               name='unique_tag_per_user')]
    
    def __str__(self):
        return self.name

class Entry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_entries', null=True)
    title = models.CharField(max_length=40, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    edited_on = models.DateField(auto_now=True)
    
    deleted = models.BooleanField(default=False)
    pinned = models.BooleanField(default=False)
    
    tags = models.ManyToManyField(Tag, related_name='tag_entries', blank=True)
    folder = models.ForeignKey(Folder, on_delete=models.SET_NULL, related_name='folder_entries', null=True, blank=True)
    
    text = models.TextField()
    
    class Meta:
        verbose_name_plural = 'Entries'
    
    def __str__(self):
        return self.user.username + ': ' + self.title