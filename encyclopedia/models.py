from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User # Django's built-in User model

# --- Your existing Category model ---
class Category(models.Model):
    """Categories for wiki entries"""
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

# --- NEW: The Missing Entry Model ---
class Entry(models.Model):
    """Represents a single wiki entry."""
    title = models.CharField(max_length=100, unique=True, db_index=True) # Ensure titles are unique and indexed for fast lookup
    content = models.TextField() # Markdown content for the entry
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL, # If a category is deleted, entries in that category remain but lose their category.
        null=True,
        blank=True,
        related_name='entries' # Allows you to get all entries for a category: category_instance.entries.all()
    )
    # Automatically sets the creation timestamp when the entry is first saved
    created_at = models.DateTimeField(auto_now_add=True)
    # Automatically updates the timestamp every time the entry is saved
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Entries' # Better plural name for the admin
        ordering = ['title'] # Order entries alphabetically by title

    def __str__(self):
        return self.title

# --- Updated EntryHistory model (now links to Entry) ---
class EntryHistory(models.Model):
    """Track the history of wiki entries"""
    # Link to the Entry model via ForeignKey
    entry = models.ForeignKey(
        Entry,
        on_delete=models.CASCADE, # If the Entry is deleted, its history should also be deleted
        related_name='history_records' # Allows entry_instance.history_records.all()
    )
    # content and category will now be fields of Entry, but stored here for historical context
    content = models.TextField()
    category_name_at_revision = models.CharField(max_length=50, blank=True, null=True) # Store category name at time of revision

    edited_at = models.DateTimeField(default=timezone.now)
    editor_ip = models.GenericIPAddressField(blank=True, null=True) # Make IP address optional for flexibility
    editor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='entry_revisions'
    )
    revision_comment = models.CharField(max_length=200, blank=True)
    
    class Meta:
        ordering = ['-edited_at']
        verbose_name_plural = 'Entry histories'
        # Add a unique constraint to ensure one history record per entry per timestamp
        # This will prevent duplicate history entries for the exact same moment
        unique_together = ('entry', 'edited_at') 
    
    def __str__(self):
        return f"Revision of '{self.entry.title}' by {self.editor.username if self.editor else 'Anonymous'} at {self.edited_at.strftime('%Y-%m-%d %H:%M')}"

# --- Updated SearchLog model ---
class SearchLog(models.Model):
    """Log search queries for analytics"""
    query = models.CharField(max_length=200)
    timestamp = models.DateTimeField(default=timezone.now)
    results_count = models.IntegerField(default=0) # Default to 0, useful if no results
    ip_address = models.GenericIPAddressField(blank=True, null=True) # Make IP optional
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='search_logs'
    )
    successful = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = 'Search logs'
    
    def __str__(self):
        return f"'{self.query}' ({self.results_count} results) by {self.user.username if self.user else 'Anonymous'} on {self.timestamp.strftime('%Y-%m-%d')}"

# --- Updated Favorite model (now links to Entry) ---
class Favorite(models.Model):
    """User's favorite entries"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    entry = models.ForeignKey( # Changed from entry_title to a ForeignKey to Entry
        Entry,
        on_delete=models.CASCADE, # If the entry is deleted, remove it from favorites
        related_name='favorited_by' # Allows entry_instance.favorited_by.all()
    )
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'entry'] # Ensure a user can only favorite an entry once
        ordering = ['-added_at']
        verbose_name_plural = 'Favorites'

    def __str__(self):
        return f"{self.user.username} favorited '{self.entry.title}'"

# --- Updated EntryComment model (now links to Entry) ---
class EntryComment(models.Model):
    """Comments on wiki entries"""
    entry = models.ForeignKey( # Changed from entry_title to a ForeignKey to Entry
        Entry,
        on_delete=models.CASCADE, # If the entry is deleted, its comments should also be deleted
        related_name='comments' # Allows entry_instance.comments.all()
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Entry comments'

    def __str__(self):
        # Access the title through the 'entry' ForeignKey
        return f"Comment on '{self.entry.title}' by {self.user.username}"