# from django_elasticsearch_dsl import Document, Index
# from django_elasticsearch_dsl.registries import registry
# from elasticsearch_dsl import field

# from .models import Employee

# posts = Index('posts')

# @posts.doc_type
# @registry.register_document
# class PostDocument(Document):
#     class Django:
#         model = Employee
        
#         fields = "__all__"   