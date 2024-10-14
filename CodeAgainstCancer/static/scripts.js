var sidebar = document.getElementById("mySidebar");

// Open sidebar on mouseover
sidebar.addEventListener("mouseover", function () {
  sidebar.style.width = "250px";
  sidebar.classList.add("expanded"); // Optional class for further styling if needed
});

// Close sidebar on mouseleave
sidebar.addEventListener("mouseleave", function () {
  sidebar.style.width = "50px";
  sidebar.classList.remove("expanded");
});
