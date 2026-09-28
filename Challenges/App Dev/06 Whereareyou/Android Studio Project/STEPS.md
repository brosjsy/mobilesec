# Challenge 02: Whereareyou — Step-by-Step

## 1. Recon
- Decompiled the target, found `LocationService` requests location updates from every provider and caches the most recent fix.

## 2. Vulnerability found
- On `onStartCommand`, the service broadcasts the current location via a plain `sendBroadcast()` with a **public, unprotected action string** (`com.mobisec.intent.action.LOCATION_ANNOUNCEMENT`) and **no `android:permission`** restricting who can receive it.
- Any app — not just an intended companion app — can register a `BroadcastReceiver` for that action and read the `"location"` extra directly. No IPC authentication at all.

## 3. Exploit / solution
- See `LocationService.java` for the target-side vulnerable code (rebuilt here to demonstrate/verify the flaw).
- Exploitation itself is simply: register a `BroadcastReceiver` for `ACTION_ANNOUNCE`, then trigger/wait for the service to run.

## 4. Result
- Location data intercepted — no static flag string; the leak itself is the finding.

## 5. Open & run in Android Studio
1. File → Open → this folder.
2. Let Gradle sync.
3. Run ▶ — `MainActivity` is a stub; the interesting code is `LocationService.java`.
