$(function() {
  $('.nav-tabs .nav-link').on("focus", function() {
    $($(this).attr("href").toUpperCase())[0].style.display = '';
    $('.nav-tabs .nav-link').not($(this)).each(function() {
      $($(this).attr("href").toUpperCase())[0].style.display = "none";
    });
  });
})

function hideLinks() {
    $('.mr-auto ~ div .nav-link:not(.active)').each(function() {
        this.style.display = '';
    });
    var x = $('div.navbar-nav.ml-auto')[0].offsetWidth;
    var y = -10;
    var z = $('.ml-auto .nav-link:not(.active)');
    for (i=0;i<z.length;i++) {
        w = z[i].offsetWidth;
        y = y + w;
        if (y > x) {
            for (j=0;j<i;j++) {
                $('#moremenu .nav-link:not(.active)')[j].style.display = 'none';
            };
            break;
        };
    };
}
