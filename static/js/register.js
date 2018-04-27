//解决上传的图像没有显示问题-- 图像预览
$("#avatar").change(function () {
    //一个dom对象 .file[0] 是什么
    var choose_file = $(this)[0].files[0];
    console.log(choose_file);
    var reader = new FileReader();
    reader.readAsDataURL(choose_file);

    reader.onload = function () {
        $(".avatar").attr("src", reader.result)
    }
});

// 注册事件
$(".reg_btn").click(function () {
    var formdata = new FormData();
    //使用form 表单发过来的字段 名字前面加 id_
    formdata.append("user", $("#id_user").val());
    formdata.append("pwd", $("#id_pwd").val());
    formdata.append("email", $("#id_email").val());
    formdata.append("repeat_pwd", $("#id_repeat_pwd").val());
    //取到文件
    formdata.append("avatar", $("#avatar")[0].files[0]);
    formdata.append("csrfmiddlewaretoken", $('[name="csrfmiddlewaretoken"]').val());

    $.ajax({
        url: "",
        type: "post",
        processData: false,
        contentType: false,
        data: formdata,
        success: function (data) {
            if (data.user) {
                // 注册成功
                location.href = "/login/"
            }
            else
            //注册失败
                console.log(data.error_dict);
            //清空注册信息
            $("form span").html("");
            // has-error 是后面代码动态添加的类,让输错的input框变红。
            $("form .form-group").removeClass("has-error");
            //加载错误信息
            $.each(data.error_dict, function (field, error_list) {
                if (field == "__all__") {
                    $("#id_repeat_pwd").next().html(error_list[0]).css("color", "red");
                    $("#id_repeat_pwd").parent().addClass("has-error")
                }
                $("#id_" + field).next().html(error_list[0]).css("color", "red")
                $("#id_" + field).parent().addClass("has-error")
            })
        }
    })
});