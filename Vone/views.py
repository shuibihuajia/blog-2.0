from django.shortcuts import render, HttpResponse, redirect
from django.contrib import auth
# 实现生成随机验证码，是一张图片
from PIL import Image
from PIL import ImageDraw, ImageFont
import random
from io import BytesIO
from django.http import JsonResponse
# 实现注册页面
from .models import UserInfo
from .forms import RegForm
from .models import *
#poll 点赞
import json
from django.db import transaction
from django.db.models import F
from django.db.models.functions import TruncMonth
#add_article
import os
from blog_bigV import settings
import json
from bs4 import BeautifulSoup


# 登录页面逻辑
def login(request):
    if request.is_ajax():
        user = request.POST.get("user")
        pwd = request.POST.get("pwd")
        valid_code = request.POST.get("valid_code")

        res = {"state": False, "msg": None}
        valid_str = request.session.get("valid_str")

        if valid_code.upper() == valid_str.upper():
            user = auth.authenticate(username=user, password=pwd)
            print(user)
            if user:
                res["state"] = True
                auth.login(request, user)
            else:
                res["msg"] = "用户名或是密码错误！"
        else:
            res["msg"] = "验证码错误！"
        return JsonResponse(res)

    return render(request, "login.html")

def logout(request):
    auth.logout(request)
    return redirect("/login/")


# 实现随机验证码，返回图片data
def get_valid_img(request):
    # 获取一个随机的RGB颜色
    def get_random_color():
        return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

    # 生成一张图片
    image = Image.new("RGB", (250, 40), get_random_color())
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("static/font/kumo.ttf", size=32)
    # 在图片里生成五个随机字符
    temp = []
    for i in range(5):
        random_num = str(random.randint(0, 9))
        random_low_alpha = chr(random.randint(79, 122))
        random_upper_alpha = chr(random.randint(65, 90))
        random_char = random.choice([random_num, random_low_alpha, random_upper_alpha])
        # 把5个字符画到图片上
        draw.text((24 + i * 36, 0), random_char, get_random_color(), font=font)
        temp.append(random_char)

    width = 250
    height = 40
    for i in range(6):
        x1 = random.randint(0, width)
        x2 = random.randint(0, width)
        y1 = random.randint(0, height)
        y2 = random.randint(0, height)
        # 噪线
        draw.line((x1, y1, x2, y2), fill=get_random_color())
    for i in range(20):
        # 添加噪点
        draw.point([random.randint(0, width), random.randint(0, height)], fill=get_random_color())
        x = random.randint(0, width)
        y = random.randint(0, height)

        # d.arc([x1, y1, x2, y2], startAngle, endAngle,options)
        #  在左上角坐标为x1,y1，右下角坐标为x2,y2的矩形区域内满圆，
        # 以startAngle为起始角度，endAngle为终点角度，截取圆的一部分圆弧。
        # 如果x1,y1,xw,y2不是正方形，则在该区域内的最大椭圆中根据角度截取片段。
        draw.arc((x, y, x + 4, y + 4), 0, 90, fill=get_random_color())

    # 在内存中生成图片
    f = BytesIO()
    # save("test.gif","GIF")   #保存（新图片路径和名称，保存格式）
    image.save(f, "png")
    data = f.getvalue()
    f.close()

    # 把列表转换成字符串
    valid_str = ''.join(temp)
    # 把随机验证码存到session
    request.session["valid_str"] = valid_str
    return HttpResponse(data)


def reg(request):
    if request.method == "POST":
        res = {"user": None, "error_dict": None}

        form = RegForm(request.POST)
        if form.is_valid():
            # print(form.cleaned_data)
            # print(request.FILES) <MultiValueDict: {}>
            user = form.cleaned_data.get("user")
            pwd = form.cleaned_data.get("pwd")
            email = form.cleaned_data.get("email")
            # 这里取到的是上传文件的名字
            avatar = request.FILES.get("avatar")
            # print(avatar)
            # print("user", user)

            if avatar:
                user = UserInfo.objects.create(username=user,
                                               password=pwd,
                                               email=email,
                                               avatar=avatar)
            else:
                user = UserInfo.objects.create(username=user,
                                               password=pwd,
                                               email=email)
            res["user"] = user.username
        else:
            res["error_dict"] = form.errors
            # print(res)
        return JsonResponse(res)
    form = RegForm()
    return render(request, "reg.html", locals())


# 主页
def index(request):
    article = Article.objects.all()
    return render(request, "index.html", locals())


