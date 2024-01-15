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
