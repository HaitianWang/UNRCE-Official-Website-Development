// Sample add a new project button
// const addProjectButton = document.getElementById("addNewProject");
// const projectGrid = document.getElementById("projectGrid");

// // Add functionality to the button
// if (addProjectButton && projectGrid) {
//     addProjectButton.addEventListener("click", () => {
//         // Create project
//         const newProject = document.createElement("div");
//         newProject.classList.add("project");

//         // Create tag for href
//         const newProjectLink = document.createElement("a");
//         newProjectLink.href = "/";

//         // Create image
//         const newProjectImage = document.createElement("img");
//         newProjectImage.src = "https://www.wallpapertip.com/wmimgs/8-82164_soothing-background.jpg"; // Replace with the actual image path
//         newProjectImage.alt = "New Project";

//         // Create title
//         const newProjectTitle = document.createElement("h3");
//         newProjectTitle.textContent = "New Project";

//         // Link it all together
//         newProject.appendChild(newProjectLink);
//         newProject.appendChild(newProjectImage);
//         newProject.appendChild(newProjectTitle); 
        
//         projectGrid.appendChild(newProjectLink);
//         newProjectLink.appendChild(newProject);
//     });
// }

function goToDetails(event, imgSrc, titleText) {
    event.preventDefault(); 
    const baseHref = document.getElementById('projectGrid').getAttribute('data-baseurl');
    const modifiedHref = baseHref + "?img=" + encodeURIComponent(imgSrc) + "&title=" + encodeURIComponent(titleText);
    window.location.href = modifiedHref;
}

// For the details page
window.onload = function() {
    // Fetch the image source from the URL parameter
    const urlParams = new URLSearchParams(window.location.search);
    const imgSrc = urlParams.get('img');
    const titleText = urlParams.get('title');

    if (imgSrc) {
        const imageElement = document.getElementById('detailImage');
        imageElement.src = decodeURIComponent(imgSrc);
    }

    if (titleText) {
        const titleElement = document.getElementById('projectTitle');
        titleElement.textContent = decodeURIComponent(titleText);
    }
}


function toggleTableVisibility() {
    var table = document.getElementById('interestTable');
    if (table.style.display === "none") {
        table.style.display = "block";
    } else {
        table.style.display = "none";
    }
}



  