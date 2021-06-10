const allOptions = document.querySelectorAll(".options");

allOptions.forEach((element) => {
  element.addEventListener("change", () => {
    if (element.value == "audio") {
      videoresolutions.style.display = "none";
    } else {
      videoresolutions.style.display = "flex";
    }
  });
});

setTimeout(() => {
  document.getElementById("final_donload").click();
}, 1000);
