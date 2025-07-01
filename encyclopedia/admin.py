from django.contrib import admin
from .models import Entry, Category, EntryComment, EntryHistory, Favorite, SearchLog

# Register your models here.
# This makes your models visible and editable in the Django admin interface.

# For a simple wiki, the Entry model is the most important one to manage.
@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    # This list_display option shows selected fields in the list view of entries
    list_display = ('title', 'created_at', 'updated_at')
    # This allows searching by title
    search_fields = ('title',)

# You might want to register other models if you need to manage them directly
# For example:
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(EntryComment)
class EntryCommentAdmin(admin.ModelAdmin):
    list_display = ('entry', 'author', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('comment_text',)

@admin.register(EntryHistory)
class EntryHistoryAdmin(admin.ModelAdmin):
    list_display = ('entry', 'edited_by', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('entry__title',) # Search by related entry title

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'entry', 'added_at')
    list_filter = ('added_at',)

@admin.register(SearchLog)
class SearchLogAdmin(admin.ModelAdmin):
    list_display = ('query', 'timestamp', 'user')
    list_filter = ('timestamp',)
    search_fields = ('query',)

# If you prefer a simpler way for models without specific admin customizations:
# admin.site.register(Entry)
# admin.site.register(Category)
# admin.site.register(EntryComment)
# admin.site.register(EntryHistory)
# admin.site.register(Favorite)
# admin.site.register(SearchLog)
