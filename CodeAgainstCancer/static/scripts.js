var mini = true;

function toggleSidebar() {
  if (mini) {
    console.log("opening sidebar");
    document.getElementById("mySidebar").style.width = "250px";
    mini = false;
  } else {
    console.log("closing sidebar");
    document.getElementById("mySidebar").style.width = "50px";
    mini = true;
  }
}
