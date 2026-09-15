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

// Tax calculator: keep the DNV income threshold visibly in sync with family size.
// This is intentionally isolated here so the direct-access calculator stays robust
// even if a browser does not dispatch the same input/change sequence for <select>.
(function () {
  function initTaxCalculatorFamilyThreshold() {
    var familySize = document.getElementById("familySize");
    var monthlyIncome = document.getElementById("monthlyIncome");
    var dnvStatus = document.getElementById("dnvStatus");
    var dnvDetail = document.getElementById("dnvDetail");
    var dnvBadge = document.getElementById("dnvBadge");
    var resultGrid = document.querySelector(".calculator-card[aria-labelledby=\"result-title\"] .result-grid");

    if (!familySize || !monthlyIncome || !dnvStatus || !dnvDetail || !dnvBadge || !resultGrid) return;

    var SMI_MONTH_12 = 17094 / 12;
    var minimumCard = document.getElementById("dnvMinimumCard");

    if (!minimumCard) {
      minimumCard = document.createElement("div");
      minimumCard.id = "dnvMinimumCard";
      minimumCard.className = "result-item";
      minimumCard.innerHTML = '<span class="result-label">Минимальный доход для DNV</span><strong id="dnvMinimumValue" class="result-value">—</strong><span id="dnvMinimumSub" class="result-sub">—</span>';
      resultGrid.insertBefore(minimumCard, resultGrid.firstChild);
    }

    function euro(value, decimals) {
      return new Intl.NumberFormat("ru-RU", {
        style: "currency",
        currency: "EUR",
        minimumFractionDigits: decimals,
        maximumFractionDigits: decimals
      }).format(value);
    }

    function minimumForFamily(size) {
      var multiplier = 2;
      if (size >= 2) multiplier += 0.75;
      if (size > 2) multiplier += (size - 2) * 0.25;
      return SMI_MONTH_12 * multiplier;
    }

    function updateFamilyThreshold() {
      var size = Math.max(1, Number(familySize.value) || 1);
      var income = Math.max(0, Number(monthlyIncome.value) || 0);
      var minimum = minimumForFamily(size);
      var difference = income - minimum;
      var value = document.getElementById("dnvMinimumValue");
      var sub = document.getElementById("dnvMinimumSub");

      if (value) value.textContent = euro(minimum, 2) + " / мес.";
      if (sub) sub.textContent = size === 1 ? "для 1 человека" : "для " + size + " человек";

      dnvStatus.classList.remove("good", "bad");
      if (income >= minimum) {
        dnvStatus.classList.add("good");
        dnvBadge.textContent = "Доход проходит";
        dnvDetail.textContent = "Минимум для " + size + " чел.: " + euro(minimum, 2) + " / мес. Запас: " + euro(difference, 2) + ".";
      } else {
        dnvStatus.classList.add("bad");
        dnvBadge.textContent = "Ниже порога";
        dnvDetail.textContent = "Минимум для " + size + " чел.: " + euro(minimum, 2) + " / мес. Не хватает: " + euro(Math.abs(difference), 2) + ".";
      }
    }

    familySize.addEventListener("change", updateFamilyThreshold);
    familySize.addEventListener("input", updateFamilyThreshold);
    monthlyIncome.addEventListener("change", updateFamilyThreshold);
    monthlyIncome.addEventListener("input", updateFamilyThreshold);
    updateFamilyThreshold();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initTaxCalculatorFamilyThreshold);
  } else {
    initTaxCalculatorFamilyThreshold();
  }
})();
