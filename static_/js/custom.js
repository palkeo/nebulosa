var category = '';

$(function() {
    var query = $('#query').magicSuggest({
        data: '/concepts',
        valueField: 'name',
        displayField: 'name',
        allowFreeEntries: false,
        toggleOnClick: true
    });
    $(query).on('selectionchange', function(e,m) {
        var word = this.getValue()[0];
        $.getJSON(
            "/nebulosa",
            {'name': word, 'category': category},
            function(data) {
                nebu(word, data['related']);
                $('#last_articles').html(data['last_articles']);
            }
        );
    });
    $('.category-link').on('click', function() {
        category = $(this).attr('title');
         $.getJSON(
            "/nebulosa",
            {'category': category},
            function(data) {
                nebu(category, data['related']);
                $('#last_articles').html(data['last_articles']);
            }
        );
    });
});


var graph = new Springy.Graph();

if (window.addEventListener) {                    // For all major browsers, except IE 8 and earlier
        window.addEventListener("click", newgraph);
} else if (window.attachEvent) {                  // For IE 8 and earlier versions
        window.attachEvent("onclick", newgraph);
}

function newgraph()
{       
    centralword = newname();
    if(centralword === "default")
    {
        centralword = newname(); //on récupère le mot cliqué
    }

    $.getJSON(
        "/nebulosa",
        {'name': centralword, 'category': category},
        function(data) {
            nebu(centralword, data['related']);
            $('#last_articles').html(data['last_articles']);
        }
    );
}
