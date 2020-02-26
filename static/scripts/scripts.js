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

    // Unbind keypresses temporarily so we can't double press
    $(window).unbind('keydown');

    // Parse drink settings
    let drinkId = $('.carousel-item.active').data('drink-id');
    let drinkDelayMs = $('.carousel-item.active').data('drink-delay') * 1000;
    let startTimeMs = Date.now();

    // Show the loading modal
    let modal = $('.js-loading-bar'),
    bar = modal.find('.progress-bar');
    modal.find('.progress-bar').width('0%');
    let drinkName = $('.carousel-item.active').find('.carousel-caption h1').text();
    modal.find('.modal-title').text('Making ' + drinkName + '...');
    modal.modal('show');

    // Animate the modal
    let intervalId = setInterval(function() {
      let elapsedMs = Date.now() - startTimeMs;
      if (elapsedMs > drinkDelayMs) {
        $('.progress-bar').width('100%');
      } else {
        let fractionDone = elapsedMs / drinkDelayMs;
        $('.progress-bar').width(Math.round(fractionDone * 100) + '%');
      }
    }, 150);

    // Finished making drink callback
    let doneFunction = function() {
      console.log('Drink has been made!');
      modal.modal('hide');
      clearInterval(intervalId);
      
      // Show the garnish modal
      let secondModal = $('.garnish-reminder');
      secondModal.modal('show');
      let message = $('.carousel-item.active').find('.garnish').text();
      secondModal.find('.modal-body').text(message ? message : 'Enjoy!');
      
      // Hide the garnish reminder in a few seconds
      setTimeout(function() {
        secondModal.fadeOut('slow', function() {
          secondModal.modal('hide');
        });
        // Re-enable key presses after a few seconds
        setTimeout(function() {
          $(window).keydown(keyHandlerFunction);
        }, 2000);

      }, 5000);
    };

    // Make the drink!
    $.post('/make_drink/' + drinkId, doneFunction);
    return false;
  }
};


$(window).keydown(keyHandlerFunction);
