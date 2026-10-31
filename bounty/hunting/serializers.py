from rest_framework import serializers

from .models import HuntLog, WantedCriminal


class HuntLogSerializer(serializers.ModelSerializer):
    criminal_id = serializers.PrimaryKeyRelatedField(
        source="criminal", queryset=WantedCriminal.objects.all())

    class Meta:
        model = HuntLog
        fields = ["id", "criminal_id", "success", "notes", "created_at"]
        read_only_fields = ["id", "created_at"]

    def validate(self, attrs):
        if self.instance is not None and "criminal" in attrs:
            raise serializers.ValidationError(
                {"criminal_id": "Cannot be changed after creation."})
        return attrs


class WantedCriminalSerializer(serializers.ModelSerializer):
    class Meta:
        model = WantedCriminal
        fields = ["id", "name", "nickname", "reward", "latitude", "longitude",
                  "last_known_note", "difficulty", "armed", "has_crew", "escape_master"]


class WantedCriminalDetailSerializer(WantedCriminalSerializer):
    hunts = HuntLogSerializer(many=True, read_only=True)

    class Meta(WantedCriminalSerializer.Meta):
        fields = WantedCriminalSerializer.Meta.fields + ["hunts"]
