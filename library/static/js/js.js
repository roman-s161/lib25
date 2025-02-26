const buttons = document.querySelectorAll(".myButton");

function random(number) {
  return Math.floor(Math.random() * (number + 1));
}

for (let i = 0; i < buttons.length; i++) {
  buttons[i].addEventListener("mouseover", function () {
    const rgbCol =
      "rgb(" + random(100) + "," + random(150) + "," + random(20) + ", 0.5)";
    buttons[i].style.backgroundColor = rgbCol;
    buttons[i].style.color = "white";
    buttons[i].style.transform = "scale(1.3)";
    buttons[i].style.zIndex = 1;
  });

  buttons[i].addEventListener("mouseout", function () {
    buttons[i].style.backgroundColor = "";
    buttons[i].style.color = "";
    buttons[i].style.transform = "scale(1)";
    buttons[i].style.zIndex = 0;
  });
}
