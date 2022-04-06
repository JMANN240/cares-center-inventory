//NEED TO DYNAMICALLY ADD ENTRIES TO LIST
var modal = document.getElementById("myModal");
var box = document.getElementById("box");
var addBtn = document.getElementById("add-entry");
var submitBtn = document.getElementById("submit");

// Get the <span> element that closes the modal
var close = document.getElementById("close");

// When the user clicks on the button, open the modal
addBtn.onclick = function() {
  box.style.display = "none";
  modal.style.display = "block";
  addBtn.style.opacity = 0;
  
}

//close the modal
close.onclick = function() {
  modal.style.display = "none";
  box.style.display = "flex";
  addBtn.style.opacity = 100;
}

submit.onclick = function() {
  //NEED TO COLLECT INFO FROM HERE
  modal.style.display = "none";
  box.style.display = "flex";
  addBtn.style.opacity = 100;
}

