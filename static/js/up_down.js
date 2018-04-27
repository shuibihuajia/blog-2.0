$("#div_digg .diggit").click(function () {

   if("{{request.user.username }}"){
       var is_up = $(this).hasClass("diggit");
       var article_id =$("#info").attr("article_id");
        alert(is_up);
       $.ajax({
               url: "/blog/poll/",
               type: "post",
               data: {
                   is_up: is_up,
                   article_id: article_id,
                   csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val()
               },
               success: function (data) {
                   console.log(data)
                   if (data.state) {
                       if (is_up) {
                           var val = parseInt($("#digg_count").text()) + 1;
                           $("#digg_count").text(val)
                       } else {
                           var val = parseInt($("#bury_count").text()) + 1;
                           $("#bury_count").text(val)
                       }
                   }else {
                       console.log(data.first_operate);
                       if(data.first_operate){
                           $("#digg_word").html("您已经推荐过").css({"color":"red","margin-right":"30px"})
                       }else{
                           $("#digg_word").html("您已经反对过").css({"color":"red","margin-right":"30px"})
                       }
                   }
               }
           }
       )
   }
   else{
       location.href="/login/"
   }
});