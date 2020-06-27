from django_elasticsearch_dsl import Document, TextField,Completion
from elasticsearch_dsl import Index, analyzer
from django_elasticsearch_dsl.registries import registry
from apps.blog.models import BlogModel


@registry.register_document
class BlogDocument(Document):
    content = TextField(analyzer='ik_max_word')
    suggestion = Completion(analyzer='ik_max_word')
    title = TextField(analyzer='ik_max_word')
    describe = TextField(analyzer='ik_max_word')

    class Index:
        # Name of the Elasticsearch index
        # 索引名称
        name = 'blog_content'
        # 创建索引
        # See Elasticsearch Indices API reference for available settings
        settings = {'number_of_shards': 2,
                    'number_of_replicas': 0}

    class Django:
        # 默认表
        model = BlogModel

        # 默认字段
        fields = [
            'username',
            "cover",
            "create_time",
            'read_count',
            'favorite',
        ]

        # 自定义字段
        def prepare_words(self, instance):
            return " ".join(instance.fields)

