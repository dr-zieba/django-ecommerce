from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.core import checks


class OrderField(models.PositiveIntegerField):
    def __init__(self, unique_for_field=None, *args, **kwargs):
        self.unique_for_field = unique_for_field
        super().__init__(*args, **kwargs)

    def check(self, **kwargs):
        return [*super().check(**kwargs), *self._check_for_field_attribute(**kwargs)]

    def _check_for_field_attribute(self, **kwargs):
        if self.unique_for_field is None:
            return [checks.Error("Order field must define unique_for_field attr")]
        elif self.unique_for_field not in [
            f.name for f in self.model._meta.get_fields()
        ]:
            return [checks.Error("Order field not in model attrs")]
        return []

    def pre_save(self, model_instance, add):
        if getattr(model_instance, self.attname) is None:
            queryset = self.model.objects.all()
            try:
                query = {
                    self.unique_for_field: getattr(
                        model_instance, self.unique_for_field
                    )
                }
                query_filtered = queryset.filter(**query)
                last_order = query_filtered.latest(self.attname)
                value_of_order = last_order.order + 1
            except ObjectDoesNotExist:
                value_of_order = 1
            return value_of_order
        else:
            return super().pre_save(model_instance, add)
