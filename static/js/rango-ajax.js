$(document).ready(function() {
    $('#like_btn').click(function() {
        var categoryIdVar = $(this).attr('data-categoryid');
        $.get('/rango/like_category/', {
            'category_id': categoryIdVar
        }, function(data) {
            if (data == -1) {
                alert('Invalid category ID.');  
            } else if (data == -2) {
                alert('You have already liked this category.');  
            } else {
                $('#like_count').html(data);  
                $('#like_btn').hide();  
            }
        });
    });
	$('#like_page_btn').click(function() {
        var pageIdVar = $(this).attr('data-pageid');
        $.get('/rango/like_page/', {
            'page_id': pageIdVar
        }, function(data) {
            if (data == -1) {
                alert('Invalid restaurant ID.');  
            } else if (data == -2) {
                alert('You have already liked this restaurant.');  
            } else {
                $('#like_count').html(data);  
                $('#like_page_btn').hide();  
            }
        });
    });
});