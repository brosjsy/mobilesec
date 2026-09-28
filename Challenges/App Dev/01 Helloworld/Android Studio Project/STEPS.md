# Challenge 01: Helloworld — Step-by-Step

## 1. The task
The challenge text: "No serious class starts without a hello world. Just
submit an app that prints the string `hello-world-mobisec-edition` on the
system log, with the MOBISEC tag."

This confirms the toolchain (build -> install -> launch -> `Log.i`) works
end to end and that the grading harness's logcat scrape picks up our
output.

## 2. Implementation
`MainActivity.onCreate()` calls:

```java
Log.i("MOBISEC", "hello-world-mobisec-edition");
```

Nothing else — no UI, no permissions, no other components.

## 3. Build & submit
```
cd "Challenges\App Dev\01 Helloworld\Android Studio Project"
gradlew.bat assembleDebug
```
Upload the resulting `app-debug.apk` (kept here as `SUBMITTED APK Challenge
01 Helloworld.apk`) on the challenge's submission page.

## 4. Open & run in Android Studio
1. File -> Open -> this folder.
2. Let Gradle sync.
3. Run on an emulator/device, or `gradlew.bat assembleDebug` from a terminal.