# 个人主页
def homesite(request, username, **kwargs):
    user = UserInfo.objects.filter(username=username).first()
    if not user:
        return HttpResponse(404)
    blog = user.blog
    if not kwargs:
        # 这个作者下的所有文章，主内容
        article_list = Article.objects.filter(user=user)
    else:
        condition = kwargs.get("condition")
        param = kwargs.get("param")
        if condition == "cate":
            article_list = Article.objects.filter(user=user).filter(category__title=param)
        elif condition == "tag":
            article_list = Article.objects.filter(user=user).filter(Tags__title=param)
        else:
            year, month = param.split("-")
            #print(param)
            article_list = Article.objects.filter(user=user).filter(create_time__year=year ,create_time__month=month)

    return render(request, "homesite.html", locals())


def article_detail(request,username,article_id):
    user = UserInfo.objects.filter(username=username).first()
    article = Article.objects.filter(pk=article_id).first()
    comment_list = Comment.objects.filter(article_id=article_id)
    return render(request,"article_detail.html",locals())

def poll(request):
    is_up = json.loads(request.POST.get("is_up"))
    article_id =request.POST.get("article_id")
    print('is article_id........',article_id)
    user_id = request.user.pk
    print(is_up)
    res = {"state":True}
    try:
        with transaction.atomic():
            ArticleUpDown.objects.create(is_up=is_up, article_id=article_id, user_id=user_id)
            if is_up:
                Article.objects.filter(pk=article_id).update(up_count=F("up_count")+1)
            else:
                Article.objects.filter(pk=article_id).update(down_count=F("down_count") + 1)
    except Exception as e:
        print('is ....',e)
        res["state"]=False
        res["first_op"]=ArticleUpDown.objects.filter(article_id=article_id,user_id=user_id).first().is_up
    #使用ajax传数据  需要json格式
    print(res['state'])
    return JsonResponse(res)

# def month_year(request):
#     date_list = Article.objects.values("title","create_time")
#     #print(date_list)
#     return render(request, "test_date.html",locals())


def comment(request):
    content = request.POST.get("content")
    article_id = request.POST.get("article_id")
    pid = request.POST.get("pid")
    user = request.user.pk
    print(article_id)

    res={"state": True}

    with transaction.atomic():
        if not pid:
            comment_obj=Comment.objects.create(user_id=user, article_id=article_id, content=content)
        else:
            comment_obj=Comment.objects.create(user_id=user,article_id=article_id, content=content, parent_comment_id=pid)
        #仔细阅读报错提示，debug不要盲目！！
        Article.objects.filter(nid=article_id).update(comment_count=F('comment_count')+1)

        #json 不能发送datetime类型的数据
        res['ctime']= comment_obj.comment_date.strftime("%Y-%m-%d %H:%M")
        res["content"]=comment_obj.content
        print(res)
    return JsonResponse(res)


def get_comment_tree(request,id):
    ret = list(Comment.objects.filter(article_id=id).values("pk","content","parent_comment_id","user__username"))
    #当safe这个参数被设置为：False, 那data可以填入任何能被转换为JSON格式的对象，比如list, tuple, set。 默认的safe
    #参数是True.如果你传入的data数据类型不是字典类型，那么它就会抛出TypeError的异常。
    #print(ret) ok
    return JsonResponse(ret, safe=False)


def backend(request):
    return render(request,"backend.html")


def add_article(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        #print(title,content)
        soap = BeautifulSoup(content,"html.parser")
        for tag in soap.find_all():
            if tag == "script":
                tag.decompose()
                #tag.decompose()方法将当前节点移除文档树并完全销毁

        article_obj = Article.objects.create(user=request.user ,title=title,desc=soap.text[0:150]+"...")
        ArticleDetail.objects.create(content=soap.prettify() ,article=article_obj)
        return redirect('/index/')

    return render(request,"add_article.html")

def upload_img(request):
    #print(request.FILES) <MultiValueDict: {'img': [<InMemoryUploadedFile: egon.jpg (image/jpeg)>]}>
    #print(request.POST) <QueryDict: {'csrfmiddlewaretoken': ['v5OKDQF8HEI1FmTp0vKYxIDBAuEUOc2D8kdk58YKUYKIdyvBgU0ygLUsreC0Gho0'], 'localUrl': ['C:\\fakepath\\egon.jpg']}>
    img_obj = request.FILES.get("img")
    media_path = settings.MEDIA_ROOT
    path = os.path.join(media_path,"article_imgs", img_obj.name)
    f = open(path,"wb")

    for i in img_obj:
        f.write(i)
    f.close()

    res ={
        "url": "/media/article_imgs/" + img_obj.name,
        "error":0
    }

    return JsonResponse(res)
    #HttpResponse(json.dumps(res))