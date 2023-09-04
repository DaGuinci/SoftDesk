import uuid
from django.db import models

from authentication.models import User


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
    contributors = models.ManyToManyField(
        User,
        through='Contributing',
        related_name='contributors')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['author', 'title'], name='unique project')
        ]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.contributors.add(self.author)

        return None


class Contributing(models.Model):
    contributor = models.ForeignKey('authentication.User',
                                    on_delete=models.CASCADE,
                                    related_name='contributes'
                                    )
    project = models.ForeignKey('Project',
                                on_delete=models.CASCADE,
                                related_name='is_developed'
                                )
    # TODO
    # class Meta:
        # constraints = [
        #     models.UniqueConstraint(fields=['contributor', 'project'], name='unique contributing')
        # ]


class Issue(models.Model):

    STATUS_CHOICES = [
        ('TD', 'To do'),
        ('PR', 'In progress'),
        ('FN', 'Finished'),
    ]
    PRIORITY_CHOICES = [
        ('LO', 'Low'),
        ('MD', 'Medium'),
        ('HI', 'High'),
    ]
    TAG_CHOICES = [
        ('BUG', 'Bug'),
        ('TAS', 'Task'),
        ('FEA', 'Feature'),
    ]
    title = models.CharField(max_length=140)
    author = models.ForeignKey(
        'authentication.User',
        on_delete=models.CASCADE,
        related_name="author",
        )
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        null=False
    )
    priority = models.CharField(
        max_length=2,
        choices=PRIORITY_CHOICES,
        null=False
    )
    tag = models.CharField(
        max_length=3,
        choices=TAG_CHOICES,
        null=False
    )
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(
        'authentication.User',
        on_delete=models.CASCADE,
        related_name='has_as_assigned',
        null=True,
        blank=True)
    created_time = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    author = models.ForeignKey('authentication.User', on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    issue = models.ForeignKey('Issue', on_delete=models.CASCADE)
    uuid = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)
    created_time = models.DateTimeField(auto_now_add=True)
