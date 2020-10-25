# coding=utf-8
import graphene

from apps.posts.schema import PostQuery, CreatePost, UpdatePost, CreateComment, DeleteComment


class Query(PostQuery, graphene.ObjectType):
    pass


class Mutation(graphene.ObjectType):
    create_post = CreatePost.Field()
    update_post = UpdatePost.Field()

    create_comment = CreateComment.Field()
    delete_comment = DeleteComment.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)


