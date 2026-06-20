from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Quote(models.Model):
    text = models.TextField()
    author = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='quotes')
    is_famous = models.BooleanField(default=False)
    source = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['author']

    def __str__(self):
        return f'"{self.text[:50]}..." — {self.author}'
