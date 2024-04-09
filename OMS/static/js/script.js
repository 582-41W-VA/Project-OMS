document.addEventListener("DOMContentLoaded", function () {
  window.toggleView = function () {
    var listView = document.querySelector(".users-table");
    var gridView = document.querySelector(".user-cards");
    listView.classList.toggle("hidden");
    gridView.classList.toggle("hidden");
  };
});

function toggleView() {
  var listView = document.querySelector(".users-table");
  var gridView = document.querySelector(".user-cards");
  listView.classList.toggle("hidden");
  gridView.classList.toggle("hidden");
}
