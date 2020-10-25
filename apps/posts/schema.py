# coding=utf-8
import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphql import GraphQLError

from apps.posts.models import Post, Comment


class PostType(DjangoObjectType):
    class Meta:
        model = Post


class CommentType(DjangoObjectType):
    class Meta:
        model = Comment


class PostQuery(graphene.ObjectType):
    posts = graphene.List(PostType)
    post = graphene.Field(PostType, id=graphene.Int())

    comments = graphene.List(CommentType)

    def resolve_posts(self, info, **kwargs):
        return Post.objects.all()

    def resolve_comments(self, info, **kwargs):
        return Comment.objects.all()

    def resolve_post(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return Post.objects.get(pk=id)
        return None


class PostCreateInput(graphene.InputObjectType):
    """
    Class defined to accept input data
    from the interactive graphql console.
    """
    title = graphene.String(required=True)
    description = graphene.String(required=True)
    publish_date = graphene.DateTime(required=True)
    author = graphene.String(required=True)


class CreatePost(relay.ClientIDMutation):
    class Input:
        # PostCreateInput class used as argument here.
        new_post = graphene.Argument(PostCreateInput)

    new_post = graphene.Field(PostType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        post = Post(**input.get('new_post'))  # get an instance of the post model here
        post.save()
        return cls(new_post=post)  # newly created post instance returned.


class UpdatePost(relay.ClientIDMutation):
    class Input:
        post = graphene.Argument(PostCreateInput)  # get the post input from the args
        id = graphene.String(required=True)  # get the post id

    updated_post = graphene.Field(PostType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        post_instance = Post.objects.filter(id=input['id'])  # get post by id
        if post_instance.exists():
            post = post_instance.first()
            post.title = input['post']['title']
            post.description = input['post']['description']
            post.publish_date = input['post']['publish_date']
            post.author = input['post']['author']
            post.save()
            return cls(updated_post=post)
        else:
            raise GraphQLError('Invalid Id')


class CommentCreateInput(graphene.InputObjectType):
    """
    Class defined to accept input data
    from the interactive graphql console.
    """
    comment = graphene.String(required=True)
    author = graphene.String(required=True)
    post = graphene.Int(required=True)


class CreateComment(relay.ClientIDMutation):
    class Input:
        # CommentCreateInput class used as argument here.
        new_comment = graphene.Argument(CommentCreateInput)

    new_comment = graphene.Field(CommentType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        post_instance = Post.objects.filter(id=input['new_comment']['post'])  # get post by id
        if post_instance.exists():
            comment = Comment()
            comment.post_id = input['new_comment']['post']
            comment.author = input['new_comment']['author']
            comment.comment = input['new_comment']['comment']
            comment.save()
        else:
            raise GraphQLError('Invalid Post Id')
        return cls(new_comment=comment)  # newly created comment instance returned.


class DeleteComment(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.ID()

    comment = graphene.Field(CommentType)

    @classmethod
    def mutate(cls, root, info, **input):
        comment_instance = Comment.objects.filter(id=input['id'])  # get comment by id
        if comment_instance.exists():
            comment_instance.delete()
        else:
            raise GraphQLError('Invalid Id')
        return cls(ok=True)
