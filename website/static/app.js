var loading =
  '<div class="loader"><span class="dot dot_1"></span><span class="dot dot_2"></span><span class="dot dot_3"></span><span class="dot dot_4"></span></div>';

function showLoader(event) {
  // Prevent the default form submission or button behavior
  event.preventDefault();

  // Show loader and overlay
  document.querySelector(".loader").style.display = "block";
  const overlay = document.createElement("div");
  overlay.classList.add("overlay");
  document.body.appendChild(overlay);
  overlay.style.display = "block";

  setTimeout(() => {
    document.querySelector(".loader").style.display = "none";
    overlay.style.display = "none";
    document.body.removeChild(overlay);
  }, 2000);
}
