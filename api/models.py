from django.db import models


class Project(models.Model):
    TYPE_CHOICES = [
        ('BE', 'Back-end'),
        ('FE', 'Front-end'),
        ('IO', 'IOS'),
        ('AN', 'Android'),
    ]
    title = models.CharField(max_length=140)
    author = models.ForeignKey('authentication.User', on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    type = models.CharField(
        max_length=2,
        choices=TYPE_CHOICES,
        null=False
    )
    created_time = models.DateTimeField(auto_now_add=True)


class Contributing(models.Model):
    contributor = models.ForeignKey('authentication.User',
                                    on_delete=models.CASCADE,
                                    related_name='contributes'
                                    )
    project = models.ForeignKey('Project',
                                on_delete=models.CASCADE,
                                related_name='is_developed'
                                )

    class Meta:
        unique_together = ('contributor', 'project')