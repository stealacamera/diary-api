from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register('folders', views.FolderDisplay, basename='folder')
router.register('tags', views.TagDisplay, basename='tag')

router.register('pinned', views.PinnedEntryDisplay, basename='fav-entry')
router.register('trash', views.DeletedEntryDisplay, basename='del-entry')
router.register('', views.EntryDisplay, basename='entry')

urlpatterns = [
    path('', include(router.urls)),
]