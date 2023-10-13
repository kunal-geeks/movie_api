// JavaScript for handling password change form submission
document
  .getElementById("passwordForm")
  .addEventListener("submit", function (event) {
    event.preventDefault();
    var newPassword = document.getElementById("newPassword").value;

    // Send a request to update password
    fetch("/edit-account", {
      method: "PUT",
      credentials: "include", // include cookies in the request
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        new_password: newPassword,
      }),
    })
      .then(function (response) {
        return response.json();
      })
      .then(function (data) {
        if (data.status === "success") {
          alert("Password updated successfully!");
        } else {
          alert("Failed to update password. Please try again.");
        }
      })
      .catch(function (error) {
        console.error(error);
      });
  });
document.getElementById("goToDashboard").addEventListener("click", function () {
  window.location.href = "/dashboard";
});
