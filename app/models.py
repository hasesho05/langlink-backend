import os
import uuid
from django.db import models
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from django.db.models.signals import post_save, pre_save
from django.db.models import Count, OuterRef, Subquery


class Account(models.Model):
    def __str__(self):
        return f"{self.id} | {self.account_id} | {self.username} | {self.email}"

    def user_directory_path(instance, filename):
        return "user_icon/user_{0}/{1}".format(instance.id, filename)

    username = models.CharField(verbose_name="ユーザー名", max_length=128)
    email = models.CharField(verbose_name="メールアドレス", max_length=128, unique=True)
    user_icon = models.ImageField(verbose_name="アイコン", upload_to=user_directory_path, null=True, blank=True)
    profile = models.TextField(verbose_name="プロフィール", null=True, blank=True)
    twitter_link = models.CharField(verbose_name="Twitter", max_length=128, null=True, blank=True)
    created_at = models.DateTimeField(verbose_name="作成日時", default=timezone.now)
    updated_at = models.DateTimeField(verbose_name="更新日時", default=timezone.now)


class Post(models.Model):
    class Meta:
        ordering = ["-created_at"]

    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="posts", null=True, blank=True)
    content = models.TextField(verbose_name="投稿内容", null=True, blank=True)
    image = models.ImageField(verbose_name="画像", upload_to="post_images", null=True, blank=True)
    like = models.ManyToManyField(Account, through="LikePost", related_name="post_liked_by", blank=True, null=True)
    created_at = models.DateTimeField(verbose_name="作成日時", default=timezone.now)
    updated_at = models.DateTimeField(verbose_name="更新日時", default=timezone.now)

    def __str__(self):
        return f"{self.id} | {self.content} | {self.account.account_id}"


class LikePost(models.Model):
    post = models.ForeignKey(Post, related_name="post", on_delete=models.CASCADE, blank=True, null=True)
    account = models.ForeignKey(Account, related_name="account", on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(verbose_name="作成日時", default=timezone.now)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["account", "post"], name="likepost_unique"),
        ]

    def __str__(self):
        return str(self.account.account_id) + "=>" + str(self.post.id)


class History(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="histories", null=True, blank=True)
    word = models.CharField(verbose_name="検索ワード", max_length=50)
    created_at = models.DateTimeField(verbose_name="作成日時", default=timezone.now)

    def __str__(self):
        return f"{self.id} | {self.account.username} | {self.word}"

    class Meta:
        ordering = ["-created_at"]