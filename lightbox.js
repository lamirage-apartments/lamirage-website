// Click a photo in the gallery to see it large. Arrows (or the arrow keys) move between
// photos, the X, the Esc key, or a click on the dark background closes it.
// If this file fails to load, the gallery still works; the photos just don't enlarge.
(function () {
  var photos = Array.prototype.slice.call(document.querySelectorAll('.photo-grid img'));
  if (!photos.length || !window.HTMLDialogElement) return;

  var box = document.createElement('dialog');
  box.className = 'lightbox';
  box.innerHTML =
    '<figure><img alt=""><figcaption></figcaption></figure>' +
    '<button class="lb-prev" aria-label="Previous photo">&#8249;</button>' +
    '<button class="lb-next" aria-label="Next photo">&#8250;</button>' +
    '<button class="lb-close" aria-label="Close">&times;</button>';
  document.body.appendChild(box);

  var img = box.querySelector('img');
  var caption = box.querySelector('figcaption');
  var current = 0;

  function show(n) {
    current = (n + photos.length) % photos.length;
    img.src = photos[current].src;
    img.alt = photos[current].alt;
    caption.textContent = photos[current].alt;
  }

  photos.forEach(function (photo, n) {
    photo.parentNode.addEventListener('click', function () {
      show(n);
      box.showModal();
    });
  });

  box.querySelector('.lb-prev').addEventListener('click', function () { show(current - 1); });
  box.querySelector('.lb-next').addEventListener('click', function () { show(current + 1); });
  box.querySelector('.lb-close').addEventListener('click', function () { box.close(); });
  box.addEventListener('click', function (e) {
    if (e.target === box || e.target.tagName === 'FIGURE') box.close();
  });
  box.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowLeft') show(current - 1);
    if (e.key === 'ArrowRight') show(current + 1);
  });
})();
