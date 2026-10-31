from decimal import Decimal, InvalidOperation

from rest_framework import mixins, viewsets
from rest_framework.exceptions import ValidationError

from .models import HuntLog, WantedCriminal
from .serializers import (HuntLogSerializer, WantedCriminalDetailSerializer,
                          WantedCriminalSerializer)

TRUE = {"true", "1", "yes"}
FALSE = {"false", "0", "no"}


def parse_bool(param, raw):
    value = raw.strip().lower()
    if value in TRUE:
        return True
    if value in FALSE:
        return False
    raise ValidationError({param: "Must be true or false."})


def parse_decimal(param, raw):
    try:
        value = Decimal(raw)
        if not value.is_finite():
            raise InvalidOperation
        return value
    except InvalidOperation:
        raise ValidationError({param: "Must be a valid number."})


class WantedCriminalViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = WantedCriminal.objects.all()
    SORT_FIELDS = {"reward", "-reward"}

    def get_serializer_class(self):
        if self.action == "retrieve":
            return WantedCriminalDetailSerializer
        return WantedCriminalSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        if self.action != "list":
            return qs.prefetch_related("hunts")
        params = self.request.query_params

        if "min_reward" in params:
            qs = qs.filter(reward__gte=parse_decimal("min_reward", params["min_reward"]))
        if "max_reward" in params:
            qs = qs.filter(reward__lte=parse_decimal("max_reward", params["max_reward"]))
        for flag in ("armed", "has_crew", "escape_master"):
            if flag in params:
                qs = qs.filter(**{flag: parse_bool(flag, params[flag])})

        sort = params.get("sort")
        if sort:
            if sort not in self.SORT_FIELDS:
                raise ValidationError({"sort": "Use 'reward' or '-reward'."})
            qs = qs.order_by(sort, "id")
        return qs


class HuntLogViewSet(viewsets.ModelViewSet):
    queryset = HuntLog.objects.select_related("criminal")
    serializer_class = HuntLogSerializer
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]

    def get_queryset(self):
        qs = super().get_queryset()
        if self.action == "list" and "criminal_id" in self.request.query_params:
            raw = self.request.query_params["criminal_id"]
            if not raw.isdigit():
                raise ValidationError({"criminal_id": "Must be a positive integer."})
            qs = qs.filter(criminal_id=int(raw))
        return qs
