(function () {
  var favicon = document.querySelector('link[rel~="icon"]');
  if (!favicon) {
    favicon = document.createElement("link");
    favicon.rel = "icon";
    document.head.appendChild(favicon);
  }
  favicon.href = "/favicon.ico";
  favicon.type = "image/x-icon";
  favicon.setAttribute("sizes", "any");
})();

(function () {
  var sidebar = document.querySelector(".sidebar");
  if (!sidebar || sidebar.querySelector('a[href$="legal-stay-in-spain.html"]')) {
    return;
  }

  var sections = sidebar.querySelectorAll(".sidebar-section");
  var primarySection = null;
  for (var i = 0; i < sections.length; i += 1) {
    if (sections[i].textContent.trim() === "Первичная подача") {
      primarySection = sections[i];
      break;
    }
  }

  if (!primarySection) {
    return;
  }

  var link = document.createElement("a");
  var path = window.location.pathname;
  if (path.indexOf("/blog/") !== -1) {
    link.href = "../docs/legal-stay-in-spain.html";
  } else if (path.indexOf("/docs/") !== -1) {
    link.href = "legal-stay-in-spain.html";
  } else {
    link.href = "docs/legal-stay-in-spain.html";
  }
  link.textContent = "Легальное нахождение";
  primarySection.insertAdjacentElement("afterend", link);
})();

(function (m, e, t, r, i, k, a) {
  m[i] = m[i] || function () {
    (m[i].a = m[i].a || []).push(arguments);
  };
  m[i].l = 1 * new Date();
  k = e.createElement(t);
  a = e.getElementsByTagName(t)[0];
  k.async = 1;
  k.src = r;
  a.parentNode.insertBefore(k, a);
})(window, document, "script", "https://mc.yandex.ru/metrika/tag.js", "ym");

ym(112065150, "init", {
  clickmap: true,
  trackLinks: true,
  accurateTrackBounce: true
});
