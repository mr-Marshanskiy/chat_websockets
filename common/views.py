from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet


class ListViewSet(GenericViewSet, mixins.ListModelMixin):
    pass


class RetrieveViewSet(GenericViewSet, mixins.RetrieveModelMixin):
    pass


class LCRViewSet(GenericViewSet,
                 mixins.ListModelMixin,
                 mixins.CreateModelMixin,
                 mixins.RetrieveModelMixin):
    pass
