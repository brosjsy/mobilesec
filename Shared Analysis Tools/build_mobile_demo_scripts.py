#!/usr/bin/env python3
"""Generates one "Mobile Demo Script Explanation" PDF per challenge, meant to
be read from live while demonstrating a challenge to a professor. Reuses the
already-verified content from build_reports.py (CH / GNIRTS) instead of
re-deriving anything, so every fact here matches the corresponding Report.pdf.

Style matches the demo scripts already produced by hand for Frontdoor,
Helloworld and Pincode: bold section headers throughout; a plain-language
glossary up front; bold + highlighted key terms/code from the exploit
explanation onward. This is a presentation aid, not a submitted report, so
the "no bold" rule that applies to Report.pdf does not apply here (see
feedback_no_bold_plain_reports memory).

Run:  python "build_mobile_demo_scripts.py"
"""
import os
import sys

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted, PageBreak
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib import colors

sys.path.insert(0, os.path.dirname(__file__))
import build_reports as br  # reuses CH, GNIRTS, P(), ROOT -- the verified source of truth

HIGHLIGHT = colors.HexColor('#fff3b0')

styles = getSampleStyleSheet()
title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontSize=17, textColor=colors.black,
                              alignment=TA_CENTER, fontName='Helvetica-Bold', spaceAfter=8)
h2 = ParagraphStyle('H2', parent=styles['Heading2'], fontSize=12.5, textColor=colors.black,
                     fontName='Helvetica-Bold', spaceBefore=13, spaceAfter=6)
body = ParagraphStyle('Body', parent=styles['BodyText'], fontSize=10, textColor=colors.HexColor('#222222'),
                       alignment=TA_LEFT, spaceAfter=7, leading=14)
say = ParagraphStyle('Say', parent=styles['BodyText'], fontSize=10, textColor=colors.HexColor('#222222'),
                      alignment=TA_LEFT, spaceAfter=6, leading=14.5, leftIndent=14)
code = ParagraphStyle('Code', parent=styles['Normal'], fontSize=8.3, fontName='Courier-Bold',
                       textColor=colors.black, leftIndent=14, spaceAfter=4, leading=11,
                       backColor=HIGHLIGHT, borderPadding=4)
small = ParagraphStyle('Small', parent=styles['BodyText'], fontSize=8.5, textColor=colors.HexColor('#555555'),
                        spaceAfter=4, leading=11)

OUT_ROOT = br.ROOT


def esc(s):
    return (s or "").replace("&", "&amp;")


# ----------------------------------------------------------------------------
# Category-level plain-language glossaries (each demo script is self
# contained, so every one repeats its own category's glossary in full).
# ----------------------------------------------------------------------------
GLOSSARY_APP_DEV = [
    ("What does \"App Dev\" mean, as a category?",
     "On this platform, <b>App Dev</b> challenges ask you to write your own small Android app that behaves "
     "a certain way. This is different from <b>Reversing</b> or <b>Exploitation</b> challenges, where you're "
     "given someone else's app to break into -- here there's usually no separate target app to download at "
     "all. You are writing code from scratch (or talking to a small server the challenge provides) to meet a spec."),
    ("What is an APK?",
     "The installable file for an Android app (like a .exe on Windows). For this category, the APK that "
     "matters is the one <b>you build and submit</b>, not a downloaded target."),
    ("What is logcat / the MOBISEC tag?",
     "Android apps can write messages to the phone's system log, called <b>logcat</b>. The grading harness "
     "watches for lines tagged <b>MOBISEC</b> and checks their content to decide whether to accept the "
     "submission."),
]

GLOSSARY_REVERSING = [
    ("What does \"Reversing\" mean, as a category?",
     "A <b>Reversing</b> challenge gives you someone else's already-built app (an APK) and asks you to "
     "figure out, by reading its code, some secret value it's hiding -- a PIN, a password, a flag string."),
    ("What is an APK, and what does \"decompile\" mean?",
     "An APK is the installable file for an Android app. It ships as compiled code that isn't directly "
     "readable, so we <b>decompile</b> it -- turn it back into readable, Java-like source code -- using a "
     "free tool called <b>jadx</b> (opened as <b>jadx-gui</b>)."),
    ("Why is there no exploit app to build here?",
     "Reversing challenges usually aren't solved by writing an Android app at all -- they're solved by "
     "reading the decompiled logic and then writing a small script (usually Python) that re-implements or "
     "defeats that same logic on a regular computer, offline."),
]

