from django.conf import settings
from django.core.files.storage import default_storage

from apps.users.models import Image


class ImageUpdateSerializerMixin:
    """
    Serializer mixin for handling image updates in a standardized way.

    This mixin provides a method to update an image field, handling deletion
    of the old image and creation of the new one. It is designed to work with
    both multipart/form-data and JSON requests where an image might be
    explicitly set to null.
    """

    def _update_image(self, instance, validated_data, image_field_name):
        """
        Updates an image field for a given model instance.

        Args:
            instance: The model instance to update.
            validated_data: The serializer's validated data.
            image_field_name (str): The name of the image ForeignKey field on the instance.
        """
        image_file = validated_data.pop(image_field_name, None)
        request = self.context.get("request")

        image_was_provided = (
            image_file is not None
            or (
                request
                and image_field_name in request.data
                and (
                    request.data[image_field_name] is None
                    or request.data[image_field_name] == "null"
                )
            )
        )

        if not image_was_provided:
            return

        # Delete the old Image model instance if it exists.
        # django-cleanup will automatically delete the associated file from storage.
        old_image = getattr(instance, image_field_name, None)
        if old_image:
            old_image.delete()
            setattr(instance, image_field_name, None)

        # If a new image file is provided, create a new Image instance.
        if image_file:
            new_image = Image.objects.create(image_file=image_file)
            setattr(instance, image_field_name, new_image)
