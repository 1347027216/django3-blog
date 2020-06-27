from collections import deque
from functools import partial

from django import VERSION as DJANGO_VERSION
from django.db import models
from django.contrib.postgres import fields as psqlfields
from django.contrib.gis.db import models as gismodels
from elasticsearch.helpers import bulk, parallel_bulk
from elasticsearch_dsl import Document as DSLDocument

from .exceptions import ModelFieldNotMappedError
from .fields import (
    ArrayField,
    BooleanField,
    DateField,
    DEDField,
    DoubleField,
    FileField,
    IntegerField,
    JSONField,
    KeywordField,
    LongField,
    ObjectField,
    ShortField,
    TextField,
    GeoPointField,
    GeoShapeField,
)
from .search import Search

model_field_class_to_field_class = {
    models.AutoField: IntegerField,
    models.BigIntegerField: LongField,
    models.BooleanField: BooleanField,
    models.CharField: TextField,
    models.DateField: DateField,
    models.DateTimeField: DateField,
    models.DecimalField: DoubleField,
    models.EmailField: TextField,
    models.FileField: FileField,
    models.FilePathField: KeywordField,
    models.FloatField: DoubleField,
    models.ImageField: FileField,
    models.IntegerField: IntegerField,
    models.NullBooleanField: BooleanField,
    models.PositiveIntegerField: IntegerField,
    models.PositiveSmallIntegerField: ShortField,
    models.SlugField: KeywordField,
    models.SmallIntegerField: ShortField,
    models.TextField: TextField,
    models.TimeField: LongField,
    models.URLField: TextField,
    models.ForeignKey: ObjectField,
    psqlfields.JSONField: JSONField,
    psqlfields.ArrayField: ArrayField,
    gismodels.PointField: GeoPointField,
    gismodels.MultiPolygonField: GeoShapeField,
}


class Document(DSLDocument):
    _prepared_fields = []

    def __init__(self, related_instance_to_ignore=None, **kwargs):
        super().__init__(**kwargs)
        self._related_instance_to_ignore = related_instance_to_ignore
        self._prepared_fields = self.init_prepare()

    def __eq__(self, other):
        return id(self) == id(other)

    def __hash__(self):
        return id(self)

    @classmethod
    def search(cls, using=None, index=None):
        return Search(
            using=cls._get_using(using),
            index=cls._default_index(index),
            doc_type=[cls],
            model=cls.django.model,
        )

    def get_queryset(self):
        """
        Return the queryset that should be indexed by this doc type.
        """
        return self.django.model._default_manager.all()

    def get_indexing_queryset(self):
        """
        Build queryset (iterator) for use by indexing.
        """
        qs = self.get_queryset()
        kwargs = {}
        if DJANGO_VERSION >= (2,) and self.django.queryset_pagination:
            kwargs = {"chunk_size": self.django.queryset_pagination}
        return qs.iterator(**kwargs)

    def init_prepare(self):
        """
        Initialise the data model preparers once here. Extracts the preparers
        from the model and generate a list of callables to avoid doing that
        work on every object instance over.
        """
        index_fields = getattr(self, "_fields", {})
        fields = []
        for name, field in index_fields.items():
            if not isinstance(field, DEDField):
                continue

            if not field._path:
                field._path = [name]

            prep_func = getattr(self, "prepare_%s_with_related" % name, None)
            if prep_func:
                fn = partial(
                    prep_func, related_to_ignore=self._related_instance_to_ignore
                )
            else:
                prep_func = getattr(self, "prepare_%s" % name, None)
                if prep_func:
                    fn = prep_func
                else:
                    fn = partial(
                        field.get_value_from_instance,
                        field_value_to_ignore=self._related_instance_to_ignore,
                    )

            fields.append((name, field, fn))

        return fields

    def prepare(self, instance):
        """
        Take a model instance, and turn it into a dict that can be serialized
        based on the fields defined on this Document subclass
        """
        data = {}
        for name, field, prep_func in self._prepared_fields:
            value = prep_func(instance)
            data[name] = value

            choices = field._value_choices
            if value and choices:
                # TODO: see if internal type is int or str and cast or dont cast accordingly
                if isinstance(value, list):
                    value_display = [str(x[1]) for x in choices if x[0] in value]
                else:
                    value_display = [str(x[1]) for x in choices if x[0] == value][0]
                data[f"{name}_display"] = value_display
        return data

    @classmethod
    def to_field(cls, field_name, model_field):
        """
        Returns the elasticsearch field instance appropriate for the model
        field class. This is a good place to hook into if you have more complex
        model field to ES field logic
        """
        try:
            is_array_field = isinstance(model_field, psqlfields.ArrayField)

            if is_array_field:
                choices = model_field.base_field.choices
            else:
                choices = model_field.choices

            field_class = model_field_class_to_field_class[model_field.__class__](
                attr=field_name, _value_choices=choices
            )

            if is_array_field:
                _internal_class = model_field_class_to_field_class[
                    model_field.base_field.__class__
                ]
                field_class.set_type(_internal_class.name)

            return field_class
        except KeyError:
            raise ModelFieldNotMappedError(
                "Cannot convert model field {} "
                "to an Elasticsearch field!".format(field_name)
            )

    def bulk(self, actions, **kwargs):
        return bulk(client=self._get_connection(), actions=actions, **kwargs)

    def parallel_bulk(self, actions, **kwargs):
        if self.django.queryset_pagination and "chunk_size" not in kwargs:
            kwargs["chunk_size"] = self.django.queryset_pagination
        bulk_actions = parallel_bulk(
            client=self._get_connection(), actions=actions, **kwargs
        )
        # As the `parallel_bulk` is lazy, we need to get it into `deque` to run it instantly
        # See https://discuss.elastic.co/t/helpers-parallel-bulk-in-python-not-working/39498/2
        deque(bulk_actions, maxlen=0)
        # Fake return value to emulate bulk() since we don't have a result yet,
        # the result is currently not used upstream anyway.
        return (1, [])

    def _prepare_action(self, object_instance, action):
        return {
            "_op_type": action,
            "_index": self._index._name,
            "_id": object_instance.pk,
            "_source": (self.prepare(object_instance) if action != "delete" else None),
        }

    def _get_actions(self, object_list, action):
        for object_instance in object_list:
            yield self._prepare_action(object_instance, action)

    def _bulk(self, *args, **kwargs):
        """Helper for switching between normal and parallel bulk operation"""
        parallel = kwargs.pop("parallel", False)
        if parallel:
            return self.parallel_bulk(*args, **kwargs)
        else:
            return self.bulk(*args, **kwargs)

    def update(self, thing, refresh=None, action="index", parallel=False, **kwargs):
        """
        Update each document in ES for a model, iterable of models or queryset
        """
        if refresh is True or (refresh is None and self.django.auto_refresh):
            kwargs["refresh"] = True

        if isinstance(thing, models.Model):
            object_list = [thing]
        else:
            object_list = thing

        return self._bulk(
            self._get_actions(object_list, action), parallel=parallel, **kwargs
        )
