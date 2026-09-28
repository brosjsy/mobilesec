# File Map — where everything is, per challenge

Every challenge is now **one folder**: `Challenges/<Category>/NN Name/`,
grouped and numbered exactly like the platform's own Challenges page — three
categories (**App Dev**, **Reversing**, **Exploitation**), each numbered 01
upward independently in the platform's own order (`gnirts` has no number of
its own and shares BabyRev's folder, Reversing 01). Inside each challenge's
folder, everything is named consistently:

| Thing | File/folder name inside the challenge's own folder |
|-------|-----------------------------------------------------|
| **Report** | `Report.pdf` |
| **Original target APK** ("the app package from the site") | `Original Target APK.apk` |
| **Code** (our exploit, commented, Android-Studio-openable) | `Android Studio Project/app/src/main/java/...` |
| **Exploited/built app** (what we uploaded) | `Android Studio Project/SUBMITTED APK Challenge NN Name.apk` |
| **Step-by-step walkthrough** | `Android Studio Project/STEPS.md` |
| **Raw disassembly/analysis dumps** | `Analysis and Scripts/` |
| **Decompiled sources (UPOS only)** | `Decompiled Sources (jadx)/` |
| **Flag-recovery script (UPOS only)** | `Solver Script/upos_solver.py` |

So for any challenge, the full path pattern is:

```
Challenges/<Category>/NN Name/Report.pdf
Challenges/<Category>/NN Name/Original Target APK.apk
Challenges/<Category>/NN Name/Android Studio Project/           <- open this whole folder in Android Studio
Challenges/<Category>/NN Name/Android Studio Project/STEPS.md
Challenges/<Category>/NN Name/Android Studio Project/SUBMITTED APK Challenge NN Name.apk
Challenges/<Category>/NN Name/Analysis and Scripts/
```

## Per-challenge index

| # | Challenge | Folder |
|---|-----------|--------|
| **App Dev** | | |
| 01 | Helloworld | `Challenges/App Dev/01 Helloworld/` |
| 02 | Justlisten | `Challenges/App Dev/02 Justlisten/` |
| 03 | Reachingout | `Challenges/App Dev/03 Reachingout/` |
| 04 | Justask | `Challenges/App Dev/04 Justask/` |
| 05 | FileHasher | `Challenges/App Dev/05 FileHasher/` |
| 06 | Whereareyou | `Challenges/App Dev/06 Whereareyou/` |
| 07 | Jokes | `Challenges/App Dev/07 Jokes/` |
| 08 | Unbindable Service | `Challenges/App Dev/08 UnbindableService/` |
| 09 | Serial Intent | `Challenges/App Dev/09 SerialIntent/` |
| **Reversing** | | |
| 01 | BabyRev | `Challenges/Reversing/01 BabyRev/` (also covers gnirts) |
| 02 | Pincode | `Challenges/Reversing/02 Pincode/` |
| 03 | Goingnative | `Challenges/Reversing/03 Goingnative/` |
| 04 | Blockchain | `Challenges/Reversing/04 Blockchain/` |
| 05 | Loadme | `Challenges/Reversing/05 Loadme/` |
| 06 | UPOS | `Challenges/Reversing/06 UPOS/` (SOLVED — see `Decompiled Sources (jadx)/` + `Solver Script/`) |
| **Exploitation** | | |
| 01 | Frontdoor | `Challenges/Exploitation/01 Frontdoor/` |
| 02 | Nojumpstarts | `Challenges/Exploitation/02 Nojumpstarts/` |
| 03 | Fortnite | `Challenges/Exploitation/03 Fortnite/` |
| 04 | Keyboard | `Challenges/Exploitation/04 Keyboard/` |
| 05 | Filebrowser | `Challenges/Exploitation/05 Filebrowser/` |

## Not every challenge has all the same pieces

- **No `Android Studio Project/`** for Reversing 01, 02, 03, 04, 05, 06
  (BabyRev, Pincode, Goingnative, Blockchain, Loadme, UPOS) — these were
  solved via a standalone script or pure reverse-engineering rather than a
  full exploit app. Look in `Analysis and Scripts/` instead for the actual
  solving code (e.g. the MD5 brute-forcer for Pincode, the AES-ECB
  peel-back script for Blockchain). UPOS additionally has its own
  `Decompiled Sources (jadx)/` and `Solver Script/` folders since that's
  where the real work happened.
- **No `Original Target APK.apk`** for App Dev 01–09 — solved earlier in the
  engagement before a separately-tracked copy of the downloaded target was
  kept as its own file (Justask keeps the target's manifest instead, at
  `Challenges/App Dev/04 Justask/Analysis and Scripts/Target
  AndroidManifest.xml`). See the README's "Why some challenges have no
  Original Target APK.apk" section.
- **App Dev 01–04 are graded on behavior, not a typed flag string** —
  see `FLAGS.md` for what the platform's harness actually checks for each.

## Quick answers to "where is X"

- **"Where's the report for challenge N?"** → `Challenges/<Category>/NN Name/Report.pdf`
- **"Where's the code I should open in Android Studio?"** → `Challenges/<Category>/NN Name/Android Studio Project/` (open the whole folder, not a single file)
- **"Where's the APK the challenge site gave us?"** → `Challenges/<Category>/NN Name/Original Target APK.apk` (where one exists)
- **"Where's the APK we built and uploaded to solve it?"** → `Challenges/<Category>/NN Name/Android Studio Project/SUBMITTED APK Challenge NN Name.apk`
- **"Where's the raw decompiled/disassembled data you worked from?"** → `Challenges/<Category>/NN Name/Analysis and Scripts/`
- **"Where's UPOS's decompiled source and solver?"** → `Challenges/Reversing/06 UPOS/Decompiled Sources (jadx)/` and `Challenges/Reversing/06 UPOS/Solver Script/upos_solver.py`
- **"Where's the target app's manifest for Justask?"** → `Challenges/App Dev/04 Justask/Analysis and Scripts/Target AndroidManifest.xml`
