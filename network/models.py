from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.content

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} likes {self.post}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} on {self.post}: {self.content}"

class SeguirPerfil(models.Model):
    seguidor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="usuarios_seguidos")
    siguiendo = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seguidores", null=True, blank=True)

    def __str__(self):
        return f"{self.seguidor} siguiendo a {self.siguiendo}"