# 分页
import json

from django.db.models import Q
from django.http import HttpResponse
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger  # 分页
from django.shortcuts import render
from django.views.generic import View

# 查询
from elasticsearch import Elasticsearch, connection

client = Elasticsearch()


class BlogSearchView(View):
    def get(self, request):
        return render(request, "blog-search-index.html")

    def post(self, request):
        '''
        根据关键字搜索
        :param request:
        :return:
        '''
        key_words = request.POST.get("search", "")

        response = client.search(
            index="blog_content",
            body={
                "query": {
                    "bool": {
                        "should": [
                            {"match":
                                {"content": {
                                    'query': key_words,
                                    # 权重
                                    "boost": 5
                                }

                                }
                            },
                            {"match":
                                {"title": {
                                    'query': key_words,
                                    # 权重
                                    "boost": 8
                                }

                                }
                            },
                        ]
                    }
                },
            })

        id = []
        title = []
        author = []
        describe = []
        create_time = []
        read_count = []

        search_count = response['hits']['total']['value']
        search_time = response["hits"]["max_score"]
        for hit in response['hits']['hits']:
            id.append(hit["_id"])
            title.append(hit['_source']['title'])
            author.append(hit['_source']['username'])
            describe.append(hit['_source']['describe'])
            create_time.append(hit['_source']['create_time'][0:10])
            read_count.append(hit['_source']['read_count'])

        blog = zip(id, title, author, describe, create_time, read_count)
        return render(request, "blog-search.html", {
            "blog": blog,
            "search_count": search_count,
            "search_time": search_time,
            "key_words": key_words,
        })


class SearchSuggestView(View):
    '''
    # 搜索建议
    '''

    def get(self, request):
        key_words = request.GET.get("search", "")
        response = client.search(
            index="blog_content",
            body={
                "query": {
                    "fuzzy": {
                        "content": {
                            "value": key_words,
                            "fuzziness": 2
                        }
                    }
                },
            })
        title = []
        for hit in response['hits']['hits']:
            title.append(hit['_source']['title'] + ",")
        return HttpResponse(title)
