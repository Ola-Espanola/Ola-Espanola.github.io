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
