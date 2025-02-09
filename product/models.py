from io import BytesIO
from django.db import models
from django.core.files import File
from PIL import Image
from vendor.models import Vendor

class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    ordering = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['ordering']
    
    def __str__(self):
        return self.title

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, related_name='products', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    date_added = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date_added']
    
    def __str__(self):
        return self.title
    
    def get_thumbnail(self):
        """Returns the thumbnail of the first image."""
        first_image = self.images.first()
        if first_image and first_image.thumbnail:
            return first_image.thumbnail.url
        else:
            return 'https://via.placeholder.com/240x180.jpg'


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/products/')
    thumbnail = models.ImageField(upload_to='uploads/thumbnails/', blank=True, null=True)
    
    def save(self, *args, **kwargs):
        """Creates a thumbnail automatically when saving an image."""
        if not self.thumbnail:
            self.thumbnail = self.make_thumbnail(self.image)
        super().save(*args, **kwargs)

    def make_thumbnail(self, image, size=(300, 200)):
        """Generate a thumbnail image."""
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)
        thumbnail = File(thumb_io, name=image.name)

        return thumbnail

    def __str__(self):
        return f"Image for {self.product.title}"
