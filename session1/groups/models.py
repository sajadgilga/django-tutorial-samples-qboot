from django.db import models
from django.dispatch import Signal

open_signal = Signal()


class Book(models.Model):
    name = models.CharField(max_length=128)
    content = models.TextField()
    author = models.CharField(max_length=128)
    is_open = models.BooleanField()
    owner = models.ForeignKey(to="auth.User", on_delete=models.CASCADE, null=True)

    def change_author(self, new_author, user):
        if user.user_permissions.filter(codename='can_change_metadata').exists():
            self.author = new_author
            self.save()

    def open(self, user):
        if user.groups.filter(name='opener').exists():
            self.is_open = True
            self.save()
            open_signal.send('Sample ...', object_id=self.id, username=user.username)
            # open_signal.send(Book, object_id=self.id, username=user.username)

    def close(self, user):
        if user.groups.filter(name='opener').exists():
            self.is_open = False
            self.save()

    def add_summary(self, summary, user):
        if user.groups.filter(permissions__codename='can_write_summary').exists():
            self.content += f'\nSummary: {summary}'
            self.save()

    class Meta:
        permissions = [
            ('can_open', 'Can open & close book'),
            ('can_write_summary', 'Can add summary to book'),
            ('can_change_metadata', 'Can change books metadata'),
        ]
