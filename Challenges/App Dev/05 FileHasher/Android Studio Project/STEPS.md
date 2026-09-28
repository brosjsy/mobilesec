# Challenge 01: FileHasher — Step-by-Step

## 1. Recon
- Downloaded the target APK, unzipped it, decompiled `classes.dex`.
- Manifest had no launcher activity declared — installing/launching it directly failed with "Failed to find main activity".

## 2. What this challenge actually checks (correction)
- This is an **"app dev"** category challenge, not a vulnerability exploit: the grading harness's own `com.mobisec.filehasher` target app writes a random file, sends an explicit Intent (`action com.mobisec.intent.action.HASHFILE`) to **our** `HashActivity` asking it to hash that file, and checks whether the SHA-256 our activity returns matches the hash it independently computed.
- The task is simply to correctly implement the receiving side of that IPC contract: `HashActivity` is exported, reads the file at the Intent data URI, computes SHA-256, and returns it as a result extra.

## 3. Fix applied so the app could even run
- Added `MainActivity` with a `MAIN`/`LAUNCHER` intent-filter (see `MainActivity.java`) purely so the APK is installable/launchable — this activity does nothing else.

## 4. Implementation
- `HashActivity.calcHash(Uri)` — SHA-256, streamed in 8KB chunks, returned as lowercase hex in the `"hash"` result extra.

## 5. Result (verified against the live platform, submission #81670)
- Real analysis log excerpt:
  ```
  I have received the following hash: aed8863481d9917aa891dfdfe0a157cad4dfa6ee775cf5dd48789cf7f9da1df8
  I was expecting the following hash: aed8863481d9917aa891dfdfe0a157cad4dfa6ee775cf5dd48789cf7f9da1df8
  They match! good job, here is the flag: MOBISEC{Was_it_known_that_these_one_way_functions_give_you_back_flags?}
  ```
- Flag: `MOBISEC{Was_it_known_that_these_one_way_functions_give_you_back_flags?}`
- (An earlier draft of this file had mistakenly listed BabyRev's flag here instead — corrected after checking the live platform log directly.)

## 6. Open & run in Android Studio
1. File → Open → this folder.
2. Let Gradle sync (uses the bundled SDK via `local.properties`).
3. Run ▶ on an emulator/device, or `gradlew.bat assembleDebug` from a terminal.