GLOSSARY_EXPLOITATION = [
    ("What does \"Exploitation\" mean, as a category?",
     "An <b>Exploitation</b> challenge gives you a real target Android app with an actual security mistake "
     "in it, and asks you to write a second, small app of your own that takes advantage of that mistake to "
     "get the flag."),
    ("What is a vulnerability?",
     "A mistake in how software was built that lets someone do something the developer never intended -- "
     "here, get the flag without going through the app the normal, intended way."),
    ("What is an APK, and what does \"decompile\" mean?",
     "An APK is the installable file for an Android app. It ships as compiled code that isn't directly "
     "readable, so we <b>decompile</b> it -- turn it back into readable, Java-like source code -- using a "
     "free tool called <b>jadx</b> (opened as <b>jadx-gui</b>) -- to find the mistake in the first place."),
    ("What is a package name?",
     "Every Android app has a unique ID string (like org.naija.fdexploit). Android refuses to install two "
     "different apps that both use the exact same ID, which occasionally trips up a first submission "
     "attempt if the exploit app accidentally reuses the target's own package name."),
]


def glossary_for(category):
    return {"App Dev": GLOSSARY_APP_DEV, "Reversing": GLOSSARY_REVERSING,
            "Exploitation": GLOSSARY_EXPLOITATION}.get(category, GLOSSARY_EXPLOITATION)


def jadx_trail(path):
    """Given a real decompiled-source path on disk, derive the package trail
    jadx-gui would show in its left tree (Source code -> a -> b -> File.java),
    straight from the real directory structure -- never fabricated."""
    norm = path.replace("\\", "/")
    for marker in ("/out/sources/", "/Decompiled Sources (jadx)/"):
        if marker in norm:
            after = norm.split(marker, 1)[1]
            parts = after.split("/")
            return " -> ".join(parts)
    return None


def is_our_own_code(path):
    norm = path.replace("\\", "/")
    return "/Android Studio Project/app/src/main/java/" in norm


def how_got_apk(c):
    folder_abs = br.P(c['folder'])
    target_apk = os.path.join(folder_abs, "Original Target APK.apk")
    if c['category'] == "App Dev":
        manifest_note = ""
        if os.path.exists(os.path.join(folder_abs, "Analysis and Scripts", "Target AndroidManifest.xml")):
            manifest_note = (" The only piece kept from the target side is its own "
                              "<b>AndroidManifest.xml</b>, used to see exactly how its components are "
                              "declared.")
        return (
            "This one doesn't hand you a separate target APK to download at all. The challenge is to "
            "<b>write your own small app</b> that satisfies a spec (often by talking to a small server the "
            "platform runs, or to another running app component)." + manifest_note + " So the only APK in "
            "play here is the one <b>you</b> build and submit -- there's nothing to decompile.")
    if os.path.exists(target_apk):
        return (
            f"The target APK was <b>downloaded directly from the challenge's own page</b> on "
            f"challs.reyammer.io, before doing anything else. A copy of it is kept at:")
    return (
        "The target APK for this one was analyzed earlier in the engagement, before keeping a "
        "separately-tracked copy of every downloaded target became standard practice -- its structure was "
        "worked out directly while decompiling and solving it.")


def how_built(c):
    folder_abs = br.P(c['folder'])
    asp = os.path.join(folder_abs, "Android Studio Project")
    if os.path.exists(asp):
        apk_name = f"SUBMITTED APK Challenge {c['num']} {c['name']}.apk"
        return (
            f"Built as a normal <b>Android Studio project</b> (Gradle). From a terminal: "
            f"<font face='Courier'>cd</font> into its <font face='Courier'>Android Studio Project</font> "
            f"folder and run <font face='Courier'>gradlew.bat assembleDebug</font>. The resulting APK is "
            f"kept right there as <b>{esc(apk_name)}</b>, ready to re-upload.")
    if c.get('diagram_kind') == 'script':
        return (
            "No Android app was built for this one at all. It was solved by <b>decompiling the target with "
            "jadx</b> and then writing a small <b>Python script</b> (or, in a couple of cases, working the "
            "logic out by hand) that re-implements or defeats the exact same check on a regular computer, "
            "offline. The recovered value was then typed directly into the challenge's own flag box.")
    return (
        "Solved directly from the recovered logic; see the code and steps below for exactly how.")


