// Cloudflare Turnstile bot check, shared by /try, the homepage chat and lead
// form, and email signup on /login.
//
// Off until SITE_KEY is filled in: getToken() then resolves to null and every
// form works exactly as before. With a key, it loads Cloudflare's script on
// first use and runs the check invisibly. Cloudflare only shows a checkbox
// when it isn't sure, inside the element with id "vs-turnstile" if the page
// has one (otherwise a small box pinned to the bottom of the screen).
(function () {
  var SITE_KEY = '0x4AAAAAAFs99bThVIoiwUZL'; // Cloudflare Turnstile site key (public). Empty = off.

  var scriptPromise = null;
  function loadScript() {
    if (window.turnstile) return Promise.resolve();
    if (scriptPromise) return scriptPromise;
    scriptPromise = new Promise(function (resolve, reject) {
      var s = document.createElement('script');
      s.src = 'https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit';
      s.async = true;
      s.onload = function () { resolve(); };
      s.onerror = function () { scriptPromise = null; reject(new Error('Bot check could not load.')); };
      document.head.appendChild(s);
    });
    return scriptPromise;
  }

  function container() {
    var el = document.getElementById('vs-turnstile');
    if (el) return el;
    el = document.createElement('div');
    el.id = 'vs-turnstile';
    el.style.cssText = 'position:fixed;bottom:16px;left:50%;transform:translateX(-50%);z-index:9999';
    document.body.appendChild(el);
    return el;
  }

  var widgetId = null;
  var pending = null;

  // Tokens are single use, so call this once per submit.
  function getToken(action) {
    if (!SITE_KEY) return Promise.resolve(null);
    return loadScript().then(function () {
      return new Promise(function (resolve, reject) {
        pending = { resolve: resolve, reject: reject };
        if (widgetId !== null) window.turnstile.remove(widgetId);
        widgetId = window.turnstile.render(container(), {
          sitekey: SITE_KEY,
          action: action,
          appearance: 'interaction-only',
          callback: function (token) { if (pending) { pending.resolve(token); pending = null; } },
          'error-callback': function () {
            if (pending) { pending.reject(new Error("We couldn't confirm you're human. Refresh the page and try again.")); pending = null; }
            return true;
          },
          'expired-callback': function () { if (widgetId !== null) window.turnstile.reset(widgetId); }
        });
      });
    });
  }

  window.vsTurnstile = { enabled: function () { return !!SITE_KEY; }, getToken: getToken };
})();
