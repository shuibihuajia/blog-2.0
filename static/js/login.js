//登录验证
$(".login_btn").click(function () {

    $.ajax( {
        url:"",
        type:"post",
        data:{
            csrfmiddlewaretoken:$("[name='csrfmiddlewaretoken']").val(),
            user:$("#user").val(),
            pwd:$("#pwd").val(),
            valid_code:$("#valid_code").val()
        },
        success:function (data) {
            console.log(data)
        if (data.state){
                location.href="/index/"
        }else{
                $(".error").text(data.msg)
        }
        }

   } )
});
// 如果验证码看不清，一点图片刷新
$("#valid_img").click(function(){
     $(this)[0].src+="?"
});