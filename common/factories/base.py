class BaseFactory:
    model = None

    def __init__(self, *args, **kwargs):
        assert self.model is not None, "Model must be specified"
        super().__init__(*args, **kwargs)

    def list(self, filters):
        filters = filters or {}
        return self.model.objects.filter(**filters)

    def get_object(self, value, lookup_field='pk'):
        return self.model.objects.filter(**{lookup_field: value}).first()
