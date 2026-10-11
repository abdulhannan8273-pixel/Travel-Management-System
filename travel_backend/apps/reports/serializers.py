from rest_framework import serializers
from .models import Report


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = "__all__"
        read_only_fields = [
            "id",
            "generated_by",
            "created_at",
        ]

    def create(self, validated_data):
        validated_data["generated_by"] = self.context["request"].user
        return super().create(validated_data)