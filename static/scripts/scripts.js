

// Add right/left keyboard support for carousel
$(document).keydown(function(e) {
    if (e.keyCode === 37) {

       // Previous
       $(".carousel-control-prev").click();
       return false;

    } else if (e.keyCode === 39) {

       // Next
       $(".carousel-control-next").click();
       return false;

    } else if (e.keyCode === 13) {

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
      setTimeout(function() {
        clearInterval(intervalId);
      }, drinkDelayMs);

      return false;
    }
});
