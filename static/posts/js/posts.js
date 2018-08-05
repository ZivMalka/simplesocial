
$(document).ready(function(){

        $(".comment-reply-btn").click(function(){
        $(".comment-reply").toggle();
    })


$("body").keydown(function (evt) {
    var keyCode = evt.which?evt.which:evt.keyCode;
    if (evt.ctrlKey && keyCode == 80) {
      $(".btn-compose").click();
      return false;
    }
  });

  $("#compose-form textarea[name='message']").keydown(function (evt) {
    var keyCode = evt.which?evt.which:evt.keyCode;
    if (evt.ctrlKey && (keyCode == 10 || keyCode == 13)) {
      $(".btn-post").click();
    }
  });

  $(".btn-compose").click(function () {
    if ($(".compose").hasClass("composing")) {
      $(".compose").removeClass("composing");
      $(".compose").slideUp();
    }
    else {
      $(".compose").addClass("composing");
      $(".compose textarea").val("");
      $(".compose").slideDown(400, function () {
        $(".compose textarea").focus();
      });
    }
  });

  $(".btn-cancel-compose").click(function () {
    $(".compose").slideUp();
  });

  $(".btn-post").click(function () {
    var last_feed = $(".stream li:first-child").attr("feed-id");
    if (last_feed == undefined) {
      last_feed = "0";
    }
    $("#compose-form input[name='last_feed']").val(last_feed);
    $.ajax({
      url: '/posts/create/',
      data: $("#compose-form").serialize(),
      type: 'post',
      cache: false,
      success: function (data) {
        $("ul.stream").prepend(data);
        $(".compose").slideUp();
        $(".compose").removeClass("composing");
        hide_stream_update();
      }
    });
  });

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
      $.ajax({
        url: '/feeds/comment/',
        data: { 'feed': feed },
        cache: false,
        beforeSend: function () {
          $("ol", post).html("<li class='loadcomment'><img src='/static/img/loading.gif'></li>");
        },
        success: function (data) {
          $("ol", post).html(data);
          $(".comment-count", post).text($("ol li", post).not(".empty").length);
        }
      });
    }
    return false;
  });

  $("ul.stream").on("keydown", ".comments input[name='post']", function (evt) {
    var keyCode = evt.which?evt.which:evt.keyCode;
    if (keyCode == 13) {
      var form = $(this).closest("form");
      var container = $(this).closest(".comments");
      var input = $(this);
      $.ajax({
        url: '/feeds/comment/',
        data: $(form).serialize(),
        type: 'post',
        cache: false,
        beforeSend: function () {
          $(input).val("");
        },
        success: function (data) {
          $("ol", container).html(data);
          var post_container = $(container).closest(".post");
          $(".comment-count", post_container).text($("ol li", container).length);
        }
      });
      return false;
    }
  });

  var modal = document.getElementById('t-wrapper');
window.onclick = function(event) {
    if (event.target == t) {
        modal.style.display = "none";
    }
}


});

