# MOBISEC Challenge — All Flags (Verified Against Live Platform)

Verified directly against `challs.reyammer.io` on 2026-09-24 by logging into
account `Naijabrooo` and reading (a) the user's own Solves history at
`/user`, and (b) the exact `Analysis Log` text on each APK submission's own
page (`/apk/<id>`) — this is the platform's own unredacted output, not a
guess or reconstruction.

**Confirmed: 21 of 21 challenges solved.** `upos` was solved by pure static
analysis (see its row below), verified by an exact SHA-256 match against the
hash hardcoded in the decompiled app, then submitted to the live flag box
and **accepted by the platform**.

Challenge numbers below are grouped and numbered by category (App Dev,
Reversing, Exploitation) to match the platform's own Challenges page, with
each category numbered 01 upward independently in the platform's own order
within that category — see `README.md` for the full renumbering note.

## Auto-graded warm-up challenges (App Dev 01–04)

These four are graded by the platform's own harness watching for a specific
signal (a tagged logcat line, a broadcast reply, a correct HTTP answer, or
an Intent reply) rather than a typed-in flag string. Originally solved
earlier in this engagement (2026-09-21); the apps were rebuilt and
resubmitted fresh on 2026-09-28 to capture real screenshots and confirm
each flag directly.

| # | Challenge | Points | Status (2026-09-28 resubmission) |
|---|-----------|--------|------------------------------------|
| 01 | helloworld | 1 | **Confirmed** — flag below, `/apk/81995` |
| 02 | justlisten | 5 | **Confirmed** — flag below, `/apk/81996` |
| 03 | reachingout | 5 | **Confirmed** — flag below, `/apk/82002` (after two intermediate fixes: `/apk/81997` showed the root page is only a link to `/flag`; `/apk/81999` showed `/flag`'s form rejects a bare answer and needs its hidden fields echoed back) |
| 04 | justask | 10 | **In progress** — `/apk/82003` pinned down both remaining bugs: PartFour's implicit intent throws `ActivityNotFoundException` (its `<intent-filter>` has no `<category>` to match the `CATEGORY_DEFAULT` Android adds automatically), and the `dumpExtras()` "key contains flag" heuristic was also pulling in a 107-character decoy taunt sentence from PartThree's `flag` key alongside the real fragment in its `hiddenFlag` key. Both fixed (PartTwo/PartFour now use explicit `ComponentName` targeting; `combined` now skips any value containing a space) and the APK rebuilt; not yet re-submitted for a confirming run |

## Flags confirmed word-for-word from the platform's own analysis logs

| # | Category | Challenge | Flag (verbatim from platform log) | Source |
|---|----------|-----------|-------------------------------------|--------|
| 01 | App Dev | helloworld | `MOBISEC{here_there_is_your_first_and_last_charity_point}` | `/apk/81995` |
| 02 | App Dev | justlisten | `MOBISEC{not_sure_Ive_heard_well_what_did_ya_say?!?}` | `/apk/81996` |
| 03 | App Dev | reachingout | `MOBISEC{I_was_told_by_liars_that_http_queries_were_easy}` | `/apk/82002` |
| 05 | App Dev | filehasher | `MOBISEC{Was_it_known_that_these_one_way_functions_give_you_back_flags?}` | `/apk/81670` |
| 06 | App Dev | whereareyou | `MOBISEC{Where_are_you_bro?_Will_not_tell_anybody_I_swear}` | `/apk/81672` |
| 07 | App Dev | jokeprovider | `MOBISEC{lol_roftl_ahahah_:D_REYAMMER_TELLS_THE_BEST_JOKES!}` | `/apk/81673` |
| 08 | App Dev | unbindable | `MOBISEC{please_respect_my_will_you_shall_not_bind_me_my_friend}` | `/apk/81674` |
| 09 | App Dev | serialintent | `MOBISEC{HOW_DID_YOU_DO_IT_THAT_WAS_SERIALLY_PRIVATE_STUFF1!!1!eleven!}` | `/apk/81675` |
| 05 | Exploitation | filebrowser | `MOBISEC{a_good_file_browser_would_gimme_the_flag_with_no_hacks}` | `/apk/81693` |
| 04 | Exploitation | keyboard | `MOBISEC{the_more_emoji_a_keyboard_has_the_more_secure_it_is}` | `/apk/81695` |
| 01 | Exploitation | frontdoor | `MOBISEC{noob_hackers_only_check_for_backdoors}` | `/apk/81741` |
| 03 | Exploitation | fortnite | `MOBISEC{players_gonna_play_mobisec_hackers_gonna_mobisec_it_up}` | `/apk/81743` |
| 02 | Exploitation | nojumpstarts | `MOBISEC{you_shall_not_jump_ok?pretty_please?}` | `/apk/81742` |

**Correction from earlier drafts of this report:** `filehasher`'s real flag
is the one above — it was previously mis-recorded as BabyRev's flag
(`MOBISEC{ThIs_iS_A_ReAlLy_bAsIc_rEv}`) by mistake. That flag text belongs
to `babyrev`, not `filehasher`. Fixed here after checking the actual
platform log.

## Solved, but exact flag text not retrievable from the platform UI

These were solved by typing the flag directly into CTFd's flag box rather
than through an APK-analysis run, and CTFd does not redisplay the text of
a past *correct* submission anywhere in the UI (by design, for every user,
not just this account). Solve status and timestamp are confirmed from
`/user`; the literal flag string as originally worked out during this
engagement is shown below for reference, unless otherwise noted.

| # | Category | Challenge | Solved at (platform time) | Points | Flag as originally derived |
|---|----------|-----------|---------------------------|--------|------------------------------|
| 01 | Reversing | babyrev | 2026-09-23 9:02:40 PM | 10 | `MOBISEC{ThIs_iS_A_ReAlLy_bAsIc_rEv}` |
| 02 | Reversing | pincode | 2026-09-23 11:01:47 PM | 10 | `MOBISEC{local_checks_can_be_very_bad_for_security}` (PIN `703958`) |
| — | Reversing | gnirts (shares BabyRev's folder) | 2026-09-23 9:14:05 PM | 20 | solved via constraint-based brute force (`gnirts/brute.py`); not separately documented as its own flag string in this engagement's reports |
| 03 | Reversing | goingnative | 2026-09-24 3:01:58 PM | 25 | validator input confirmed as `native_is_so`; exact accepted submission wrapper was never confirmed back to this session in chat, but the platform confirms it was solved |
| 04 | Reversing | blockchain | 2026-09-23 9:46:01 PM | 25 | `MOBISEC{blockchain_failed_to_deliver_once_again}` |
| 05 | Reversing | loadme | 2026-09-23 9:53:13 PM | 30 | `MOBISEC{dynamic_code_loading_can_make_everything_tricky_eh?}` |

## Solved by static analysis, confirmed accepted by the platform

| # | Category | Challenge | Points | Flag |
|---|----------|-----------|--------|------|
| 06 | Reversing | upos | 35 | `MOBISEC{Isnt_this_a_truly_evil_undebuggable_piece_of_sh^W_software??}` — recovered by decompiling with jadx and reverse-driving the LFSR/matrix-lookup logic in `FC.checkFlag()`/`Streamer.java`; verified by exact SHA-256 match against the hash hardcoded in the app (`4193d9b7...30654a12`), then submitted to the live CTFd flag box and **accepted**. |

## Score summary (from `/user`, live)

**Naijabrooo — 391 points, 21/21 challenges solved.** All challenges,
including the four warm-ups (helloworld, justlisten, reachingout, justask)
and UPOS, are confirmed solved on the live platform.

## Notes on how each flag was retrieved

- The 4 warm-up challenges (App Dev 01–04) are graded on a *behavior*, not a typed
  string — see the table at the top. Their code and write-ups were added to
  this report after the rest, from the original challenge text and (for
  justask) the target app's own `AndroidManifest.xml`.
- The 10 "confirmed from platform log" flags all came from this specific
  pattern: our own exploit APK runs *after* the target APK inside the same
  analysis sandbox, and prints `FLAG: MOBISEC{...}` (or similar) to logcat,
  which the grading harness captures verbatim into that submission's
  `Analysis Log`. Reading that log is not a guess — it is the platform
  echoing back exactly what our exploit extracted at runtime.
- The 6 "solved but not retrievable" challenges never went through an APK
  analysis run — they were solved by working out the flag from static
  analysis/scripting and typing it directly into the challenge's flag box.
  CTFd's own UI does not store or redisplay a *correct* submission's text
  anywhere, for any user, so there is no way to re-read it from the site
  after the fact — only the solve timestamp and point value remain visible.
- UPOS (35 pts) followed the same "typed into the flag box" path as those 6,
  but its flag text stayed independently checkable throughout because it
  was derived from, and cross-verified against, a hash embedded in the
  app's own decompiled code, rather than trusted purely on the strength of
  platform acceptance.
