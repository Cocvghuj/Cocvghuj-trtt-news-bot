// Direct Blogger posting is intentionally disabled in this public client-side script.
// A PIN embedded in JavaScript is visible to every visitor and is not authentication.
// Use Blogger's authenticated dashboard or a server-side endpoint with proper authorization.
(function () {
  if (window.TRTT_DIRECT_POST_LOADED) return;
  window.TRTT_DIRECT_POST_LOADED = true;
  window.trttDirectPost = function () {
    alert("Direct posting is disabled here. Please sign in to Blogger and create or review the post in the authenticated dashboard.");
    return false;
  };
})();
