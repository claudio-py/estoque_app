document.addEventListener("DOMContentLoaded", () => {
  const current = window.location.pathname;
  const links = document.querySelectorAll("ul li a");

  links.forEach((link) => {
    if (link.getAttribute("href") === current) {
      link.classList.add("active");
    }
  });
});