def how_to_explain_flag(c):
    """What to say if the professor asks 'how did you actually get/confirm the
    flag' -- an Android emulator isn't always available to demo live, so this
    points to the real, already-verified evidence instead."""
    folder_abs = br.P(c['folder'])
    asp = os.path.join(folder_abs, "Android Studio Project")
    has_screenshot = bool(c.get('real_screenshots'))
    if os.path.exists(asp) and c.get('log_kind', 'platform') != 'local':
        line = (
            "\"I built my exploit app and uploaded the APK to the platform's own submission page. Their "
            "server ran it automatically against the target and returned the flag in the analysis log.\"")
        if has_screenshot:
            line += (" This is backed by a real screenshot of that exact submission page (see "
                      "<b>Real Screenshot: Live Platform Submission Page</b> in this challenge's Report.pdf), "
                      "not just a claim -- worth pointing to directly if an emulator isn't running.")
        return ("<b>If asked how you got/confirmed the flag:</b> " + line)
    if c.get('diagram_kind') == 'script':
        return (
            "<b>If asked how you got/confirmed the flag:</b> \"I decompiled the target with jadx, recovered "
            "the secret value with a script (no exploit app was built or uploaded for this one), and typed "
            "the recovered flag directly into the challenge site's own flag box.\" There is no APK submission "
            "or platform analysis log for this challenge -- don't claim one.")
    return None


def result_block(story, c):
    story.append(Paragraph("Result", h2))
    if c.get('flag'):
        story.append(Paragraph("The flag this challenge produced:", body))
        story.append(Preformatted(c['flag'], code))
        if c.get('flag_source'):
            story.append(Paragraph(f"Source: {esc(c['flag_source'])}", small))
    if c.get('log'):
        story.append(Paragraph("The real, verbatim output this run produced:", body))
        lines = c['log'].strip().split('\n')
        # keep it to a reasonable on-screen length for a live demo cue card
        for line in lines[-12:]:
            story.append(Preformatted(line, code))


def files_to_open_block(story, c):
    story.append(Paragraph("Files to open", h2))
    folder_abs = br.P(c['folder'])
    target_apk = os.path.join(folder_abs, "Original Target APK.apk")
    step_n = 1
    if os.path.exists(target_apk):
        story.append(Paragraph(f"{step_n}. Open the target APK in jadx-gui:", body))
        story.append(Preformatted(target_apk, code))
        step_n += 1
    for label, path, _maxl in c.get('code_paths', []):
        story.append(Paragraph(f"{step_n}. {esc(label)}:", body))
        story.append(Preformatted(path, code))
        trail = jadx_trail(path)
        if trail:
            story.append(Paragraph(f"In jadx-gui's left tree: Source code -> {esc(trail)}", small))
        elif is_our_own_code(path):
            story.append(Paragraph("This is our own code -- open directly in Android Studio or any text editor.", small))
        step_n += 1


def build_one(c):
    folder_abs = br.P(c['folder'])
    out_path = os.path.join(folder_abs, f"Mobile Demo Script Explanation - {c['name']} ({c['category']}).pdf")

    story = []
    story.append(Paragraph(
        f"Mobile Demo Script Explanation -- {esc(c['name'])} ({esc(c['category'])}, Challenge {c['num']})",
        title_style))
    story.append(Paragraph("Olawoyin Joseph Pamilerin, ISU520196", small))
    story.append(Spacer(1, 8))

    if c.get('key_insight'):
        story.append(Paragraph(f"In one sentence: {esc(c['key_insight'])}", body))

    story.append(Paragraph("Background -- what the terms below mean", h2))
    for term, expl in glossary_for(c['category']):
        story.append(Paragraph(f"<b>{esc(term)}</b> {expl}", body))
    story.append(Spacer(1, 3))

    story.append(Paragraph("How the APK was obtained", h2))
    apk_text = how_got_apk(c)
    story.append(Paragraph(apk_text, body))
    if os.path.exists(os.path.join(folder_abs, "Original Target APK.apk")):
        story.append(Preformatted(os.path.join(folder_abs, "Original Target APK.apk"), code))

    story.append(Paragraph("How the solution was built", h2))
    story.append(Paragraph(how_built(c), body))

    story.append(Paragraph("The vulnerability / technique, in plain terms", h2))
    story.append(Paragraph(c.get('description', ''), body))

    files_to_open_block(story, c)

    if c.get('steps'):
        story.append(Paragraph("What to say -- explanation of the exploit, step by step", h2))
        for i, step in enumerate(c['steps'], 1):
            story.append(Paragraph(f"{i}. {step}", say))

    explain_flag = how_to_explain_flag(c)
    if explain_flag:
        story.append(Paragraph("If an emulator isn't available", h2))
        story.append(Paragraph(explain_flag, say))

    result_block(story, c)

    doc = SimpleDocTemplate(out_path, pagesize=letter, rightMargin=0.75 * inch, leftMargin=0.75 * inch,
                             topMargin=0.75 * inch, bottomMargin=0.75 * inch)
    doc.build(story)
    print(f"  -> {out_path}")


