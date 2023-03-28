$(document).ready(function() {

    // $("head").append('<link rel="stylesheet" href={% static "css/style.css" %} type="text/css" />');
    // alert('Hello, world!');

    $('#about-btn').click(function() {
        msgStr = $('#msg').html();
        msgStr = msgStr + ' ooo, fancy!';

        $('#msg').html(msgStr);
    });

    $('#like_btn').click(function() {
        var categoryIdVar;
        categoryIdVar = $(this).attr('data-categoryid');

        $.get('/rango/like_category/',
              {'category_id': categoryIdVar},
              function(data) {
                  values = data.split('#');
                  $('#like_count').html(values[0]);
                //   $('#like_btn').hide();
                  if(values[1]=="True"){
                    $('#thumb').addClass("filled");
                    $('#like_btn_text').text("Liked");
                  } else {
                    $('#thumb').removeClass("filled");
                    $('#like_btn_text').text("Like it");
                  }
              })
    });
});