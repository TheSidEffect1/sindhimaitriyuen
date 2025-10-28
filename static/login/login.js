document.getElementById("loginForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const mob = document.getElementById("mob").value.trim();
  const password = document.getElementById("password").value.trim();

  const response = await fetch("/login_check/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify({ mob, password }),
  });

  const result = await response.json();

  if (result.success) {
    window.location.href = "/logged/"; // Redirect after login success
  } else {
    document.getElementById("error-message").textContent =
      result.error || "Invalid credentials.";
  }
});

function getCookie(name) {
  let cookieValue = null;

  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");

    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();

      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }

  return cookieValue;
}
