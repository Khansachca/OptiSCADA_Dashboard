//fungsi untuk menangani efek hide/show pada header saat scroll
function scrollFunction() {
  if (
    document.body.scrollTop > 50 ||
    document.documentElement.scrollTop > 100
  ) {
    navbarLogo.style.display = "none";
    navbarNav.classList.add("navbar-nav-fixed");
  } else {
    navbarLogo.style.display = "block";
    navbarNav.classList.remove("navbar-nav-fixed");
  }
}
