// Get the modal
var modal = document.getElementById("myModal");

// Get the button that opens the modal
// Let's assume you have a button like: <button id="myBtn">Open Modal</button>
var btn = document.getElementById("myBtn");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks the button, open the modal 
btn.onclick = function(event) {
    event.preventDefault();
    event.stopPropagation();
    modal.style.display = "block";
  }
   
// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

//Function to help with image input 
document.getElementById("organisationImage").addEventListener('change', function() {
    var fileName = this.value.split("\\").pop(); // Extract filename from full path
    var label = document.querySelector("#input-label");
    
    if(fileName) {
        label.textContent = fileName;
    } else {
        label.textContent = "Organisation Image (.png, .jpeg)"; // Reset to placeholder if no file selected
    }
});

