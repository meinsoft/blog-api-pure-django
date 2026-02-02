from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50,unique=True,allow_unicode=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.slug
    
    def save(self,*args,**kwargs):
        self.slug=slugify(self.name,allow_unicode=True)
        super().save(*args,**kwargs)
        
    def to_dict(self):
        data = {
            'name':self.name,
            'slug':self.slug,
            'description':self.description,
            'is_active':self.is_active,
            'created_at':self.created_at.isoformat() if self.created_at else None

        }
        return data

class Post(models.Model):
    class StatusChoices(models.TextChoices):
        DRAFT = 'draft','Draft'
        PUBLISHED = 'published','Published'

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,unique=True,allow_unicode=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,related_name='posts')
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,related_name='posts')
    content = models.TextField()
    excerpt = models.CharField(max_length=300,blank=True)
    status = models.CharField(max_length=30,choices=StatusChoices.choices,default=StatusChoices.DRAFT)
    views_count = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    
    def save(self,*args,**kwargs):
        self.slug=slugify(self.title,allow_unicode=True)
        super().save(*args,**kwargs)

    def to_dict(self, include_content=False):
        data = {
            'id': self.id,
            'title': self.title,
            'slug': self.slug,
            'author': {'id': self.author.id, 'username': self.author.username},
            'category': self.category.to_dict() if self.category else None,
            'excerpt': self.excerpt,
            'status': self.status,
            'views_count': self.views_count,
            'comments_count': self.comments.count(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
        if(include_content):
            data['content']=self.content
            data['comments']=[i.to_dict() for i in self.comments.all()]
        return data


class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE,related_name='comments')
    content = models.TextField()
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.author.username} - {self.post.title[:20]}"
        
    def to_dict(self):
        return {
            'id': self.id,
            'author': {'id': self.author.id, 'username': self.author.username},
            'content': self.content,
            'is_approved': self.is_approved,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
    
    