# from django.db import models

# # Create your models here.
# from django.db import models

# class Conversation(models.Model):
#     session_id = models.CharField(max_length=100, unique=True)
#     context = models.TextField(default="")
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"Conversation {self.session_id}"




from django.db import models

class Conversation(models.Model):
    session_id = models.CharField(max_length=100, unique=True)
    context = models.TextField(default="", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['session_id']),
        ]

    def __str__(self):
        return f"Conversation {self.session_id}"

    def clean_context(self):
        """Clean up the conversation context if it gets too long"""
        if len(self.context) > 8000:  # Adjust this limit based on your needs
            exchanges = self.context.split('\n\n')
            self.context = '\n\n'.join(exchanges[-10:])  # Keep last 10 exchanges
            self.save()