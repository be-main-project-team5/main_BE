from django import forms
from django.contrib import admin
from django.db import transaction
from django.utils.html import format_html

from apps.idols.models import Idol  # Idol 모델 임포트

from .models import CustomUser, Image


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
            "password",  # For creating/changing password
            "role",
            "is_active",
            "is_staff",
            "is_superuser",
            "profile_image_upload",  # Custom field for image upload
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If an instance exists and has a profile image, we don't need to pre-populate
        # profile_image_upload as it's for new uploads. The admin will show the current
        # image via the related object's __str__ or a custom display if implemented.
        pass

    def save(self, commit=True):
        user = super().save(
            commit=False
        )  # user 인스턴스를 가져오지만 아직 저장하지 않음

        # 비밀번호가 변경되었을 경우에만 set_password를 호출
        if self.cleaned_data.get("password"):
            user.set_password(self.cleaned_data["password"])

        # Get the uploaded file from the form's cleaned_data
        profile_image_file = self.cleaned_data.get("profile_image_upload")

        with transaction.atomic():
            # Handle profile image update/creation
            if profile_image_file:
                # If a new file is uploaded, create or update the Image instance
                if user.profile_image:
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
    list_display = (
        "email",
        "nickname",
        "role",
        "get_profile_image_url",
        "created_at",
        "updated_at",
    )
    list_filter = ("role",)
    search_fields = ("email", "nickname")
    # Exclude the original profile_image ForeignKey field from the form
    # as we are handling it via profile_image_upload
    exclude = ("profile_image",)  # This will hide the ForeignKey dropdown

    # readonly_fields: 관리자 페이지에서 수정할 수 없는 필드를 지정합니다.
    readonly_fields = (
        "get_profile_image_url",
        "created_at",
        "updated_at",
        "date_joined",
        "last_login",
    )

    def get_profile_image_url(self, obj):
        if obj.profile_image and obj.profile_image.url:
            return format_html(
                '<img src="{}" width="50" height="50" />', obj.profile_image.url
            )
        return ""

    get_profile_image_url.short_description = "프로필 이미지"

    def save_model(self, request, obj, form, change):
        # form.cleaned_data에서 비밀번호를 가져옵니다.
        password = form.cleaned_data.get("password")
        # 비밀번호가 입력되었고, 이전 비밀번호와 다른 경우에만 해싱합니다.
        if password and (not change or obj.password != password):
            obj.set_password(password)
        super().save_model(request, obj, form, change)

        # If the user's role is 'IDOL' and no Idol instance exists for this user, create one
        if obj.role == "IDOL":
            if not hasattr(
                obj, "idol"
            ):  # Check if an Idol instance already exists for this user
                Idol.objects.create(user=obj, name=obj.nickname, group=None)


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("url", "file_size", "created_at")
    search_fields = ("url",)
