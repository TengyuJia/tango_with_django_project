from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.utils import timezone

# Define the Category model
class Category(models.Model):
    Name_Max_Length = 128
    name = models.CharField(max_length=Name_Max_Length, unique=True)  
    views = models.IntegerField(default=0) 
    likes = models.IntegerField(default=0) 
    slug = models.SlugField(unique=True) 

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)  # Generate slug from name
        super(Category, self).save(*args, **kwargs)
        
    class Meta:
        verbose_name_plural = 'Categories'  

    def __str__(self):
        return self.name  

# Define the Page model
class Page(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # Associated category
    title = models.CharField(max_length=128)  
    url = models.URLField(blank=True, null=True)  
    views = models.IntegerField(default=0) 
    price = models.FloatField(default=0)  
    rating = models.FloatField(default=0)  
    location = models.CharField(max_length=128, blank=True, null=True)  
    slug = models.SlugField(unique=True, blank=True, null=True)  
    image = models.ImageField(upload_to="page_images/", blank=True, null=True)  
    likes = models.IntegerField(default=0)  
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)  # Generate slug from title 
        super(Page, self).save(*args, **kwargs)
        
    def update_average_price(self):
        # Calculate the average price from related Price objects
        prices = self.prices.all()
        if prices.exists():
            self.price = sum(price.price for price in prices) / prices.count()
            self.save()

    def update_average_rating(self):
        # Calculate the average rating from related Rating objects
        ratings = self.ratings.all()
        if ratings.exists():
            self.rating = sum(rating.stars for rating in ratings) / ratings.count()
            self.save()

    def __str__(self):
        return self.title 
        
# Define the UserProfile model
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Associated user
    website = models.URLField(blank=True)  
    picture = models.ImageField(upload_to='profile_images', blank=True)  
    
    def __str__(self):
        return self.user.username  
        
# Define the Comment model
class Comment(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='comments')  
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')  
    content = models.TextField()  
    created_at = models.DateTimeField(default=timezone.now)  # Timestamp of the comment

    def __str__(self):
        return f"Comment by {self.user.username} on {self.page.title}"  
        
# Define the UserLike model
class UserLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Associated user
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # Associated category
    liked_at = models.DateTimeField(auto_now_add=True)  # Timestamp of the like

    class Meta:
        unique_together = ('user', 'category')  # Ensure unique like per user and category
        
# Define the UserLikePage model
class UserLikePage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Associated user
    page = models.ForeignKey(Page, on_delete=models.CASCADE)  # Associated page
    liked_at = models.DateTimeField(auto_now_add=True)  # Timestamp of the like

    class Meta:
        unique_together = ('user', 'page')  # Ensure unique like per user and page
        
# Define the RecommendedDish model
class RecommendedDish(models.Model):
    page = models.ForeignKey('Page', on_delete=models.CASCADE, related_name='recommended_dishes')  # Associated page
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Associated user
    dish_name = models.CharField(max_length=255)  # Name of the recommended dish
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of the recommendation

    def __str__(self):
        return self.dish_name  
        
# Define the Price model
class Price(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='prices')  # Associated page
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Associated user
    price = models.FloatField()  
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of the price submission

    def __str__(self):
        return f"{self.user.username} - {self.price}" 

# Define the Rating model
class Rating(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='ratings')  # Associated page
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Associated user
    stars = models.FloatField(default=0)  # Rating from 0 to 5
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"{self.user.username} - {self.stars} stars"  

# Define the ContactUs model
class ContactUs(models.Model):
    full_name = models.CharField(max_length=255)  
    email = models.EmailField() 
    subject = models.CharField(max_length=255, choices=[
        ('inquiry', 'General Inquiry'),
        ('feedback', 'Feedback'),
        ('complaint', 'Complaint'),
        ('other', 'Other'),
    ])  # Subject of the contact
    message = models.TextField()  
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"{self.full_name} - {self.subject}"  