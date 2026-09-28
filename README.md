# MOBISEC Challenge — Master Index

Everything from this engagement. Each challenge is now a single,
self-contained folder under `Challenges/<Category>/` — report, code,
original target APK, and the APK we built and submitted, all together in
one place.

**Easiest challenge to walk a professor through: Exploitation 01,
Frontdoor** — see "Which one is easiest to explain" near the bottom for why.

## Numbering note

Challenge folders are now organized and numbered exactly like the
platform's own Challenges page: three category groups (**App Dev**,
**Reversing**, **Exploitation**), each numbered 01 upward in the same order
the platform lists them in that category. So "Challenge 01" now means a
different challenge depending on category — App Dev 01 is Helloworld,
Reversing 01 is BabyRev, Exploitation 01 is Frontdoor — and every report's
"Category" line makes that unambiguous. `gnirts` still has no separate
folder/number — it shares BabyRev's folder (Reversing 01), same as before.
An earlier revision numbered every challenge 01–20 in one flat platform-wide
sequence; this one regroups those same 20 folders by category to mirror the
platform's own "app dev" / "reversing" / "exploitation" tabs.

## Folder layout

```
MOBISEC Challenge/
├── README.md                    <- this file
├── FLAGS.md                     <- every flag, in one table
├── FILE MAP.md                  <- quick per-challenge file lookup
├── MOBISEC Professional Report BW.pdf   <- combined report, all 21 challenges, grouped by category
├── Reports By Category/         <- the 20 individual Report.pdf files, copied into
│   ├── App Dev/                    3 folders matching the platform's own category
│   ├── Reversing/                  tabs (App Dev / Reversing / Exploitation) -- grab
│   └── Exploitation/               the one you need to submit, nothing combined
├── Shared Analysis Tools/       <- reusable DEX/ELF disassembler + report-builder scripts
└── Challenges/
    ├── App Dev/
    │   ├── 01 Helloworld/
    │   │   ├── Report.pdf                      <- the write-up (includes a project-layout diagram)
    │   │   └── Android Studio Project/         <- code + submitted APK, open in Android Studio
    │   │       ├── SUBMITTED APK Challenge 01 Helloworld.apk
    │   │       ├── STEPS.md                    <- numbered walkthrough
    │   │       ├── app/src/main/java/...       <- commented source
    │   │       └── gradlew(.bat), build.gradle <- opens directly, no setup
    │   ├── 02 Justlisten/   (same shape)
    │   ├── 03 Reachingout/  (same shape)
    │   ├── 04 Justask/
    │   │   ├── Report.pdf
    │   │   ├── Android Studio Project/
    │   │   └── Analysis and Scripts/Target AndroidManifest.xml  <- the target app's own manifest
    │   ├── 05 FileHasher/   (same shape as 01–04)
    │   ├── 06 Whereareyou/, 07 Jokes/, 08 UnbindableService/, 09 SerialIntent/
    ├── Reversing/
    │   ├── 01 BabyRev/
    │   │   ├── Report.pdf
    │   │   ├── Original Target APK.apk         <- the APK downloaded from the challenge site
    │   │   └── Analysis and Scripts/           <- brute-force script / disassembly dumps (also covers gnirts)
    │   ├── 02 Pincode/, 03 Goingnative/, 04 Blockchain/, 05 Loadme/
    │   └── 06 UPOS/
    │       ├── Report.pdf
    │       ├── Original Target APK.apk
    │       ├── Analysis and Scripts/           <- raw unzipped APK, jadx-run notes
    │       ├── Decompiled Sources (jadx)/      <- FC.java, Streamer.java (the files that mattered)
    │       └── Solver Script/upos_solver.py    <- the Python flag-recovery script
    └── Exploitation/
        ├── 01 Frontdoor/, 02 Nojumpstarts/, 03 Fortnite/, 04 Keyboard/
        └── 05 Filebrowser/
```

Every `Challenges/<Category>/NN Name/` folder holds up to five things:

