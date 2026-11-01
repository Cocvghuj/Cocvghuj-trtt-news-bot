(function () {
  "use strict";

  async function syncAffiliateLinks() {
    const response = await fetch("/affiliate-services.json", { cache: "no-cache" });
    if (!response.ok) throw new Error("Affiliate catalog unavailable");
    const catalog = await response.json();
    const services = new Map((catalog.services || []).map((service) => [service.id, service]));

    document.querySelectorAll("a[data-affiliate-id]").forEach((anchor) => {
      const service = services.get(anchor.dataset.affiliateId);
      if (!service || !service.url) return;

      const destination = new URL(service.url, window.location.href);
      const current = new URL(anchor.href, window.location.href);
      const subId = current.searchParams.get("sub_id");
      if (subId) destination.searchParams.set("sub_id", subId);

      anchor.href = destination.toString();
      anchor.target = "_blank";
      anchor.rel = "sponsored nofollow noopener noreferrer";
    });
  }

  syncAffiliateLinks().catch((error) => {
    // Keep the server-rendered affiliate URLs usable if the catalog cannot load.
    console.warn("Affiliate links kept their fallback URLs:", error);
  });
})();
