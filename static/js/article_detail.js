//点赞js
$("#div_digg .digg").click(function () {
    if ("{{ request.user.username }}") {
        var is_up = $(this).hasClass("diggit");
        var article_id = $("#info").attr("article_id");
        console.log(article_id)
        $.ajax({
            url: "/blog/poll/",
            type: "post",
            data: {
                is_up: is_up,
                article_id: article_id,
                csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val()
            },
            success: function (data) {
                //console.log(data)
                console.log(article_id)
                if (data.state) {   //state =True 传过来表明赞或踩的数据成功的存进了数据库
                    // 判断是赞还是踩
                    var up_count =$("#digg_count");
                    var down_count=$("#bury_count");
                    if (is_up) {
                        var val = parseInt(up_count.text()) + 1;
                        up_count.text(val)
                    } else {
                         val = parseInt(down_count.text()) + 1;
                         down_count.text(val)
                    }
                } else {
                    if (data.first_op) {
                        $("#digg_word").html("您已经赞过了！").css({"color": "red", "margin-right": "30px"})
                    } else {
                        $("#digg_word").html("您已经踩过了！").css({"color": "red", "margin-right": "30px"})
                    }
                }
            }
        })

    } else {
        location.href("/login/")
    }
});
//评论js
var pid = "";
var coment_area = $("#inputPassword3");
$(".comment_btn").click(function () {
    //alert(123)
    if ("{{ request.user.username }}") {
        var article_id = $("#info").attr("article_id");
        //bug 如果用户手动删除@用户名
        if (coment_area.val()[0] !== "@") {
            pid = ""
        }
        if (pid) {
            var index = coment_area.val().indexOf("\n");
            var content = coment_area.val().slice(index + 1)
        } else {
            content = coment_area.val();
        }

        $.ajax({
            url: "/blog/comment/",
            type: "post",
            data: {
                article_id: article_id,
                content: content,
                pid: pid,
                csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val()
            },
            success: function (data) {
                if (data.state) {
                    //console.log(data);
                    var user = $("#info").attr("username");
                    var floor = $(".comment_item").length + 1;
                    var ctime = data.ctime;
                    var content = data.content;
                    var s = "            <li class=\"list-group-item comment_item\">\n" +
                        "                <div>\n" +
                        "                    <span>   #" + floor + "楼 </span> &nbsp;&nbsp;\n" +
                        "                    <span>" + ctime + "</span> &nbsp; &nbsp;|\n" +
                        "                    <span><a href=\"/blog/" + user + "/\">" + user + "</a>  </span>\n" +
                        "                   <p class='well'> " + content + "</p>" +
                        "                </div>\n" +
                        "            </li>";
                    //append 是添加到选择器的子元素的后面
                    $(".comment_list ").append(s);

                    //回复后再次提交应该清空 根评论
                    coment_area.val("");
                    pid = ""

                } else {
                    coment_area.val(" 提交失败！").css({"color": "red"});
                }
            }
        })
    }

    else (
        location.href("/login/")
    )

});

//回复
$(".replay").click(function () {

    coment_area.focus();
    var val = $(this).attr("username") + "\n";
    coment_area.val("@" + val);
    pid = $(this).attr("pk")
});
