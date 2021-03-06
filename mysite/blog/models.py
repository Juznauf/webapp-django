from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
class PublishedManager(models.Manager):
    """
    add the custom manager to the Post class 
    """
    def get_queryset(self):
        """
        override superclass method
        """
        return models.Manager.get_queryset(self)\
                            .filter(status='published') # extend method instead of using super)
        # return super(PublishedManager, 
        #              self).get_queryset()\
        #                 .filter(status='published') 

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published')
    ) # for status field
    title = models.CharField(max_length=250) # translates into a VARCHAR column in the SQL database
    slug = models.SlugField(max_length=250, unique_for_date='publish') # this is intended to build beautiful, SEO-friendly URLs for your blog posts. Add the unique for date params so that you can build URLs for posts using their publish date and slug. Django will prevent multiple post from having the same slug for a given date, this will be unique entries, indexable
    author = models.ForeignKey(User, 
                            on_delete=models.CASCADE,
                            related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10,
                            choices=STATUS_CHOICES,
                            default='draft')
    objects = models.Manager() # the default manager
    published = PublishedManager() # our custom manager
    tags = TaggableManager() # to set tags in post. allows us to add, retrieve and remove tags from Post object


    class Meta:
        ordering = ('-publish',)
        # can customize table name with db_table attribute
    
    def __str__(self): # for str overloading will not interfere with object repr, only str() and print() functionalities
        return self.title

    def get_absolute_url(self):
        """
        this method will be used in templates to link to specific posts
        """
        return reverse('blog:post_detail',
                        args=[self.publish.year,
                        self.publish.month,
                        self.publish.day,
                        self.slug])
 
 
class Comment(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments') # related name allows for back ref
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True) # manually deactivate inappropriate comments

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'