# Challenge 03: Reachingout — Step-by-Step

## 1. The task
"There is an HTTP server listening on 10.0.2.2:31337 (reachable from within
the emulator where your app is running). The flag is there. It's easy, but
you may need to pro-up your math skills." `10.0.2.2` is the Android
emulator's standard alias for the host machine running it (i.e. the
grading harness's own local services), not a real internet address.

## 2. First real submission (#81997) — the root page is just a pointer
```
GET / response: You can get the flag <a href="http://10.0.2.2:31337/flag">here</a>.
no math expression found in initial response; nothing more to try
```
The root page isn't the math question — it's a link to `/flag`. Fixed the
app to follow any `href` it finds in a response before giving up.

## 3. Second real submission (#81999) — the real form, and why the first POST failed
Following the link showed `/flag` serves an actual HTML form:
```html
How much is 3 + 6?
<form action="/flag" method="POST">
  <input id="answer" name="answer" required type="text" value="">
  <input id="val1" name="val1" type="hidden" value="3">
  <input id="oper" name="oper" type="hidden" value="+">
  <input id="val2" name="val2" type="hidden" value="6">
  <input type="submit" value="Get Flag">
</form>
```
The app correctly parsed `3 + 6 = 9` and tried several submission
conventions, but every GET attempt just returned the same form again, and
the POST attempt (`answer=9` alone) got:
```
POST http://10.0.2.2:31337/flag (answer=9) -> You passed some weird values or your HTTP query was malformed. Something went wrong. Bye.
```
The server expects the hidden `val1`/`oper`/`val2` fields echoed straight
back alongside the answer — not just the computed answer on its own.

## 4. Fixed approach
1. `GET` the URL, log the response.
2. If it contains the flag, done.
3. If it contains a math expression: parse the page's own `<form
   action="..." method="...">` tag and every `<input type="hidden" ...>`
   field directly out of the HTML, build a POST (or GET) body containing
   every hidden field plus the computed `answer`, and submit that to the
   form's own `action` URL. A couple of bare-`answer=` fallbacks are still
   tried afterward in case a different hop's page has no `<form>` at all.
4. If it contains an `href="..."` link instead, follow it (bounded to a
   few hops) and repeat from step 2 at the new URL.

## 5. Confirmed (submission #82002)
The third real submission returned the flag itself:
```
POST http://10.0.2.2:31337/flag (val1=3&oper=%2B&val2=6&answer=9) -> Correct! Here is the flag: MOBISEC{I_was_told_by_liars_that_http_queries_were_easy}
FLAG: MOBISEC{I_was_told_by_liars_that_http_queries_were_easy}
```
Challenge solved.

## 6. Build & submit
```
cd "Challenges\App Dev\03 Reachingout\Android Studio Project"
gradlew.bat assembleDebug
```
Upload `SUBMITTED APK Challenge 03 Reachingout.apk` on the challenge's
submission page. `INTERNET` permission and `usesCleartextTraffic="true"`
are both declared in the manifest since the target is a plain-HTTP local
service.
