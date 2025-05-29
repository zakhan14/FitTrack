document.addEventListener("DOMContentLoaded", () => {
  const nav = document.querySelector("#nav");
  const abrir = document.querySelector("#abrir");
  const cerrar = document.querySelector("#cerrar");

  if (abrir && cerrar && nav) {
    abrir.addEventListener("click", () => {
      nav.classList.add("visible");
    });

    cerrar.addEventListener("click", () => {
      nav.classList.remove("visible");
    });
  }

  function getCookie(name) {
    let cookies = document.cookie.split(';');
    for(let cookie of cookies) {
      let [key, value] = cookie.trim().split('=');
      if (key === name) return value;
    }
    return null;
  }

  const cookieBanner = document.getElementById('cookie-banner');
  const consentCookie = getCookie('consent_analytics');

  if (!consentCookie && cookieBanner) {
    cookieBanner.style.display = 'block';
  }

  const acceptCookiesBtn = document.getElementById('btn-accept'); // o 'accept-cookies', según tu HTML
  if (acceptCookiesBtn) {
    acceptCookiesBtn.onclick = function() {
      document.cookie = "consent_analytics=true; path=/; max-age=" + (60*60*24*365);
      if(cookieBanner) cookieBanner.style.display = 'none';
      location.reload();  // Para activar GA después del consentimiento
    };
  }

  const rejectCookiesBtn = document.getElementById('btn-reject');
  if (rejectCookiesBtn) {
    rejectCookiesBtn.onclick = function() {
      document.cookie = "consent_analytics=false; path=/; max-age=" + (60*60*24*365);
      if(cookieBanner) cookieBanner.style.display = 'none';
    };
  }
});
