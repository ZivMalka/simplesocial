

$(document).ready(function(){

  $("ul.stream").on("click", ".comment", function () {
    var post = $(this).closest(".post");
    if ($(".comments", post).hasClass("tracking")) {
      $(".comments", post).slideUp();
      $(".comments", post).removeClass("tracking");
    }
    else {
      $(".comments", post).show();
      $(".comments", post).addClass("tracking");
      $(".comments input[name='post']", post).focus();
      var feed = $(post).closest("li").attr("feed-id");


      });
    }
}