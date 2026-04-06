from django.db import models
from django.conf import settings
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Product(models.Model):
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products/')
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            import uuid
            base_slug = slugify(self.name)
            # Initial slug: name-sellerid
            generated_slug = f"{base_slug}-{self.seller.id}"
            
            # Check for collisions and append unique suffix if necessary
            if Product.objects.filter(slug=generated_slug).exists():
                generated_slug = f"{generated_slug}-{uuid.uuid4().hex[:6]}"
                
            self.slug = generated_slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def average_rating(self):
        from django.db.models import Avg
        avg = self.reviews.aggregate(Avg('rating'))['rating__avg']
        return round(avg, 1) if avg else 0

    @property
    def review_count(self):
        return self.reviews.count()
