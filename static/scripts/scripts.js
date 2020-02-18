let keyHandlerFunction = function(e) {
  if (e.keyCode === 37) {

      // Previous
      $(".carousel-control-prev").click();
      return false;

  } else if (e.keyCode === 39) {

      // Next
      $(".carousel-control-next").click();
      return false;

  } else if (e.keyCode === 13) {

    $(window).unbind('keydown');
    console.log('disabling keypresses...')

    let drinkId = $('.carousel-item.active').data('drink-id');
    let drinkDelayMs = $('.carousel-item.active').data('drink-delay') * 1000;
    let startTimeMs = Date.now();

    let intervalId = setInterval(function() {
      let elapsedMs = Date.now() - startTimeMs;
      if (elapsedMs > drinkDelayMs) {
        // update to 100%
      } else {
        let fractionDone = elapsedMs / drinkDelayMs;
        // update progress bar
      }
    }, 50);

    let doneFunction = function() {
      console.log('Drink has been made!');
      // clear the modal
      clearInterval(intervalId);

      // Re-enable key presses after a few seconds
      setTimeout(function() {
        $(window).keydown(keyHandlerFunction);
      }, 3000);
    };

    $.post('/make_drink/' + drinkId, doneFunction);
    return false;
  }
};


$(window).keydown(keyHandlerFunction);
