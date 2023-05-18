// scripts.js

window.onload = function() {
    // Get a reference to the prediction div
    var predictionDiv = document.querySelector(".right-content");

    // Add an event listener for the wheel event
    predictionDiv.addEventListener("wheel", function(e) {
        // Determine the direction of scroll
        var delta = Math.sign(e.deltaY);

        // Scroll the div
        predictionDiv.scrollTop += delta * 30;

        // Prevent the default browser scroll
        e.preventDefault();
    }, { passive: false });
}
