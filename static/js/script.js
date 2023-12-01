// ambil elemen header
var navbarLogo = document.getElementById("navbar-logo");
var navbar = document.getElementsByClassName;
("navbar-nav");
//saat pengguna menggulir, panggil fungsi scrollFunction
window.onscroll = function () {
  scrollFunction();
  navbarLogoScrollFunction();
};
//fungsi untuk menangani efek hide/show pada header saat scroll
function scrollFunction() {
  if (
    document.body.scrollTop > 50 ||
    document.documentElement.scrollTop > 100
  ) {
    navbarNav.classList.add("navbar-nav-fixed");
  } else {
    navbarNav.classList.remove("navbar-nav-fixed");
  }
}

function navbarLogoScrollFunction() {
  if (
    document.body.scrollTop > 50 ||
    document.documentElement.scrollTop > 100
  ) {
    navbarLogo.style.display = "none";
  } else {
    navbarLogo.style.display = "block";
  }
}

//Toggle class active
const navbarNav = document.querySelector(".navbar-nav");
//Ketika Hamburger menu di klik
document.querySelector("#hamburger-menu").onclick = () => {
  navbarNav.classList.toggle("active");
};

//Klik di luar sidebar untuk menghilangkan nav
const hamburger = document.querySelector("#hamburger-menu");

document.addEventListener("click", function (e) {
  if (!hamburger.contains(e.target) && !navbarNav.contains(e.target)) {
    navbarNav.classList.remove("active");
  }
});
