from django.db import models
from django.contrib.auth.models import AbstractUser


class UserInfo(AbstractUser):
    """
    用户信息
    这里使用django 的用户认证系统，必须继承AbstraUser 这个类，
    继承它可以改写auth_user，这张表，添加我们需要的字段
    """
    #这里包含username，password等字段，django 认证系统帮我们创建
    nid = models.AutoField(primary_key=True)
    # 手机号存成字符串，最大11位
    telphone = models.CharField(null=True, unique=True, max_length=11)
    # 用户替身头像，上传到avatars/文件夹，默认是default.png
    avatar = models.FileField(upload_to="avatars/", default="/avatars/default.png")
    # verbose_name ???????
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    # 用户与博客的一对一关系，通过nid字段关联，可以为空
    blog = models.OneToOneField(to="Blog", to_field="nid", null=True)

    def __str__(self):
        return self.username


class Blog(models.Model):
    """
    博客信息
    个人博客主页，用到的一些字段。
    """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name="个人博客标题", max_length=64)
    # 为什么这里需要max_length
    theme = models.CharField(verbose_name="博客主题",max_length=32)
    #个人博客地址必须唯一
    site = models.CharField(verbose_name="博客地址", max_length=32, unique=True)

    def __str__(self):
        return self.title


class Category(models.Model):
    """
    博主个人文章分类
    """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32, verbose_name="分类标题")
    blog = models.ForeignKey(verbose_name="所属博客", to_field="nid", to="Blog")

    def __str__(self):
        return self.title


class Tag(models.Model):
    """
    博主给自己的博客写标签
    """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32, verbose_name="标签的名字")
    blog = models.ForeignKey(verbose_name="标签下的博客", to="Blog", to_field="nid")

    def __str__(self):
        return self.title


class Article(models.Model):
    """
    博文表
    """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, verbose_name="博客标题")
    desc = models.CharField(verbose_name="博文描述", max_length=255)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    comment_count = models.IntegerField(default=0)
    up_count = models.IntegerField(default=0)
    down_count = models.IntegerField(default=0)

    category = models.ForeignKey(verbose_name="博客所属分类", to="Category", to_field="nid", null=True)
    user = models.ForeignKey(verbose_name="文章的博主", to_field="nid", to="UserInfo")
    Tags = models.ManyToManyField(
        verbose_name="文章的标签",
        to="Tag",
        through="Article2Tag",
        through_fields=("article", "tag"),
    )
    def __str__(self):
        return self.title


class ArticleDetail(models.Model):
    """
    文章详细内容表，这张表也可以放在Article 表里，分开写更清晰
    """
    nid = models.AutoField(primary_key=True)
    content = models.TextField()
    article = models.OneToOneField(to=Article, to_field="nid")


class Article2Tag(models.Model):
    """
    文章表和标签表多对多关系的中间表
    """
    nid = models.AutoField(primary_key=True)
    article = models.ForeignKey(verbose_name="文章", to="Article", to_field="nid")
    tag = models.ForeignKey(verbose_name="标签", to="Tag", to_field="nid")

    class Meta:
        unique_together = [
            ('article', 'tag')
        ]

    def __str__(self):
        v = self.article.title+"---"+self.tag.title
        return v

class ArticleUpDown(models.Model):
    """
    点赞表，任意user对任意博客点赞与否
    """
    nid = models.AutoField(primary_key=True)
    # 用户可以不点赞，所以要由null= True
    user = models.ForeignKey(to="UserInfo",to_field="nid",null=True)
    article = models.ForeignKey(to="Article", to_field="nid", null=True)
    # 为什么要默认为True？？？
    is_up = models.BooleanField(default=True)

    class Meta:
        # 确保一个user 只能进行一次投票
        unique_together =[
            ("user", "article")
        ]


class Comment(models.Model):
    """
    评论表，支持二级评论
    """
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey( "UserInfo", verbose_name="评论的用户", to_field="nid")
    article = models.ForeignKey("Article",verbose_name="被评论的文章", to_field="nid")
    content = models.CharField(verbose_name="评论内容", max_length=255)
    comment_date =models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    parent_comment= models.ForeignKey("self", null=True)

    def __str__(self):
        return self.content

    """
    如果报下面的这些内容一定是setting里面配置出问题了
    （因为修改了django的auth_user，需要加一个变量AUTH_USER_MODEL="appname.UserInfo"）
    Vone.UserInfo.groups: (fields.E304) Reverse accessor for 'UserInfo.groups' clashes with reverse accessor for 'User.groups'.
	HINT: Add or change a related_name argument to the definition for 'UserInfo.groups' or 'User.groups'.
Vone.UserInfo.user_permissions: (fields.E304) Reverse accessor for 'UserInfo.user_permissions' clashes with reverse accessor for 'User.user_permissions'.
	HINT: Add or change a related_name argument to the definition for 'UserInfo.user_permissions' or 'User.user_permissions'.
auth.User.groups: (fields.E304) Reverse accessor for 'User.groups' clashes with reverse accessor for 'UserInfo.groups'.
	HINT: Add or change a related_name argument to the definition for 'User.groups' or 'UserInfo.groups'.
auth.User.user_permissions: (fields.E304) Reverse accessor for 'User.user_permissions' clashes with reverse accessor for 'UserInfo.user_permissions'.
	HINT: Add or change a related_name argument to the definition for 'User.user_permissions' or 'UserInfo.user_permissions'.
    """