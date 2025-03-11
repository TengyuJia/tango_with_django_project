from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.
class Category(models.Model):
    Name_Max_Length = 128
    name = models.CharField(max_length=Name_Max_Length, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique = True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)
        
    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
class Page(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    url = models.URLField(blank=True, null=True)
    views = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    location = models.CharField(max_length=128,blank=True, null=True)
    slug = models.SlugField(unique = True, blank=True, null=True)
    image = models.ImageField(upload_to="page_images/", blank=True, null=True)
    likes = models.IntegerField(default=0)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Page, self).save(*args, **kwargs)
    def __str__(self):
        return self.title
        
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    
    def __str__(self):
        return self.user.username
        
class Comment(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='comments')  
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')  
    content = models.TextField()  
    created_at = models.DateTimeField(default=timezone.now)  

    def __str__(self):
        return f"Comment by {self.user.username} on {self.page.title}"  
        
class UserLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    category = models.ForeignKey(Category, on_delete=models.CASCADE) 
    liked_at = models.DateTimeField(auto_now_add=True)  

    class Meta:
        unique_together = ('user', 'category')  
        
class UserLikePage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    page = models.ForeignKey(Page, on_delete=models.CASCADE)  
    liked_at = models.DateTimeField(auto_now_add=True)  

    class Meta:
        unique_together = ('user', 'page')  