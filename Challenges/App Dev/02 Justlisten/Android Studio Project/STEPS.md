# Challenge 02: Justlisten — Step-by-Step

## 1. The task
The flag is announced system-wide with a broadcast Intent, action
`com.mobisec.intent.action.FLAG_ANNOUNCEMENT`, carrying the flag under the
`"flag"` key in its extras. The challenge's own hint warns that recent
Android versions behave differently from older ones for broadcasts, and
points at broadcast-exception documentation.

## 2. The catch (why a plain manifest `<receiver>` isn't safe)
Since Android 8.0 (API 26), the OS silently drops most manifest-declared
`<receiver>` entries for *implicit* broadcasts — this is a device/OS-level
restriction based on the emulator's own Android version, not something our
app's `targetSdkVersion` can opt out of. If the grading emulator is running
API 26+, a `<receiver>` in `AndroidManifest.xml` for `FLAG_ANNOUNCEMENT`
would simply never fire.

The fix: register the receiver **dynamically at runtime** with
`Context.registerReceiver()` instead of declaring it in the manifest.
Dynamically-registered receivers are exempt from that restriction on every
Android version, so this approach is correct regardless of which API level
the analysis emulator actually runs (see
`https://mobisec.reyammer.io/analysis` for the exact version, if needed).

## 3. Implementation
`MainActivity.onCreate()`:
```java
IntentFilter filter = new IntentFilter("com.mobisec.intent.action.FLAG_ANNOUNCEMENT");
registerReceiver(flagReceiver, filter, Context.RECEIVER_EXPORTED); // API 33+
```
`flagReceiver.onReceive()` reads `intent.getStringExtra("flag")` and logs it
with the `MOBISEC` tag; it also dumps every extra key/value defensively, in
case the flag isn't a plain `String` extra.

On API 33+, `Context.RECEIVER_EXPORTED` is required for a dynamically
registered receiver to see a broadcast sent by another app/process — without
it, the system would only deliver broadcasts sent from within our own app.

## 4. Build & submit
```
cd "Challenges\App Dev\02 Justlisten\Android Studio Project"
gradlew.bat assembleDebug
```
Upload `SUBMITTED APK Challenge 02 Justlisten.apk` on the challenge's
submission page.
