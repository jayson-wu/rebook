
$("nav [href]").each(function () {
    if (this.href.split("?")[0] == window.location.href.split("?")[0]) {
        $(this).addClass("active");
    }
});

$("#seeMore").click(function () {
    if ($(this).text() == 'See More') {
        $(this).text('See Less');
    } else {
        $(this).text('See More');
    }
});

/* newlisting form validation */
$('#newlisting').submit(function (e) {
    $('#post-listing').attr("disabled", true);
    e.preventDefault();
    var price = $('#price-input').val();
    var course = $('#course-input').val();
    var additional_info = $('#additional-input').val()
    var condition = $('input:radio[name=conditionRadios]:checked').val();


    if (price == '' || course == '' || condition == undefined) {
        alert("Please fill in the required fields.");
        $('#post-listing').attr("disabled", false);
        return false;
    }

    if (course.length >= 60) {
        alert("Your course number is too long. Please enter a valid course number.");
        $('#post-listing').attr("disabled", false);
        return false;
    }
    if (isNaN(price)) {
        alert("Please enter a numeric value for price. Make sure not to include dollar signs or other symbols.");
        $('#post-listing').attr("disabled", false);
        return false;
    }

    if (price < 0) {
        alert("Please enter a positive number for price.");
        $('#post-listing').attr("disabled", false);
        return false;
    }

    if (price >= 1000) {
        alert("We don't think anyone's going to buy a book for that price. Please enter a reasonable price (<$1000).");
        $('#post-listing').attr("disabled", false);
        return false;
    }

    var regex  = /^\d+\.\d\d$/
    if (!regex.test(price)) {
        alert("Please enter a valid price. Prices should have 2 digits after the decimal.");
        $('#post-listing').attr("disabled", false);
        return false;
    }

    if (additional_info.length >= 500) {
        alert("You have exceeded the 500 character maximum limit for the additional information box. Please shorten your description.");
        $('#post-listing').attr("disabled", false);
        return false;
    }

    else {
        $('#newlisting').unbind('submit').submit();
    }

   
});

$('#editlisting').submit(function (e) {
    $('#update-listing').attr("disabled", true);
    e.preventDefault();

    var price = $('#price-input').val();
    var course = $('#course-input').val();
    var additional_info = $('#additional-input').val()
    var condition = $('input:radio[name=conditionRadios]:checked').val();
    
    if (price == '' || course == '' || condition == undefined) {
        alert("Please fill in the required fields.");
        $('#update-listing').attr("disabled", false);
        return false;
    }

    if (course.length >= 60) {
        alert("Your course number is too long. Please enter a valid course number.");
        $('#update-listing').attr("disabled", false);
        return false;
    }
    if (isNaN(price)) {
        alert("Please enter a numeric value for price. Make sure not to include dollar signs or other symbols.");
        $('#update-listing').attr("disabled", false);
        return false;
    }

    if (price < 0) {
        alert("Please enter a positive number for price.");
        $('#update-listing').attr("disabled", false);
        return false;
    }

    if (price >= 1000) {
        alert("We don't think anyone's going to buy a book for that price. Please enter a reasonable price (<$1000).");
        $('#update-listing').attr("disabled", false);
        return false;
    }

    var regex  = /^\d+\.\d\d$/
    if (!regex.test(price)) {
        alert("Please enter a valid price. Prices should have 2 digits after the decimal.");
        $('#update-listing').attr("disabled", false);
        return false;
    }

    if (additional_info.length >= 500) {
        alert("You have exceeded the 500 character maximum limit for the additional information box. Please shorten your description.");
        $('#update-listing').attr("disabled", false);
        return false;
    }
    
    else {
        $('#editlisting').unbind('submit').submit();
    }

})


$(document).on('click', '.dropdown-menu', function (e) {
    e.stopPropagation();
});


$('#search').submit(function () {
    var upper = $('#upper-bound').val();
    var lower = $('#lower-bound').val();
    if (isNaN(lower) || isNaN(upper)) {
        alert("Please enter a numeric value for price bounds. Make sure not to include dollar signs or other symbols.")
        return false;
    }
})

/* when loading a file for postlisting2 */

var loadFile = function (event) {
    if (event.target.files.length > 5) {
        alert('You may only upload 5 images');
        $('#file').val('');
        return;
    }
    $('#clear').removeClass('hidden_text_field')
    var files = $('#file').get(0).files;
    var text = "";
    for (var i = 0; i < files.length; i++) {
        text += files[i].name;
        text += '<br>'
    }
    $('#filelist').html(text)

    var i = 0;

    $('#imagelist img').each(function () {
        if (i >= event.target.files.length) this.src = '';
        else {
            this.src = URL.createObjectURL(event.target.files[i]);
            this.onload = function () {
                URL.revokeObjectURL(this.src) // free memory
            }
            i++;
        }
    })
};

$('#clear').on('click', function () {
    $('#file').val('');
    $('#imagelist img').each(function () {
        this.src = ''
    })
    $('#filelist').html('')
    $('#clearimages').val('True')
    $('#clear').addClass('hidden_text_field')
})

