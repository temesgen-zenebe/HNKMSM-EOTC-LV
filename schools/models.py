# models.py
from django.db import models
from django.conf import settings
from common.utils.text import unique_slug

class Course(models.Model):
    SCHOOL_TYPES = (
        ('sunday School Youth ', 'youthSchool'),
        ('sunday School children ', 'childrenSchool'),  
    )
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500, blank=True, null=True)
    school_type = models.CharField(max_length=100, choices=SCHOOL_TYPES)
    created_by = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to="course_image/%Y/%m/%d" ,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=200, unique=True ,null=True, blank=True)  
    
    def save(self, *args, **kwargs):
        if not self.slug:
            value = str(self.title)
            self.slug = unique_slug(value, type(self))
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title

class Chapter(models.Model):
    chapter_title = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    content = models.TextField(max_length=2000)
    audio_file = models.FileField(upload_to='audio', null=True, blank=True)
    video_url = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=200, unique=True ,null=True, blank=True)  
    
    
    def save(self, *args, **kwargs):
        if not self.slug:
            value = str(self.chapter_title)
            self.slug = unique_slug(value, type(self))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.chapter_title

class Resources(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    Resources_title = models.CharField(max_length=100)
    links = models.TextField()

    def __str__(self):
        return f"Resources for {self.chapter.chapter_title}"

class Quiz(models.Model):
    quiz_title = models.CharField(max_length=100)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=200, unique=True ,null=True, blank=True)  
    
    def save(self, *args, **kwargs):
        if not self.slug:
            value = str(self.quiz_title)
            self.slug = unique_slug(value, type(self))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.quiz_title

class Question(models.Model):
    text = models.TextField()
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            value = str(self.text)
            self.slug = unique_slug(value, type(self))[:200]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.text

class Answer(models.Model):
    text = models.CharField(max_length=255)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class Result(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.FloatField()
    is_pass = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if self.score >= 4:
            self.is_pass = True
        else:
            self.is_pass = False
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.user}'s result for {self.quiz}"

class Report(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    completion_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}'s report for {self.chapter}"

class Progress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    is_chapter_completed = models.BooleanField(default = False)
    is_quiz_completed = models.BooleanField(default = False)
    slug = models.SlugField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            value = f"{self.user.username}"
            self.slug = unique_slug(value, type(self))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} progress of {self.course}"

class QuationsAndAnswer(models.Model):
    VIEWED_TYPES =(
        ('public', 'public'),
        ('private', 'private'),  
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  # Replace 'YourCourseModel' with your actual course model
    question = models.TextField(max_length=2000)
    answer = models.TextField(blank=True, null=True)
    is_answered= models.BooleanField(default=False)
    viewed_by = models.CharField(max_length=100, default='private', choices=VIEWED_TYPES)
    slug = models.SlugField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
      
    def save(self, *args, **kwargs):    
        if self.answer:
            self.is_answered = True
        if not self.answer:
            self.is_answered = False
            
        if not self.slug:
            value = f"{self.user.username}-QA"
            self.slug = unique_slug(value, type(self))
       
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Question by {self.user.username} on {self.course.title}"