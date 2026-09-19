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

// Keep already-generated pages in sync with the shared sidebar source.
// The next run of scripts/update-layout.cjs will bake this link into the HTML;
// until then this guard adds it once and preserves each page's relative path.
(function () {
  function ensureFamilyMemberSidebarLink() {
    var sidebar = document.querySelector(".sidebar");
    if (!sidebar || sidebar.querySelector('a[href$="family-member.html"]')) return;

    var contractLink = sidebar.querySelector('a[href$="contract-work.html"]');
    if (!contractLink) return;

    var link = document.createElement("a");
    link.href = contractLink.getAttribute("href").replace(/contract-work\.html$/, "family-member.html");
    link.textContent = "Член семьи";
    contractLink.insertAdjacentElement("afterend", link);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", ensureFamilyMemberSidebarLink);
  } else {
    ensureFamilyMemberSidebarLink();
  }
})();

// Google Analytics 4
(function () {
  var measurementId = "G-99P57JN7WT";
  var script = document.createElement("script");
  script.async = true;
  script.src = "https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(measurementId);
  document.head.appendChild(script);

  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function () {
    window.dataLayer.push(arguments);
  };

  window.gtag("js", new Date());
  window.gtag("config", measurementId);
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

// Tax calculator interaction guard.
// The calculator itself lives in docs/tax-calculator.html. This small bridge only
// makes control changes robust across browser-restored form state (including bfcache).
(function () {
  function initTaxCalculatorInteractions() {
    var employee = document.getElementById("work-employee");
    var autonomo = document.getElementById("work-autonomo");
    var regular = document.getElementById("regime-regular");
    var beckham = document.getElementById("regime-beckham");
    var income = document.getElementById("monthlyIncome");
    var family = document.getElementById("familyComposition");
    var region = document.getElementById("region");
    var expenses = document.getElementById("monthlyExpenses");

    if (!employee || !autonomo || !regular || !beckham || !income || !family || !region) return;

    var nudging = false;

    function forceRecalculate(source) {
      if (nudging || source === income) return;
      nudging = true;
      try {
        income.dispatchEvent(new Event("input", { bubbles: false }));
      } finally {
        nudging = false;
      }
    }

    // When the employee mode is opened, always start from ordinary IRPF.
    // Otherwise some browsers restore a previously selected Beckham radio button,
    // where region and joint-family taxation intentionally do not affect the tax.
    employee.addEventListener("change", function () {
      if (!employee.checked) return;
      regular.checked = true;
      beckham.checked = false;
      forceRecalculate(employee);
    });

    [regular, beckham, family, region].forEach(function (control) {
      control.addEventListener("change", function () {
        forceRecalculate(control);
      });
      control.addEventListener("input", function () {
        forceRecalculate(control);
      });
    });

    if (expenses) {
      expenses.addEventListener("change", function () {
        forceRecalculate(expenses);
      });
      expenses.addEventListener("input", function () {
        forceRecalculate(expenses);
      });
    }

    // Recalculate once when a restored page becomes visible again.
    window.addEventListener("pageshow", function () {
      if (employee.checked && beckham.checked) {
        regular.checked = true;
        beckham.checked = false;
      }
      forceRecalculate(document.body);
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initTaxCalculatorInteractions);
  } else {
    initTaxCalculatorInteractions();
  }
})();
