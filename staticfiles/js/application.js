$(document).ready(function() {
    // Home Page
    $('#singin_form').parsley();

    $('#signup-button').on('click', function() {
        var first_name = $("#first_name").val();
        var last_name = $("#last_name").val();
        var email = $("#register-email").val();
        var gender = $("#gender").val();
        var zip_code = $("#zip_code").val();
        var date_of_birth = $("#date_of_birth").val();
        var password1 = $("#password1").val();
        var password2 = $("#password2").val();
        var csrftoken = getCookie('csrftoken');

        $.ajax({
            beforeSend: function(xhr) {
                // Before AJAX request send
                var validatedForm = $('#registration_form').parsley();
                validatedForm.validate();
                if (!validatedForm.isValid()) {
                    xhr.abort();
                    console.log('Request Failed, Form is not valid');
                }

                xhr.setRequestHeader("X-CSRFToken", csrftoken);
                $('#error-container').html('').addClass('hide');
            },
            type: "POST",
            url: "/register_user/",
            data: "first_name="+ first_name +"&last_name="+ last_name +"&email="+ email +"&gender="+ gender +"&zip_code="+ zip_code
            +"&date_of_birth="+ date_of_birth + "&password1=" + password1 + "&password2=" + password2,
            success: function(xhr) {
                // On Success
                window.location.href = "/personalized";
                $('#error-container').html('').addClass('hide');
            },
            error: function(xhr, textStatus, errorThrown) {
                var textResponse =  'Oops: <br/>';
                var jsonResponse = xhr.responseJSON;

                for (var property in jsonResponse) {
                    if (jsonResponse.hasOwnProperty(property)) {
                        var propertyText = '';

                        if (property == 'password1') {
                            propertyText = 'Password';
                        }
                        else if (property == 'password2') {
                            propertyText = 'Confirm Password';
                        }
                        else {
                            propertyText = property;
                        }

                        textResponse += propertyText + ': ' + jsonResponse[property].join(' ');
                    }
                    textResponse += '<br/>';
                }

                $('#error-container').html(textResponse).removeClass('hide');
            }
        });
    });

    // Drag n Drop to Add
    $(".origin-content a").draggable({
        revert: "invalid", // when not dropped, the item will revert back to its initial position
        containment: "document",
        helper: "clone",
        cursor: "move"
    });

    $(".target-droppable").droppable({
        drop: function(event, ui) {
            // Add Element
            var $item = ui.draggable;
            var widgetId = $item.attr('data-id');
            var result = saveWidgetForUser('add', widgetId);

            if (result) {
                var $itemClonend = $item.clone();
                $itemClonend.contents().filter(function(){
                    return (this.nodeType == 3);
                }).remove();

                $itemClonend.appendTo($itemClonend.parent()).draggable({
                    revert: "invalid", // when not dropped, the item will revert back to its initial position
                    containment: "document",
                    helper: "clone",
                    cursor: "move"
                });

                $block = $("<div />").addClass("col-md-2").append($itemClonend);
                $block.find("a").append("<div class='ellipse-bottom'></div>");
                $(".target-droppable").append($block);
                removeElementCall();
            }
        },
        out: function(event, ui) {
            // Remove Element
            var $item = ui.draggable;
            var widgetId = $item.attr('data-id');
            saveWidgetForUser('remove', widgetId);
            ($item).parent().remove();
        }
    });
    
    // Drag n Drop to Remove
    removeElementCall();

    // BackGround
    $('.background-list-item').on('click', function(event) {
        var imageUrl = event.target.src;
        var imageId = event.target.id;
        var csrftoken = getCookie('csrftoken');

        $.ajax({
            url: "/update_background/",
            type: 'POST',
            data: {background_id: imageId},
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            success: function(result) {
                $('#personal-background-image').css('background-image', 'url(' + imageUrl + ')');
            }
        });
    });

    // Count Clicks
    $('.count-clicks').on('click', function (event) {
        var widgetId = $(this).attr('data-id');
        var csrftoken = getCookie('csrftoken');

        $.ajax({
            url: "/update_count/",
            type: 'POST',
            data: {widget_id: widgetId},
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            success: function(result) { }
        });
    });


});

function removeElementCall() {
    // Drag n Drop to Remove
    $(".remove-icons-class a").draggable({
        revert: "invalid", // when not dropped, the item will revert back to its initial position
        containment: "document",
        helper: "clone",
        cursor: "move"
    });
}

function saveWidgetForUser(action, widgetId) {
    var csrftoken = getCookie('csrftoken');
    var response;

    $.ajax({
        url: "/users_widgets/",
        type: 'POST',
        async: false,
        data: {action: action, widget_id: widgetId},
        beforeSend: function (xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        success: function(result) {
            response = true;
        },
        error: function (result) {
            response = false;
        }
    });

    return response;
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}