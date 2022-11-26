from rest_framework import serializers

from app.models import Bill


class BillViewSerializer(serializers.ModelSerializer):
    client = serializers.SlugRelatedField(read_only=True, slug_field="name")
    organisation = serializers.SlugRelatedField(read_only=True, slug_field="name")
    service = serializers.SlugRelatedField(read_only=True, slug_field="name")

    class Meta:
        model = Bill
        fields = (
            'bill_number',
            'client',
            'organisation',
            'summa',
            'date',
            'service'
        )

class BillUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
