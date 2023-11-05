import os
from io import BytesIO

from celery import shared_task
from django.core.files.base import ContentFile

from users.models import ImageUpload


@shared_task(bind=True)
def custom_formula(self, inp):
    try:
        result = inp * 7 - 4 + inp % 6
        # raise Exception('custom exception')
        print('result is', result)
        return result
    except Exception as e:
        self.retry(exc=e, max_retries=3, countdown=5)


@shared_task
def addition(first, second):
    return first + second


def create_thumbnail_from_image(image):
    from PIL import Image
    original = Image.open(image)
    original.thumbnail((200, 200))
    print(image.name)
    thumb_name, thumb_extension = os.path.splitext(image.name.split('/')[1])
    thumb_extension = thumb_extension.lower()
    print(thumb_name)
    thumb_filename = thumb_name + '_thumb' + thumb_extension

    temp_thumb = BytesIO()
    original.save(temp_thumb, format='JPEG')
    temp_thumb.seek(0)

    temp_file = ContentFile(temp_thumb.read())
    temp_thumb.close()
    return thumb_filename, temp_file


@shared_task
def generate_thumbnail(image_id):
    image_obj = ImageUpload.objects.get(id=image_id)
    thumbnail_name, thumbnail_file = create_thumbnail_from_image(image_obj.original_image)
    image_obj.thumbnail.save(thumbnail_name, thumbnail_file, save=False)
    image_obj.save()