def build_gnirts():
    c = br.GNIRTS
    folder_abs = br.P("Reversing/01 BabyRev")
    out_path = os.path.join(folder_abs, "Mobile Demo Script Explanation - Gnirts (Reversing).pdf")

    story = []
    story.append(Paragraph("Mobile Demo Script Explanation -- Gnirts (Reversing)", title_style))
    story.append(Paragraph("Olawoyin Joseph Pamilerin, ISU520196", small))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "In one sentence: this challenge's flag is checked in five independent pieces, each against its own "
        "target MD5 hash and its own allowed character set, recovered by brute-forcing each piece separately.",
        body))

    story.append(Paragraph("Background -- what the terms below mean", h2))
    for term, expl in GLOSSARY_REVERSING:
        story.append(Paragraph(f"<b>{esc(term)}</b> {expl}", body))
    story.append(Paragraph(
        "<b>What does \"constraint-based brute force\" mean?</b> Instead of guessing the entire flag at "
        "once (which would take far too long), each of the five segments is brute-forced <b>on its own</b>, "
        "each with a smaller, known character set -- which is fast enough to actually finish, then the five "
        "results are joined back together.", body))
    story.append(Spacer(1, 3))

    story.append(Paragraph("How the APK was obtained", h2))
    story.append(Paragraph(
        "Gnirts shares its target APK and its whole analysis folder with <b>BabyRev</b> and <b>Pincode</b> "
        "-- all three were extracted from the same decompile pass. There is no separate Gnirts APK folder "
        "of its own.", body))

    story.append(Paragraph("How the solution was built", h2))
    story.append(Paragraph(
        "No Android app was built. The target was decompiled with jadx to recover each segment's target "
        "hash and character set, then a Python script brute-forced each of the five segments independently "
        "using multiprocessing, and the results were joined into the final flag.", body))

    story.append(Paragraph("Files to open", h2))
    story.append(Paragraph("The brute-force script:", body))
    story.append(Preformatted(br.GNIRTS['code_paths'][0][1], code))

    story.append(Paragraph("What to say -- explanation, step by step", h2))
    for i, step in enumerate([
        "I decompiled the target APK with jadx and found the flag check runs five independent segments, "
        "each comparing an MD5 hash of a candidate substring against its own fixed target hash.",
        "Each segment also only allows a small, specific set of characters, which keeps a brute force of "
        "that segment alone fast even though the whole flag together would be far too slow to guess at once.",
        "I wrote a Python script that brute-forces all five segments in parallel using multiprocessing, "
        "then joins the five recovered pieces into the final flag.",
        "I typed the reassembled flag into the challenge site's flag box to solve it.",
    ], 1):
        story.append(Paragraph(f"{i}. {step}", say))

    story.append(Paragraph("If an emulator isn't available", h2))
    story.append(Paragraph(
        "<b>If asked how you got/confirmed the flag:</b> \"I decompiled the target with jadx, recovered the "
        "flag's five segments with a Python brute-force script (no exploit app was built or uploaded for "
        "this one), and typed the reassembled flag directly into the challenge site's own flag box.\" There "
        "is no APK submission or platform analysis log for this challenge -- don't claim one.", say))

    story.append(Paragraph("Result", h2))
    story.append(Paragraph("Solved via constraint-based brute force; not separately documented as its own "
                            "flag string elsewhere in this engagement's reports (see BabyRev's report or the "
                            "master report for the fuller family write-up).", body))

    doc = SimpleDocTemplate(out_path, pagesize=letter, rightMargin=0.75 * inch, leftMargin=0.75 * inch,
                             topMargin=0.75 * inch, bottomMargin=0.75 * inch)
    doc.build(story)
    print(f"  -> {out_path}")


if __name__ == "__main__":
    print("Building Mobile Demo Script Explanation PDFs for all challenges...")
    for c in br.CH:
        try:
            build_one(c)
        except Exception as e:
            print(f"  WARNING: failed for {c['name']}: {e}")
    build_gnirts()
    print("Done.")
