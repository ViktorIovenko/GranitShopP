import uuid
from datetime import date
from django.db import models
from django.utils.text import slugify
import os


class Product(models.Model):
    FLOOR_MOUNT = 'floor'
    WALL_MOUNT = 'wall'
    CEILING_MOUNT = 'ceiling'

    MOUNT_CHOICES = [
        (FLOOR_MOUNT, 'Напольная'),
        (WALL_MOUNT, 'Крепление на стену'),
        (CEILING_MOUNT, 'Крепление на потолок'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    discount_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    width = models.DecimalField(max_digits=5, decimal_places=2)
    height = models.DecimalField(max_digits=5, decimal_places=2)
    length = models.DecimalField(max_digits=5, decimal_places=2)
    weight = models.DecimalField(max_digits=6, decimal_places=2)
    production_time = models.IntegerField()
    model = models.CharField(max_length=50)
    mount_type = models.CharField(max_length=20, choices=MOUNT_CHOICES)
    slug = models.SlugField(unique=True, default='default-slug')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


def generate_product_image_filename(instance, filename):
    extension = filename.split('.')[-1]
    new_filename = f'{uuid.uuid4()}.{extension}'
    path = os.path.join('product_images', instance.product.slug)
    return os.path.join(path, new_filename)


def upload_product_image_to(instance, filename):
    if not instance.pk:
        today = date.today()
        filename = f'{uuid.uuid4()}.{filename.split(".")[-1]}'
        path = os.path.join('product_images', str(today.year), str(today.month), str(today.day))
        return os.path.join(path, filename)
    else:
        return instance.image.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_product_image_to)

    def __str__(self):
        return self.product.name

    def save(self, *args, **kwargs):
        if self.image:
            super().save(*args, **kwargs)
        elif self.pk:
            self.delete()
        else:
            return

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)
