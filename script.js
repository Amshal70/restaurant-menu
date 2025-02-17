// Function to toggle the visibility of the feedback form
function toggleFeedbackForm() {
    const feedbackForm = document.getElementById("feedback-form");
    feedbackForm.style.display = feedbackForm.style.display === "none" ? "block" : "none";
}

// Handle feedback form submission
document.getElementById("feedbackForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent page reload

    // Get the rating and comments from the form
    let rating = document.getElementById("rating").value;
    let comments = document.getElementById("comments").value;

    // Send feedback data to Flask backend using fetch
    fetch('/submit_feedback', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ rating: rating, comments: comments })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("feedback-response").innerText = data.message;
    })
    .catch(error => console.error("Error submitting feedback:", error));
});

// Function to redirect the user to Instagram with the restaurant's tag
function addToInstagramStory() {
    const restaurantTag = "restaurantname"; // Replace with the actual restaurant's Instagram handle
    const instagramURL = `https://www.instagram.com/create/story/?text=%40${restaurantTag}`;
    
    // Open Instagram in a new tab or window
    window.open(instagramURL, "_blank");
}
