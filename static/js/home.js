document.addEventListener("DOMContentLoaded", function () {
  const navbarNav = document.querySelector(".navbar-nav");
  const hamburgerMenu = document.querySelector("#hamburger-menu");
  const navbarLinks = document.querySelector(".navbar .links");
  const showPopupBtn = document.querySelector(".login-btn");
  const formPopup = document.querySelector(".form-popup");
  const hidePopupBtn = formPopup.querySelector(".close-btn");
  const signupLoginLink = formPopup.querySelectorAll(".bottom-link .button2");

  // Toggle class active on hamburger menu click
  hamburgerMenu.addEventListener("click", function () {
    navbarNav.classList.toggle("active");
  });

  // Click outside sidebar to hide menu
  document.addEventListener("click", function (e) {
    if (!hamburgerMenu.contains(e.target) && !navbarLinks.contains(e.target)) {
      navbarNav.classList.remove("active");
    }
  });

  // Show login popup
  showPopupBtn.addEventListener("click", () => {
    document.body.classList.toggle("show-popup");
  });

  // Hide login popup
  hidePopupBtn.addEventListener("click", () => showPopupBtn.click());

  // Show or hide signup form
  signupLoginLink.forEach((link) => {
    link.addEventListener("click", (e) => {
      e.preventDefault();
      formPopup.classList[link.id === "signup-link" ? "add" : "remove"](
        "show-signup"
      );
    });
  });
});
