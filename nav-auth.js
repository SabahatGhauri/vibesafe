// Point the nav CTA at the real scanner once someone is signed in.
//
// Every marketing page's nav button sends visitors to /try, which runs the
// anonymous demo-scan endpoint: no history, no one-click fixes, capped per IP.
// That is the right destination for a cold visitor and the wrong one for a
// customer -- a signed-in user clicking "Start free scan" was being routed
// back through the front door instead of into their dashboard.
//
// Supabase keeps its session in localStorage, so presence can be checked
// without pulling in the whole SDK on 40+ static pages. A stale or expired
// token is harmless here: /dashboard re-checks properly and redirects to
// /login if the session is no longer valid.
(function () {
  var KEY = 'sb-uxsmmpujxbzdgxxburxr-auth-token';

  var signedIn = false;
  try {
    signedIn = !!localStorage.getItem(KEY);
  } catch (e) {
    return;               // private mode / storage blocked: leave the page as-is
  }
  if (!signedIn) return;

  var cta = document.querySelector('a.nav-cta');
  if (cta) {
    cta.setAttribute('href', '/dashboard');
    cta.textContent = 'Open dashboard';
  }

  // The separate "Sign in" link is noise once a session exists.
  var links = document.querySelectorAll('nav a[href="/login"], nav a[href="/login.html"]');
  for (var i = 0; i < links.length; i++) links[i].style.display = 'none';
})();
