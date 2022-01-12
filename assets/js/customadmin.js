window.addEventListener('load',function() {
 document.querySelectorAll('.module.aligned.collapse').forEach(function(elem) {
  elem.setAttribute('id','this');
  const x = document.createElement('div');
  x.setAttribute('class','container');
  const y = document.querySelectorAll('#this > div');
  y.forEach(function(elem) {
    x.appendChild(elem);
    elem.classList.remove('form-row');
  });
  document.getElementById('this').appendChild(x);
  elem.removeAttribute('id');
  elem.classList.remove('d-none');
 });
  const n = document.querySelector('img');
  if (!!n)
    n.style.display = '';
});
