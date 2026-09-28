# Challenge 04: Justask — Step-by-Step

## 1. The task
The target app (`com.mobisec.justask`) has four activities, each holding
one part of the flag. Each replies with its part in the result Intent of a
`startActivityForResult()` call, so it's a matter of asking each one
correctly and reading its reply.

## 2. Reading the target's manifest (see `Analysis and Scripts/Target AndroidManifest.xml`)
```xml
<activity android:name=".PartOne" android:exported="true"/>
<activity android:name=".PartTwo">
    <intent-filter><action android:name="com.mobisec.intent.action.JUSTASK" /></intent-filter>
</activity>
<activity android:name=".PartThree" android:exported="true" />
<activity android:name=".PartFour">
    <intent-filter><action android:name="com.mobisec.intent.action.JUSTASKBUTNOTSOSIMPLE" /></intent-filter>
</activity>
```
Two different ways to address these four activities:
- **PartOne / PartThree** — `exported="true"` but no custom action, so they
  must be started with an **explicit** Intent (`ComponentName`).
- **PartTwo / PartFour** — no `exported` attribute, but each declares an
  `<intent-filter>` with its own custom action, so they're started with an
  **implicit** Intent using that action (implicit intent-filters make an
  activity exported by default on the API levels this manifest targets).

## 3. Implementation
`MainActivity` chains the four calls through `onActivityResult()`,
starting the next one only after the previous one replies:
```java
Intent i = new Intent();
i.setComponent(new ComponentName("com.mobisec.justask", "com.mobisec.justask.PartOne"));
startActivityForResult(i, REQ_PART_ONE);
// ...
Intent i2 = new Intent("com.mobisec.intent.action.JUSTASK");
i2.setPackage("com.mobisec.justask");
startActivityForResult(i2, REQ_PART_TWO);
```
For each reply, every key in the result Intent's extras `Bundle` is dumped
to logcat under the `MOBISEC` tag (`extra[key] = value`) — since the exact
key holding each flag fragment isn't specified by the challenge, logging
everything guarantees the grading harness's logcat scrape catches it
regardless of the key name.

## 4. Making a cut-off log unambiguous (submission #81998)
The first real submission's log, as viewed, appeared to cut off PartOne's
flag value partway through — unclear whether that was a real truncation or
just a display/paste limit. Two changes make this unambiguous:
- Every extra value is now wrapped in `[START]...[END]` markers — a missing
  `[END]` means it really was cut off, not just hard to read.
- After all four parts reply, every extra key containing `"flag"` is
  concatenated and logged one final time as `COMBINED_FULL = ...`, plus
  again in short 60-character `COMBINED[off..end]` chunks, each easily
  short enough that no log viewer would ever truncate it.

## 5. PartOne's value was real, but the chain went silent (submission #82000)
That fix confirmed `extra[flag] length=11 value=[START]MOBISEC{Ive[END]`
really is the complete 11-character value — not a truncation. But the log
then stopped right after `"asking PartTwo (implicit intent, action
JUSTASK)"`, with no reply and no crash. This platform's own harness only
surfaces `MOBISEC`-tagged log lines (confirmed earlier in this engagement
with the Nojumpstarts challenge), so an uncaught exception from
`startActivityForResult()` — e.g. `ActivityNotFoundException` if the
implicit intent doesn't resolve, or a `SecurityException` — would crash the
app silently, with nothing useful in this log to explain why.

Fixed by wrapping every `startActivityForResult()` call in a `safeStart()`
helper that catches any exception and logs its class name and message
explicitly under the `MOBISEC` tag, so if PartTwo genuinely fails to
resolve on the next run, the exact reason will be visible instead of the
chain just going quiet.

## 6. The exact reason, and a second bug (submission #82003)
That fix paid off immediately. The next real submission showed exactly
what was going wrong, plus something new:
- **PartFour really does fail to resolve**: `safeStart()` caught and logged
  `android.content.ActivityNotFoundException: No Activity found to handle
  Intent { act=com.mobisec.intent.action.JUSTASKBUTNOTSOSIMPLE
  pkg=com.mobisec.justask }`. The target's manifest declares PartTwo and
  PartFour's `<intent-filter>` with only an `<action>`, no `<category>` —
  but `startActivityForResult()` automatically adds `CATEGORY_DEFAULT` to
  outgoing implicit intents, and Android only matches a filter that also
  declares that category. Since neither filter declares it, the safest fix
  is to stop relying on implicit resolution at all: PartTwo and PartFour are
  now started with an **explicit** `ComponentName`, exactly like PartOne and
  PartThree, while still setting the custom action string on the `Intent`
  object in case the target activity itself checks `getAction()`.
- **A second, unrelated bug**: PartThree's reply carries a genuine fragment
  under key `hiddenFlag` (`I_got_the_f`) *and* a decoy taunt sentence under
  a separate key `flag` (107 characters of prose). The `dumpExtras()`
  "key contains flag" heuristic caught both, so `COMBINED_FULL` ended up
  with the decoy text spliced into the real fragments. Fixed by skipping
  any value that contains a space character before appending it to
  `combined` — every genuine fragment seen so far (`MOBISEC{Ive`,
  `I_got_the_f`) is a short underscore-joined token with no spaces, while
  the decoy is a full sentence.

## 7. Build & submit
```
cd "Challenges\App Dev\04 Justask\Android Studio Project"
gradlew.bat assembleDebug
```
Upload `SUBMITTED APK Challenge 04 Justask.apk` on the challenge's
submission page (alongside the target's own `justask.apk`, if the platform
requires uploading both).
