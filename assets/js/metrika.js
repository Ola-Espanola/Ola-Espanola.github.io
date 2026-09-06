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
    if (!sidebar) {
      return;
    }

    var existing = Array.prototype.some.call(sidebar.querySelectorAll('a'), function (a) {
      return a.getAttribute('href') && a.getAttribute('href').indexOf('diploma-apostille.html') !== -1;
    });
    if (existing) {
      return;
    }

    var path = window.location.pathname;
    var docsPrefix = path.indexOf('/docs/') !== -1 ? '' : (path.indexOf('/blog/') !== -1 ? '../docs/' : 'docs/');

    var links = sidebar.querySelectorAll('a');
    var workRecordLink = null;
    for (var j = 0; j < links.length; j += 1) {
      var href = links[j].getAttribute('href') || '';
      if (href.indexOf('electronic-work-record.html') !== -1) {
        workRecordLink = links[j];
        break;
      }
    }

    var diplomaLink = document.createElement('a');
    diplomaLink.href = docsPrefix + 'diploma-apostille.html';
    diplomaLink.textContent = 'Апостиль диплома';

    if (workRecordLink) {
      workRecordLink.parentNode.insertBefore(diplomaLink, workRecordLink);
      return;
    }

    var sectionHeadings = sidebar.querySelectorAll('.sidebar-section');
    var referenceSection = null;
    for (var i = 0; i < sectionHeadings.length; i += 1) {
      if (sectionHeadings[i].textContent.trim() === 'Справочник') {
        referenceSection = sectionHeadings[i];
        break;
      }
    }
    if (!referenceSection) {
      return;
    }

    var documentsSection = document.createElement('p');
    documentsSection.className = 'sidebar-section';
    documentsSection.textContent = 'Документы';

    var workRecord = document.createElement('a');
    workRecord.href = docsPrefix + 'electronic-work-record.html';
    workRecord.textContent = 'Выписка из электронной трудовой';

    referenceSection.parentNode.insertBefore(documentsSection, referenceSection);
    referenceSection.parentNode.insertBefore(diplomaLink, referenceSection);
    referenceSection.parentNode.insertBefore(workRecord, referenceSection);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', addDiplomaApostilleLink);
  } else {
    addDiplomaApostilleLink();
  }
})();
