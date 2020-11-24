load_posts()

// Load all posts on page load
function load_posts() {
    $.ajax({
        url : "api/v1/posts/", // the endpoint
        type : "GET", // http method
        // handle a successful response
        success : function(json) {
            for (var i = 0; i < json.length; i++) {
                console.log(json[i])
                $("#talk").prepend("<li id='post-"+json[i].id+"'><strong>"+json[i].text+"</strong> - <em> "+json[i].author+"</em> - <span> "+json[i].created+
                "</span> - <a id='delete-post-"+json[i].id+"'>delete me</a></li>");
            }
        },
        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};
