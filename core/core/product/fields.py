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
            print(getattr(model_instance, self.attname))
            return 1
        return super().pre_save(model_instance, add)
