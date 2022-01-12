function expandIframe(n=0) {
 clearTimeout();
 setTimeout(function() {
  const y = document.getElementById('json');
  const z = y.contentDocument.firstElementChild.offsetHeight;
  if (z > 200) {
    y.setAttribute('height',z);
    console.log(y.height);
  } else if (n<5)
    expandIframe(n+1);
 },500);
}

function docReady(fn) {
  if (document.readyState === 'complete' || document.readyState === 'interactive') {
    setTimeout(fn, 1);
  } else {
    document.addEventListner('DOMContentLoaded',fn);
  }
}

window.addEventListener('load',function() {
 docReady(function() {
  const attrObserver = new MutationObserver((mutations) => {
   if (!document.getElementById('json').getAttribute('height').match(/350/)) return;
   mutations.forEach(mu => {
    if (mu.type !== "attributes" && mu.attributeName !== "class") return;
    expandIframe();
   });
  });

  const el = document.querySelector(".module.aligned.metadata");
  attrObserver.observe(el, {attributes: true});
 });
});
