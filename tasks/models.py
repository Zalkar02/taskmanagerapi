from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    status = models.BooleanField()
    creation_date = models.DateTimeField(auto_now_add=True)
    finish_date = models.DateTimeField()
    owner = models.ForeignKey('auth.User', related_name='tasks', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    tasks = models.ManyToManyField(Task, related_name='tags')
    owner = models.ForeignKey('auth.User', related_name='tags', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title