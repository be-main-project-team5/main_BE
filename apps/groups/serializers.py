from rest_framework import serializers
from .models import Group

# Group 모델의 데이터를 JSON 형태로 변환하거나, JSON 데이터를 Group 모델 인스턴스로 변환하는 역할을 합니다.
# 이 시리얼라이저는 Django REST Framework의 ModelSerializer를 상속받아, 모델 필드에 대한 자동 매핑 기능을 활용합니다.
# 'apps/groups/views.py'의 GroupViewSet에서 Group 모델의 데이터를 직렬화하고 역직렬화하는 데 사용됩니다.
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        # 이 시리얼라이저가 어떤 모델과 연결될지 지정합니다.
        # 여기서는 'apps/groups/models.py'에 정의된 Group 모델을 사용합니다.
        model = Group

        # 시리얼라이저에 포함될 모델의 필드를 지정합니다.
        # '__all__'은 Group 모델의 모든 필드를 시리얼라이저에 포함시키겠다는 의미입니다.
        # 이는 Group 모델의 모든 필드(name, debut_date, agency, logo_image_url, created_at, updated_at)가
        # API 응답에 포함되거나 API 요청을 통해 처리될 수 있음을 의미합니다.
        fields = '__all__'
