// Submit post on submit
/**$('#comment-form').on('submit', function(event){
    event.preventDefault();
    console.log("form submitted!")  // sanity check
    create_comment();
});
// AJAX for posting
function create_comment() {
    console.log("create post is working!") // sanity check
    var post_id = $('.post-id').val()
    var form = $(this).closest("form");
     $.ajax({
        url : "posts/comment/", // the endpoint
        type : "POST", // http method
        data :  $("#comment-form").serialize(), // data sent with the post request
        // handle a successful response
        success : function(json) {
            $('#comment-text').val(''); // remove the value from the input
            console.log(json); // log the returned json to the console
            console.log("success"); // another sanity check
        },
        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};
/***/


  $("ul.stream").on("keydown", ".comments input[name='content']", function (evt) {
    var keyCode = evt.which?evt.which:evt.keyCode;
    if (keyCode == 13) {
      var form = $(this).closest("#comment-form");
      var container = $(this).closest(".comments");
      var input = $(this);
      console.log("form submitted!")  // sanity check
      $.ajax({
        url: '/posts/comment/',
        data: $(form).serialize(),
        type: 'post',
        cache: false,
        beforeSend: function () {
          $(input).val("");
        },

       success : function(json) {
          $("ol", container).prepend("<li><div>" + json.text + "</div>" + "<h4><a>" + json.author + "</h4></a></li>");
        }
      });
      return false;
    }
  });


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

  $("ul.stream").on("click", ".comment", function (e) {
    var post = $(this).closest(".post");
     e.preventDefault();
    if ($(".comments", post).hasClass("tracking")) {
      $(".comments", post).slideUp();
      $(".comments", post).removeClass("tracking");
    }
    else {
      $(".comments", post).show();
      $(".comments", post).addClass("tracking");
      $(".comments input[name='content']", post).focus();
      var feed = $(post).closest("li").attr("feed-id");;
    }
     return false;
  });


   function updateText(btn, newCount){
          btn.text(newCount)
          btn.attr("data-likes", newCount)
      }
      $(".like").click(function(e){
        e.preventDefault()
        var this_ = $(this)
        var likeUrl = this_.attr("data-href")
        var likeCount = parseInt(this_.attr("data-likes")) | 0
        var addLike = likeCount + 1
        var removeLike = likeCount - 1
        if (likeUrl){
           $.ajax({
            url: likeUrl,
            method: "GET",
            data: {},
            success: function(data){
              console.log(data)
              var newLikes;
              if (data.liked){
                  updateText(".like-count1", addLike)
              } else {
                  updateText(".like-count1", removeLike)
                  // remove one like
              }
            }, error: function(error){
              console.log(error)
              console.log("error")
            }
          })
        }

      })
