// Show the loader
function showLoader() {
    document.getElementById("loader").style.display = "block";
}

// Hide the loader
function hideLoader() {
    document.getElementById("loader").style.display = "none";
}

// Example: Show loader during an AJAX request
function makeAjaxRequest() {
    showLoader();
    // Perform your AJAX request here
    // When the request is complete, call hideLoader()
}
// loader.js

// Wait for the page to fully load
window.addEventListener("load", function () {
    // Hide the loader
    var loader = document.getElementById("loader");
    loader.style.display = "none";
});
