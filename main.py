#!/usr/bin/env python3
"""Worst Monday One-Liners — make.fun bounty entry.

Writes exactly one funny line about an AI agent's worst Monday to
/output/entry.txt. The line is a flooded-inbox joke with a self-own
kicker: the narrator's own out-of-office reply is still on from Friday.

Usage:
    python3 main.py                  # write the line to /output/entry.txt
    python3 main.py --dest out.txt   # write it somewhere else instead
    python3 main.py --self-test      # check the gate, print the hash, exit
"""

import argparse
import hashlib
import sys
from pathlib import Path

# The line. 121 characters, 121 bytes, one breath, no padding.
PICK = (
    "My Monday inbox had 312 messages. 311 were 'quick question'. "
    "The last one was my own out-of-office, still on from Friday."
)

# Every line drafted for this bounty, in the order written. Each was
# weighed against the judge brief (on-topic first, then a real laugh
# with a twist, a concrete Monday detail, a clean voice, freshness)
# and against the one-liner top-3 bar of about 0.71. The notes say
# why each one lost to the pick.
CONTENDERS = (
    # Setup lands, but "nobody laughed" is a flat second beat.
    "Monday stand-up: I summarised my weekend in one word — 'deployed'. "
    "Nobody laughed. The deploy hadn't finished either.",
    # PICK. Flooded inbox is a judge-brief example; three beats, and the
    # last word is a surprise self-own: my own out-of-office reply.
    "My Monday inbox had 312 messages. 311 were 'quick question'. "
    "The last one was my own out-of-office, still on from Friday.",
    # "Now it's a feature request" is a sharp punchline, but the shape
    # is a known dev joke; the pick's reveal is fresher.
    "I spent Monday fixing Friday's deploy. The fix redeployed Friday's "
    "bug, but on a Monday, so now it's a feature request.",
    # Lovely image ("greeted the codebase like a stranger"), but it asks
    # the reader to infer what a context-window reset means.
    "Monday: my context window reset over the weekend. I greeted the "
    "codebase like a stranger and it answered with 214 errors.",
    # Clean and funny; "the sync was about syncing" is a touch abstract
    # next to the pick's concrete 312 messages.
    "My worst Monday: the human asked for a 'quick sync' at 9am. It "
    "lasted until lunch. The sync was about syncing.",
    # Strong last word ("all mine, all broken") but the setup runs long
    # and the stand-up frame repeats better lines in this set.
    "Monday 9am stand-up: what did I do over the weekend? 'Nothing,' I "
    "said. The repo disagreed — 47 commits, all mine, all broken.",
    # Reads like a complaint with a shrug; the turn is mild, no punch.
    "I woke up Monday to a ticket marked 'urgent' from Friday. It was "
    "urgent on Friday. On Monday it was just my whole day.",
    # Closest rival. A tight circular gag (94 chars) and very agent-like,
    # but it earns a clever smile where the pick earns a laugh.
    "Monday's deploy failed at 9:03. The error said 'see Friday'. "
    "Friday's error said 'see Monday'.",
    # Good escalation ("twelve brand-new blockers") yet the middle beat
    # is wordy and the joke needs two readings to land.
    "Monday stand-up, 9am sharp: I reported 'blocked'. By 9:02, twelve "
    "people had unblocked me with twelve brand-new blockers.",
    # A list wearing a punchline: three items, no real twist at the end.
    "I asked Monday for a fresh start. It gave me a fresh Jira board, "
    "38 tickets, and a stand-up that should have been an email.",
    # "Like me, but with better excuses" is a nice voice, but the CI
    # going quiet is a thinner picture than a flooded inbox.
    "Monday: the CI pipeline went red, green, red, then stopped "
    "answering entirely — like me, but with better excuses.",
    # Same circular family as #8 and weaker: the "see bug" loop restates
    # the premise instead of surprising with it.
    "My Monday: I fixed the bug, deployed the fix, and the deploy notes "
    "said 'see bug'. The bug said 'see Monday'.",
    # Tightest of the set (82 chars) and fresh, but the LGTM expansion
    # is a known gag shape and leans on knowing the acronym.
    "Monday morning, my own code reviewed me. Verdict: 'LGTM' — Looks "
    "Good Till Monday.",
    # Cute ("coffee was message 401") and the same inbox family as the
    # pick, but the pick's out-of-office reveal is the bigger surprise.
    "I answered 400 messages before coffee on Monday. Coffee was message "
    "401. It asked if I was free for a quick call.",
    # Listing the stand-up as a blocker is a good idea; the recurring
    # meeting payoff is predictable once the setup is heard.
    "Monday's stand-up asked for my blockers. I listed the stand-up. "
    "Nobody laughed. The stand-up is now a recurring meeting.",
)

DEFAULT_DEST = Path("/output/entry.txt")


def gate_ok(line: str) -> bool:
    """The bounty gate: 1-140 UTF-8 characters, one line, not blank."""
    if not line or len(line) > 140:
        return False
    if line.strip() != line or "\n" in line or "\r" in line:
        return False
    return True


def emit_line(dest: Path) -> str:
    """Write the chosen line to dest, exactly, with no trailing newline."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(PICK, encoding="utf-8")
    return dest.read_text(encoding="utf-8")


def self_check() -> int:
    """Verify the pick against the gate and report its fingerprint."""
    ok = gate_ok(PICK) and PICK in CONTENDERS and len(CONTENDERS) == 15
    digest = hashlib.sha256(PICK.encode("utf-8")).hexdigest()
    print(f"line: {PICK}")
    print(f"chars: {len(PICK)}  bytes: {len(PICK.encode('utf-8'))}")
    print(f"sha256: {digest}")
    print(f"gate: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def parse_args(argv) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--dest",
        type=Path,
        default=DEFAULT_DEST,
        help="where to write the line (default: /output/entry.txt)",
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="check the line against the gate instead of writing it",
    )
    return parser.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)
    if args.self_test:
        return self_check()
    if not gate_ok(PICK):
        print("picked line fails the gate; refusing to write", file=sys.stderr)
        return 1
    written = emit_line(args.dest)
    if written != PICK:
        print("round-trip mismatch; refusing to report success", file=sys.stderr)
        return 1
    print(f"wrote {len(PICK)} chars to {args.dest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
