// main.js - lightweight interactions for templates/main.html
(function(){
  // open hero image in a simple lightbox when clicked
  const heroImage = document.querySelector('.hero-image');
  const lightbox = document.getElementById('lightbox');
  const lightboxImg = document.getElementById('lightbox-img');

  if(heroImage && lightbox && lightboxImg){
    heroImage.style.cursor = 'zoom-in';
    heroImage.addEventListener('click', function(){
      lightboxImg.src = heroImage.src;
      lightboxImg.alt = heroImage.alt || 'hero image';
      lightbox.classList.add('show');
      lightbox.setAttribute('aria-hidden','false');
      // lock scroll
      document.documentElement.style.overflow = 'hidden';
      document.body.style.overflow = 'hidden';
    });

    // clicking outside the image or pressing ESC closes the lightbox
    lightbox.addEventListener('click', function(e){
      if(e.target === lightbox || e.target === lightboxImg){
        closeLightbox();
      }
    });

    document.addEventListener('keydown', function(e){
      if(e.key === 'Escape') closeLightbox();
    });

    function closeLightbox(){
      lightbox.classList.remove('show');
      lightbox.setAttribute('aria-hidden','true');
      lightboxImg.src = '';
      document.documentElement.style.overflow = '';
      document.body.style.overflow = '';
    }
  }

  // small effect: header becomes compact on scroll
  const header = document.querySelector('.hero-header');
  if(header){
    const compactClass = 'compact';
    window.addEventListener('scroll', function(){
      const scrolled = window.scrollY || window.pageYOffset;
      if(scrolled > 30) header.classList.add(compactClass); else header.classList.remove(compactClass);
    }, {passive:true});
  }
})();