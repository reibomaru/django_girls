from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # 他のモデルへのリンク
    title = models.CharField(max_length=200)
    # 文字数が制限されたテキストを定義するフィールド
    text = models.TextField()
    # 制限無しの長いテキスト用です。ブログポストのコンテンツに理想的なフィールド
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    # 日付と時間のフィールド
    # https://docs.djangoproject.com/ja/2.2/ref/models/fields/#field-types

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)
    
    def __str__(self):
        return self.title

class Comments(models.Model):
    # ポストモデルの中からコメントにアクセスできるようにします。
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text
