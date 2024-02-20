from django.db import models

# This is the landing page, which is the first page that the user sees when they visit the website. Users can contact us through the contact form.

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name