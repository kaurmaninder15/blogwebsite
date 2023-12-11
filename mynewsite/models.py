from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
        # return self.name + " " + str(self.id)

class Post(models.Model):

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True,null=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='post', null=True)
    active = models.BooleanField(default=False)
    user = models.CharField(max_length=100)
    # tags = models.ManyToManyField(Tag)
    status = models.CharField(max_length=1, choices=(('d','Draft'),('p','Published')),default='d')
    like_by = models.ManyToManyField(User, related_name='liked_by', blank=True)
    view_counter = models.PositiveIntegerField(default=0,blank=True)



class PostComments(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment