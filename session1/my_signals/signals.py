# Create your models here.
from django.contrib.auth.models import Permission
from django.db.models.signals import post_save
from django.dispatch import receiver

from groups.models import Book, open_signal


@receiver([post_save, open_signal], sender=Book)
def log_create_new_books(sender, instance: Book, created, *args, **kwargs):
    if created:
        print(f'new book with name {instance.name}:{instance.id} has been created')
    else:
        print(f'book with id {instance.id} has been updated')


@receiver(open_signal, sender='PROCESS_AND_API')
def log_open_action_for_books(sender, *args, **kwargs):
    print(f'item {kwargs["object_id"]} from sender {sender} has been opened')


@receiver(open_signal, sender='PROCESS_AND_API')
def log_open_action_for_books(sender, *args, **kwargs):
    print(f'item {kwargs["object_id"]} from sender {sender} has been opened')


@receiver(post_save, sender=Permission)
def log_created_permission(sender, instance, created, *args, **kwargs):
    if created:
        print(f'New permission with name {instance.codename} was created')
