$(document).ready(function() {
    // Home Page
    $('#singin_form').parsley();
    $('#registration_form').parsley();

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
            saveWidgetForUser('add', widgetId);

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

            $block = $("<div />").addClass("col-md-3").append($itemClonend);
            $block.find("a").append("<div class='ellipse-bottom'></div>");
            $(".target-droppable").append($block);
            removeElementCall();
        },
        out: function(event, ui) {
            // Remove Element
            var $item = ui.draggable;
            var widgetId = $item.attr('data-user-widget-id');
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

    $.ajax({
        url: "/users_widgets/",
        type: 'POST',
        data: {action: action, widget_id: widgetId},
        beforeSend: function (xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        success: function(result) { }
    });
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