# Challenge 06: Serial Intent — Step-by-Step

## 1. Recon
- Decompiled the target, found `com.mobisec.serialintent.SerialActivity` exported, returning a `Serializable` `FlagContainer` object as a result extra.

## 2. Vulnerability found
- `FlagContainer.getFlag()` is a **private** instance method — private is a compile-time access-control concept only, not a runtime security boundary at the bytecode level.
- Deserializing the object at all just requires the exact class (name + `serialVersionUID`) on our own classpath.

## 3. Exploit / solution
- Bundled a matching copy of `com.mobisec.serialintent.FlagContainer` into this project (see `app/src/main/java/com/mobisec/serialintent/`) purely so `Intent.getSerializableExtra()` can reconstruct it.
- `MainActivity.java`: `startActivityForResult()` on `SerialActivity`, then in `onActivityResult()` call `getFlag()` reflectively via `setAccessible(true)`.

## 4. Result
- Flag delivered live via reflection (see `Log.e(TAG, "FLAG: " + flag)`).

## 5. Open & run in Android Studio
1. File → Open → this folder.
2. Let Gradle sync.
3. Run ▶ on a device/emulator with the target `com.mobisec.serialintent` app installed.
