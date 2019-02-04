$(document).ready(function() {
    $(".btn-pref .btn").click(function () {
        $(".btn-pref .btn").removeClass("btn-success").addClass("btn-default");
        // $(".tab").addClass("active"); // instead of this do the below
        $(this).removeClass("btn-default").addClass("btn-success");
    });

    $.ajax({
        url: location.href,
        context: document.body,

        success: function(){
            // comment modal
//            var star_li = $("#new-star li");
//            var star_word = $("#star-grade");
//            var new_star_word = $("#input-grade");
//	        var i=0;
//	        var len = star_li.length;
//	        var word = [' 很差',' 差',' 一般',' 推荐',' 力荐'];
//	        var new_grade = [2, 4, 6, 8, 10];
//	        for(i=0; i<len; i++)
//	        {
//		        star_li[i].index = i;
//		        alert(star_li[i].index);
//			    star_li[i].on('mouseover', function(){
//		            star_word.show();
//		            star_word.text(word[this.index]);
//		            new_star_word.value(new_grade[this.index]);
//		            for(i=0; i<=this.index; i++){
//			            star_li[i].addClass("text-danger").removeClass("text-muted");
//		            }
//				    for(i=this.index+1; i<len; i++){
//					    star_li[i].addClass("text-muted").removeClass("text-danger");
//				    }
//	            });
//	        }

            var is_in_likes = $("#likes").attr("data-l");
            if (is_in_likes === "True") {
                $("#new-likes").removeClass("text-muted").addClass("text-danger");
            } else {
                $("new-likes").removeClass("text-danger").addClass("text-muted");
            }

            var is_in_favourite = $("#add_to_favourites").attr("data-f");
            // console.log(is_in_favourite);
            if (is_in_favourite === "True") {
                // console.log("!");
                $("#new-favourites").removeClass("text-muted").addClass("text-danger");
            } else {
                $("#new-favourites").removeClass("text-danger").addClass("text-muted");
            }

            var is_in_watch_list = $("#add_to_watch_list").attr("data-w");
            // console.log(is_in_watch_list);
            if (is_in_watch_list === "True") {
                // console.log("!!");
                $("#new-watch").removeClass("text-muted").addClass("text-danger");
            } else {
                $("#new-watch").removeClass("text-danger").addClass("text-muted");
            }
        }
    });

    $('#stars').click(function() {
        $('#tab1').show();
        $('#tab2').hide();
        $('#tab3').hide();
    });

    $('#favorites').click(function() {
        $('#tab1').hide();
        $('#tab2').show();
        $('#tab3').hide();
    });

    $('#following').click(function() {
        $('#tab1').hide();
        $('#tab2').hide();
        $('#tab3').show();
    });

    $('#likes').on('click', function(event){
        event.preventDefault();
        var element = $(this);

        $.ajax({
            url : '/like_movie/',
            type : 'POST',
            data : { movie_id : $(this).attr("data-id")},

            success : function(data){
                if (data === 'add'){
                    $('#new-likes').removeClass('text-muted').addClass('text-danger');
                    $('#like-count').text(parseInt($('#like-count').text())+1);
                } else if (data === 'delete'){
                    $('#new-likes').removeClass('text-danger').addClass('text-muted');
                    if ($('#like-count').text() === '0'){
                        $('#like-count').text(0);
                    } else{
                        $('#like-count').text(parseInt($('#like-count').text())-1);
                    }
                } else{
                    alert("请登录后再使用此功能!");
                }
            }
        });
    });

    $('#add_to_favourites').on('click', function(event){
        event.preventDefault();

        $.ajax({
            url : '/add_to_favourites/',
            type : 'POST',
            data : { movie_id : $(this).attr("data-id")},

            success : function(data){
                if (data === 'add') {
                    $("#new-favourites").removeClass("text-muted").addClass("text-danger");
                    $("#favourite-count").text(parseInt($("#favourite-count").text())+1);
                } else if (data === 'delete'){
                    $("#new-favourites").removeClass("text-danger").addClass("text-muted");
                    if ($('#favourite-count').text() === '0'){
                        $('#favourite-count').text(0);
                    } else{
                        $('#favourite-count').text(parseInt($('#favourite-count').text())-1);
                    }
                } else{
                    alert("请登录后再使用此功能!");
                }
            }
        });
    });

    $('#add_to_watch_list').on('click', function(event){
        event.preventDefault();

        $.ajax({
            url : '/add_to_watch_list/',
            type : 'POST',
            data : { movie_id : $(this).attr("data-id")},

            success : function(data){
                if (data === 'add') {
                    $("#new-watch").removeClass("text-muted").addClass("text-danger");
                    $("#watch-count").text(parseInt($("#watch-count").text())+1);
                } else if (data === 'delete'){
                    $("#new-watch").removeClass("text-danger").addClass("text-muted");
                    if ($('#watch-count').text() === '0'){
                        $('#watch-count').text(0);
                    } else{
                        $("#watch-count").text(parseInt($("#watch-count").text())-1);
                    }
                } else{
                    alert("请登录后再使用此功能!");
                }
            }
        });
    });

    // You need these methods to add the CSRF token using jQuery
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
});