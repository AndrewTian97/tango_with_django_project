$(document).ready(function() {

    // $("head").append('<link rel="stylesheet" href={% static "css/style.css" %} type="text/css" />');
    // alert('Hello, world!');

    $('#about-btn').click(function() {
        msgStr = $('#msg').html();
        msgStr = msgStr + ' ooo, fancy!';

        $('#msg').html(msgStr);
    });

    $('#like_btn').click(function() {
        var catecategoryIdVar;
        catecategoryIdVar = $(this).attr('data-categoryid');

        $.get('/rango/like_category/',
              {'category_id': catecategoryIdVar},
              function(data) {
                  $('#like_count').html(data);
                //   $('#like_btn').hide();
                  $('#thumb').addClass("filled");
              })
    });
});