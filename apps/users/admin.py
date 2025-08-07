from django import forms
from django.contrib import admin
from django.db import transaction
from django.utils.html import format_html

from .models import CustomUser, GroupBookmark, IdolBookmark, Image


# Custom form for CustomUserAdmin to handle image upload
class CustomUserAdminForm(forms.ModelForm):
    # Define an ImageField for profile_image to handle direct file uploads
    # This field will override the default ForeignKey widget in the admin form
    profile_image_upload = forms.ImageField(required=False, label="Profile Image File")

    class Meta:
        model = CustomUser
        fields = (
            "email",
            "nickname",
            "password", # For creating/changing password
            "role",
            "is_active",
            "is_staff",
            "is_superuser",
            "profile_image_upload", # Custom field for image upload
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If an instance exists and has a profile image, we don't need to pre-populate
        # profile_image_upload as it's for new uploads. The admin will show the current
        # image via the related object's __str__ or a custom display if implemented.
        pass

    def save(self, commit=True):
        # Get the uploaded file from the form's cleaned_data
        profile_image_file = self.cleaned_data.get("profile_image_upload")
        user = super().save(
            commit=False
        )  # Save the user instance without committing yet


        with transaction.atomic():
            # Handle profile image update/creation
            if profile_image_file:
                # If a new file is uploaded, create or update the Image instance
                if user.profile_image:
                    # If user already has a profile image, delete the old one
                    user.profile_image.delete()  # This will also delete the file from storage

                # Create a new Image instance for the uploaded file
                new_image = Image(image_file=profile_image_file)
                new_image.save()  # This will save the file and populate url/file_size
                user.profile_image = new_image
            elif "profile_image_upload" in self.changed_data and not profile_image_file:
                # If the user explicitly cleared the image upload field in the form
                if user.profile_image:
                    user.profile_image.delete()  # Delete the old image
                user.profile_image = None

            if commit:
                user.save()
        return user


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    form = CustomUserAdminForm  # Use the custom form
    list_display = ("email", "nickname", "role", "get_profile_image_url", "created_at", "updated_at")
    list_filter = ("role",)
    search_fields = ("email", "nickname")
    # Exclude the original profile_image ForeignKey field from the form
    # as we are handling it via profile_image_upload
    exclude = ("profile_image",)  # This will hide the ForeignKey dropdown

    # readonly_fields: 관리자 페이지에서 수정할 수 없는 필드를 지정합니다.
    readonly_fields = ("get_profile_image_url", "created_at", "updated_at", "date_joined", "last_login")

    def get_profile_image_url(self, obj):
        if obj.profile_image and obj.profile_image.url:
            return format_html('<img src="{}" width="50" height="50" />', obj.profile_image.url)
        return ""
    get_profile_image_url.short_description = "프로필 이미지"


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("url", "file_size", "created_at")
    search_fields = ("url",)


@admin.register(IdolBookmark)
class IdolBookmarkAdmin(admin.ModelAdmin):
    list_display = ("user", "idol_id", "created_at")
    search_fields = ("user__email",)


@admin.register(GroupBookmark)
class GroupBookmarkAdmin(admin.ModelAdmin):
    list_display = ("user", "group_id", "created_at")
    search_fields = ("user__email",)
