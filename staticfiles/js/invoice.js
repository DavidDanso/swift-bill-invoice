$(document).ready(function () {
  /********************************************** Navigation ********************************************/

  //closes responsive menu when a scroll trigger link is clicked
  $(".nav-link").click(function () {
    $(".navbar-collapse").collapse("hide");
  });

  //
  $("body").scrollspy({
    target: "#mainNav",
    offset: 70,
  });

  //On scroll down if offset is higher than 50 pixels add navBar shrink else remove that class
  $(window).scroll(function () {
    if ($("#mainNav").offset().top > 50) {
      $("#mainNav").addClass("navbar-shrink");
    } else {
      $("#mainNav").removeClass("navbar-shrink");
    }
  });

  //
  $(window).scroll(function () {
    if ($("#mainNav").offset().top > 1000) {
      $("#mainNav").addClass("navbar-color");
    } else {
      $("#mainNav").removeClass("navbar-color");
    }
  });
});

//live-search
jQuery(document).ready(function ($) {
  $(".live-search-list #search_invoice").each(function () {
    $(this).attr("data-search-term", $(this).text().toLowerCase());
  });

  $(".live-search-box").on("keyup", function () {
    var searchTerm = $(this).val().toLowerCase();
    var noDataFound = true;

    $(".live-search-list #search_invoice").each(function () {
      if (
        $(this).filter("[data-search-term *= " + searchTerm + "]").length > 0 ||
        searchTerm.length < 1
      ) {
        $(this).show();
        noDataFound = false;
      } else {
        $(this).hide();
      }
    });

    // Toggle the visibility of the no-data-found message
    $(".no-data-found").toggle(noDataFound);
  });
});
