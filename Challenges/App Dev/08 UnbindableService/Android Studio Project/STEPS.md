# Challenge 05: Unbindable Service — Step-by-Step

## 1. Recon
- Decompiled the target, found `com.mobisec.unbindable.UnbindableService` exported and speaking a `Messenger`-based protocol (`MSG_REGISTER_CLIENT`, `MSG_GET_FLAG`).

## 2. Vulnerability found
- The service is bindable by **any app** — no permission requirement — and hands the flag to whoever sends `MSG_GET_FLAG` after registering, with no signature/identity check on the caller at all.

## 3. Exploit / solution
- `MainActivity.java`:
  1. `bindService()` on the target's exact component.
  2. On connect, send `MSG_REGISTER_CLIENT` with our own reply `Messenger`.
  3. Send `MSG_GET_FLAG`.
  4. Read the flag out of the `Bundle` the service replies with.

## 4. Result
- Flag delivered live in the reply `Bundle` (see `Log.e(TAG, "FLAG: " + flag)`).

## 5. Open & run in Android Studio
1. File → Open → this folder.
2. Let Gradle sync.
3. Run ▶ on a device/emulator with the target `com.mobisec.unbindable` app installed.
