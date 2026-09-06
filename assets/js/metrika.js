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

(function () {
  function addDiplomaApostilleLink() {
    var sidebar = document.querySelector('.sidebar');
    if (!sidebar || sidebar.querySelector('a[href="diploma-apostille.html"]')) {
      return;
    }

    var workRecordLink = sidebar.querySelector('a[href="electronic-work-record.html"]');
    if (!workRecordLink) {
      return;
    }

    var link = document.createElement('a');
    link.href = 'diploma-apostille.html';
    link.textContent = 'Апостиль диплома';
    workRecordLink.parentNode.insertBefore(link, workRecordLink);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', addDiplomaApostilleLink);
  } else {
    addDiplomaApostilleLink();
  }
})();
