from django import forms
from django.contrib import admin
from django.db import transaction
from django.utils.html import format_html

from apps.users.models import Image  # Image 모델 임포트
from .models import Group


# Custom form for GroupAdmin to handle image upload
class GroupAdminForm(forms.ModelForm):
    # Define an ImageField for logo_image to handle direct file uploads
    logo_image_upload = forms.ImageField(required=False, label="Logo Image File")

    class Meta:
        model = Group
        fields = "__all__"

    def save(self, commit=True):
        logo_image_file = self.cleaned_data.get("logo_image_upload")
        group = super().save(commit=False)

        with transaction.atomic():
            if logo_image_file:
                if group.logo_image:
                    group.logo_image.delete()

                new_image = Image(image_file=logo_image_file)
                new_image.save()
                group.logo_image = new_image
            elif "logo_image_upload" in self.changed_data and not logo_image_file:
                if group.logo_image:
                    group.logo_image.delete()
                group.logo_image = None

            if commit:
                group.save()
        return group


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    form = GroupAdminForm  # Use the custom form
    list_display = ("name", "debut_date", "agency", "get_logo_image_url", "created_at", "updated_at")
    list_filter = ("agency",)
    search_fields = ("name", "agency")
    exclude = ("logo_image",)  # Hide the ForeignKey field

    # readonly_fields: 관리자 페이지에서 수정할 수 없는 필드를 지정합니다.
    # logo_image는 ForeignKey이므로 직접 수정하기보다는 URL을 통해 확인하는 것이 좋습니다.
    readonly_fields = ("get_logo_image_url",)

    def get_logo_image_url(self, obj):
        if obj.logo_image and obj.logo_image.url:
            return format_html('<img src="{}" width="50" height="50" />', obj.logo_image.url)
        return ""
    get_logo_image_url.short_description = "로고 이미지"
