window.addEventListener('load',function() {
  const x = document.location.href.split('/').reduceRight((item) => item);
  const y = document.location.pathname;
  const z = y.match('/change/');
  if (!z && x) {
   var b = '&';
   const a = x.split('&').map((s) => !s.match(/author=/g) && s.replace('?',''));
   a.forEach(function(elem) {
     if (!!elem) {
      b += elem;
     }
   });
   document.querySelectorAll('#filter_user').forEach(function(link) {
    var ref = link.getAttribute('href');
    ref += b;
    link.setAttribute('href',ref);
   })
  }
})
