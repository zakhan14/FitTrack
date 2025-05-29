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

  const acceptCookiesBtn = document.getElementById('accept-cookies');
  if (acceptCookiesBtn) {
    acceptCookiesBtn.onclick = function() {
      document.cookie = "consent_analytics=true; path=/; max-age=" + (60*60*24*365);
      document.getElementById('cookie-banner').style.display = 'none';
      location.reload();  // Para activar el GA después del consentimiento
    };
  }
});
