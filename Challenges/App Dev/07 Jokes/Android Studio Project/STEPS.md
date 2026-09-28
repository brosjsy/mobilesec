# Challenge 04: Jokes — Step-by-Step

## 1. Recon
- Decompiled the target, found a `ContentProvider` registered at `content://com.mobisec.provider.Joke/jokes`.

## 2. Vulnerability found
- The provider is exported with **no read-permission requirement**, and applies **no server-side filtering** — any app can query the full `jokes` table directly via `ContentResolver`.

## 3. Exploit / solution
- `MainActivity.java` queries the provider with no restrictions, then filters client-side for rows where `author == "reyammer"`, concatenating the `joke` column of matches in cursor order.

## 4. Result
- Flag reconstructed from the concatenated joke text (see logcat output `FLAG: ...` when run).

## 5. Open & run in Android Studio
1. File → Open → this folder.
2. Let Gradle sync.
3. Run ▶ on a device/emulator that also has the target `com.mobisec.provider` app installed — the query will fail with "provider not found" otherwise.
