function toggleView() {
  var listView = document.querySelector(".users-table");
  var gridView = document.querySelector(".user-cards");
  var gridIcon = document.querySelector(".grid-icon");
  var listIcon = document.querySelector(".list-icon");

  // Toggle views
  listView.classList.toggle("hidden");
  gridView.classList.toggle("hidden");

  // Toggle icons
  if (gridView.classList.contains("hidden")) {
    gridIcon.style.display = "inline";
    listIcon.style.display = "none";
  } else {
    gridIcon.style.display = "none";
    listIcon.style.display = "inline";
  }
}

// For Orders

function toggleOrderView() {
  var listView = document.querySelector(".orders-table");
  var gridView = document.querySelector(".order-cards");
  var gridIcon = document.querySelector(".grid-icon");
  var listIcon = document.querySelector(".list-icon");

  // Toggle views
  listView.classList.toggle("hidden");
  gridView.classList.toggle("hidden");

  // Toggle icons
  if (gridView.classList.contains("hidden")) {
    gridIcon.style.display = "inline";
    listIcon.style.display = "none";
  } else {
    gridIcon.style.display = "none";
    listIcon.style.display = "inline";
  }
}
