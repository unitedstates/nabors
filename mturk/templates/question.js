$(function() {
  $('#mturk_form').submit(function() {
    $('#error-incomplete').hide();
    // num_lines is passed in from the template.
    for (var i=0; i < num_lines; i++) {
      if ($('input[name=accuracy_' + i + ']:checked').length < 1 && $('input[name=unclear_' + i + ']:checked').length < 1) {
        $('#error-incomplete').show();
        return false;
      } else {
        window.console.log($('input[name=accuracy_' + i + ']:checked').length < 1, $('input[name=unclear_' + i + ']:checked').length < 1)
      }
    }
  });
});
