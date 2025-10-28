document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("filterForm");

  form.addEventListener("submit", (e) => {
    e.preventDefault();

    const params = new URLSearchParams();
    const gender = form.gender.value;
    const education = form.education.value;
    const minAge = form.min_age.value;
    const maxAge = form.max_age.value;

    if (gender) params.append("gender", gender);
    if (education) params.append("education", education);
    if (minAge) params.append("min_age", minAge);
    if (maxAge) params.append("max_age", maxAge);

    window.location.search = params.toString();
  });
});
