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
  if (sidebar) {
    var sections = sidebar.querySelectorAll(".sidebar-section");
    var documentsSection = null;
    var nextSection = null;
    for (var i = 0; i < sections.length; i += 1) {
      if (sections[i].textContent.trim() === "Документы") {
        documentsSection = sections[i];
        nextSection = sections[i + 1] || null;
        break;
      }
    }

    if (documentsSection) {
      var link = sidebar.querySelector('a[href$="legal-stay-in-spain.html"]');
      if (!link) {
        link = document.createElement("a");
        var path = window.location.pathname;
        if (path.indexOf("/blog/") !== -1) {
          link.href = "../docs/legal-stay-in-spain.html";
        } else if (path.indexOf("/docs/") !== -1) {
          link.href = "legal-stay-in-spain.html";
        } else {
          link.href = "docs/legal-stay-in-spain.html";
        }
        link.textContent = "Легальное нахождение";
      }

      if (nextSection) {
        sidebar.insertBefore(link, nextSection);
      } else {
        sidebar.appendChild(link);
      }
    }
  }

  var cells = document.querySelectorAll("table tbody td:first-child");
  for (var j = 0; j < cells.length; j += 1) {
    if (cells[j].textContent.trim() === "Легальное нахождение в Испании" && !cells[j].querySelector("a")) {
      var stayLink = document.createElement("a");
      stayLink.href = window.location.pathname.indexOf("/docs/") !== -1
        ? "legal-stay-in-spain.html"
        : "docs/legal-stay-in-spain.html";
      stayLink.textContent = "Легальное нахождение в Испании";
      cells[j].textContent = "";
      cells[j].appendChild(stayLink);
    }
  }
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
