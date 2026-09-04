// Point the nav CTA at the real scanner once someone is signed in.
//
// Every marketing page's nav button sends visitors to /login?mode=signup, which
// is right for a stranger and wrong for a customer. This upgrades the nav for
// people who already have a session: the CTA becomes "Open dashboard" and the
// now-redundant Sign in link is hidden.
//
// Supabase keeps its session in localStorage, so this needs no SDK on 40+
// static pages. The token's presence is NOT enough on its own -- an expired
// token sticks around in storage, and treating it as signed-in hid the Sign in
// link from people who were actually signed out, leaving them no way back in.
// So the expiry is checked, and anything unparseable or lapsed is treated as
// signed out. Being wrong in that direction only shows an extra link; being
// wrong the other way strands the user.
(function () {
  var KEY = 'sb-uxsmmpujxbzdgxxburxr-auth-token';

  function hasLiveSession() {
    var raw;
    try {
      raw = localStorage.getItem(KEY);
    } catch (e) {
      return false;               // private mode / storage blocked
    }
    if (!raw) return false;

    try {
      var s = JSON.parse(raw);
      // Supabase stores seconds since epoch; some versions nest it.
      var exp = s && (s.expires_at || (s.currentSession && s.currentSession.expires_at));
      if (!exp) return false;
      return (Number(exp) * 1000) > Date.now();
    } catch (e) {
      return false;               // unreadable token: assume signed out
    }
  }

  if (!hasLiveSession()) return;  // leave the page exactly as served

  var cta = document.querySelector('a.nav-cta, a.nav-cta-primary');
  if (cta) {
    cta.setAttribute('href', '/dashboard');
    cta.textContent = 'Open dashboard';
  }

  var links = document.querySelectorAll('nav a[href="/login"], nav a[href="/login.html"]');
  for (var i = 0; i < links.length; i++) links[i].style.display = 'none';
})();