| Thing | File/folder name | Present for |
|-------|-------------------|-------------|
| **Report** | `Report.pdf` | all 20 |
| **Original target APK** (downloaded from the challenge site) | `Original Target APK.apk` | 12 of 20 — see gap note below |
| **Code + submitted APK** | `Android Studio Project/` (open this whole folder in Android Studio; the built APK sits inside it as `SUBMITTED APK *.apk`) | the 14 challenges that needed a custom app (10 exploits + the 4 warm-ups) |
| **Raw analysis material** | `Analysis and Scripts/` | the challenges solved via script/reverse-engineering rather than a full app, plus a few others where the raw disassembly dumps were kept, plus Justask's copy of the target's manifest |
| **Decompiled sources + solver script** | `Decompiled Sources (jadx)/`, `Solver Script/` | UPOS only — solved by pure static analysis, no exploit APK was submitted |

### Which challenges have which

| # | Challenge | Report | Original APK | Android Studio Project | Analysis/Scripts |
|---|-----------|:---:|:---:|:---:|:---:|
| **App Dev** | | | | | |
| 01 | Helloworld | ✅ | — | ✅ | — |
| 02 | Justlisten | ✅ | — | ✅ | — |
| 03 | Reachingout | ✅ | — | ✅ | — |
| 04 | Justask | ✅ | — | ✅ | ✅ (target's manifest) |
| 05 | FileHasher | ✅ | — | ✅ | — |
| 06 | Whereareyou | ✅ | — | ✅ | — |
| 07 | Jokes | ✅ | — | ✅ | — |
| 08 | Unbindable Service | ✅ | — | ✅ | — |
| 09 | Serial Intent | ✅ | — | ✅ | — |
| **Reversing** | | | | | |
| 01 | BabyRev | ✅ | ✅ | — | ✅ |
| 02 | Pincode | ✅ | ✅ | — | ✅ |
| 03 | Goingnative | ✅ | ✅ | — | ✅ |
| 04 | Blockchain | ✅ | ✅ | — | ✅ |
| 05 | Loadme | ✅ | ✅ | — | ✅ |
| 06 | UPOS | ✅ | ✅ | — (jadx `Decompiled Sources` + `Solver Script` instead) | ✅ |
| **Exploitation** | | | | | |
| 01 | Frontdoor | ✅ | ✅ | ✅ | ✅ |
| 02 | Nojumpstarts | ✅ | ✅ | ✅ | ✅ |
| 03 | Fortnite | ✅ | ✅ | ✅ | ✅ |
| 04 | Keyboard | ✅ | ✅ | ✅ | ✅ |
| 05 | Filebrowser | ✅ | ✅ | ✅ | ✅ |

Package names inside every `Android Studio Project` (`org.naija.*`) are
deliberately distinct from the target's own package (`com.mobisec.*`) — the
grading harness installs the real target first, and a colliding package
name on the uploaded APK fails installation (hit this directly with an
early Frontdoor submission before fixing it).

To rebuild any project from a terminal instead of Android Studio:

```
cd "Challenges\<Category>\NN Name\Android Studio Project"
gradlew.bat assembleDebug
```

The resulting APK lands in `app\build\outputs\apk\debug\app-debug.apk`
(the same bytes as the `SUBMITTED APK *.apk` already sitting in that folder).

## Why some challenges have no "Original Target APK.apk"

App Dev 01–04 (the warm-ups) and 05, 06, 07, 08, 09 were solved earlier
in this engagement, before the practice of keeping a separately-tracked copy
of the downloaded target APK was established. The target's structure was
worked out directly while building each solution instead (for Justask, the
target's `AndroidManifest.xml` was kept separately — see
`Analysis and Scripts/Target AndroidManifest.xml` in that folder). Everything
needed to understand and rebuild the solution is still fully present in
each challenge's `Android Studio Project/`.

## Reports grouped by challenge type

`Reports By Category/` is **not** a combined document — it's plain copies of
the same 20 individual `Report.pdf` files that already live in each
`Challenges/<Category>/NN Name/` folder, sorted into three subfolders that
mirror the platform's own category tabs (**app dev**, **reversing**,
**exploitation** — visible on the Challenges page). The point is to make it
fast to find and grab the one report you need to submit, without opening 20
folders to find it:

