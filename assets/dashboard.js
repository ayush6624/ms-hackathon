var add = document.querySelector('#add');
var subtract = document.querySelector('#subtract');
var number = document.querySelector('#number');
var number2 = document.querySelector('#number').innerText;
var number1 = parseInt(number2, 10);

add.addEventListener('click', function() {
  number1 = number1 + 1;
  number.textContent = number1;
  add.style.background = 'yellow';
  subtract.style.background = 'white';
});

subtract.addEventListener('click', function() {
  number1 = number1 - 1;
  number.textContent = number1;
  subtract.style.background = 'yellow';
  add.style.background = 'white';
});