| Folder | Challenges included |
|--------|---------------------|
| `Reports By Category/App Dev/` | 01 Helloworld, 02 Justlisten, 03 Reachingout, 04 Justask, 05 FileHasher, 06 Whereareyou, 07 Jokes, 08 Unbindable Service, 09 Serial Intent |
| `Reports By Category/Reversing/` | 01 BabyRev, 02 Pincode, 03 Goingnative, 04 Blockchain, 05 Loadme, 06 UPOS (gnirts has no standalone report of its own — see the note file in this folder) |
| `Reports By Category/Exploitation/` | 01 Frontdoor, 02 Nojumpstarts, 03 Fortnite, 04 Keyboard, 05 Filebrowser |

This numbering matches the `Challenges/` folder structure above — each
category's reports are numbered 01 upward independently, the same way the
platform lists them under its own "app dev" / "reversing" / "exploitation"
tabs. Each file is named `Challenge NN Name - Report.pdf`. Regenerated by the same
`build_reports.py` that builds everything else — it copies, it doesn't
regenerate content twice.

## Report diagrams

Every `Report.pdf` (individual and the combined `MOBISEC Professional Report
BW.pdf`) includes a project-layout diagram: the real file tree on the left
and the real source code on the right, generated by
`Shared Analysis Tools/android_studio_diagram.py` from the actual files on
disk. To rebuild all reports after any code/flag change:

```
cd "Shared Analysis Tools"
python build_reports.py
```

## Which one is easiest to explain

**Exploitation 01, Frontdoor**, by a clear margin. Reasons, ranked by how much
they matter for a live walkthrough:

1. **One root cause, one sentence.** "The app has a hardcoded debug password
   left in it that we found by reading the decompiled code." No IPC concept,
   no cryptography, no classloader internals, no timing — just a literal
   string sitting in the bytecode.
2. **The exploit is a single HTTP GET request.** `MainActivity.java` in
   `Challenges/Exploitation/01 Frontdoor/Android Studio Project/` is ~40 lines
   and does nothing but call one URL with the found credentials and print
   the response. It could be demoed with `curl` just as easily as with the
   Android app.
3. **It maps directly onto a well-known real-world bug class** ("debug/test
   credentials shipped in production"), so a professor doesn't need any
   Android-specific background to immediately understand why it matters.
4. **The failure-and-fix story is short and instructive on its own**: first
   submission attempt used the unmodified target APK and failed with a
   package-name collision — a two-sentence, easy-to-follow detour that
   itself teaches something (see that challenge's `STEPS.md`, step 3).

If an even simpler, non-Android-specific opener is wanted first,
**App Dev 01 (Helloworld)** is literally one `Log.i()` call, and
**App Dev 07 (Jokes)** is one unprotected `ContentProvider` query (though
that needs briefly explaining what a `ContentProvider` is); **App Dev 06
(Whereareyou)** is one unprotected broadcast, similarly needs the
`BroadcastReceiver` concept explained first. Everything in the Reversing and
Exploitation categories involves at least two chained vulnerabilities or a
non-trivial crypto/classloader/timing detail, making them better "depth"
demonstrations but weaker "quick and clear" ones.

**UPOS (Reversing 06)** is the most mathematically interesting to present if
the audience wants to see cryptanalysis rather than app exploitation — it's
"predict a fake random-number generator, then reverse a lookup table," with
no Android-specific concepts at all.

All 21 challenges are now solved and confirmed on the live platform. UPOS
(Reversing 06) was the last of the "main" 16 to close: decompiled with
jadx, reverse-drove the LFSR (`Streamer.java`) and 256×256 perfect-square
lookup table (`assets/lotto.dat`) referenced from `FC.checkFlag()`,
recovered the flag character-by-character, verified it by an exact SHA-256
match against the hash hardcoded in the app itself
(`4193d9b72a5c4805e9a5cc739f8a8fc23b2890e13b83bb887d96f86c30654a12`), then
submitted it to the live CTFd flag box, where it was **accepted**. The four
warm-ups (App Dev 01–04) were solved even earlier (2026-09-21) but only
given full write-ups, code, and reports in a later revision.
