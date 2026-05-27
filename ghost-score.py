#!/usr/bin/env python3
"""
ghost-score.py - Offline digital security audit.
No account. No network calls. One file.
Built by Brainiac Ltd - ghost-os.online
"""

__version__ = "1.0.0"

import sys
import argparse

parser = argparse.ArgumentParser(description="ghost-score: offline digital security audit", add_help=True)
parser.add_argument("--version", action="store_true", help="Print version and exit")
parser.add_argument("--json", action="store_true", help="Output results as JSON and exit")
parser.add_argument("--csv", action="store_true", help="Export scoring schema to ghost-score-results.csv and exit")
args = parser.parse_args()

if args.version:
    print(f"ghost-score v{__version__}")
    sys.exit(0)

from textual.app import App, ComposeResult
from textual.widgets import Static, Button, Label
from textual.containers import Container, Vertical, Horizontal
from textual.screen import Screen
from textual import events
from textual.reactive import reactive
import pyfiglet
import json
import qrcode as _qrcode

GREEN     = "#00FF41"
GREEN_DIM = "#00AA00"
GREEN_DARK= "#003300"
BLACK     = "#000000"
RED_WARN  = "#FF2222"
AMBER     = "#FFAA00"

QUESTIONS = [
    {"id":1,"vector":"Password hygiene","text":"How do you manage your passwords?","options":[("I use a password manager with unique passwords everywhere",8),("I use a password manager but reuse some passwords",5),("I have a system but no password manager",2),("I reuse passwords across sites",0)]},
    {"id":2,"vector":"VPN usage","text":"Do you use a VPN?","options":[("Yes - self-hosted or open-source (WireGuard / Mullvad)",8),("Yes - commercial VPN (NordVPN / ExpressVPN etc)",5),("Only sometimes, on public Wi-Fi",2),("No",0)]},
    {"id":3,"vector":"Device encryption","text":"Are your devices encrypted?","options":[("Full-disk encryption on all devices",8),("Most devices encrypted",5),("Only my phone",2),("Nothing is encrypted",0)]},
    {"id":4,"vector":"Browser privacy","text":"What browser setup do you use?","options":[("Firefox / Librewolf hardened + uBlock Origin",8),("Brave or Firefox with privacy extensions",5),("Chrome or Safari with some extensions",2),("Default browser, no extensions",0)]},
    {"id":5,"vector":"Local backup","text":"How do you back up critical data?","options":[("Encrypted local backup + offsite / encrypted cloud",8),("Regular local backup (external drive)",5),("Cloud only (Google Drive / iCloud etc)",2),("No backup strategy",0)]},
    {"id":6,"vector":"Encrypted comms","text":"How do you communicate sensitive information?","options":[("Signal for all sensitive comms, self-hosted email",8),("Signal or Matrix for some conversations",5),("WhatsApp (metadata exposed)",2),("SMS / standard email only",0)]},
    {"id":7,"vector":"Mesh network capability","text":"Can you communicate if the internet goes down?","options":[("Yes - Meshtastic / LoRa radio or ham setup",8),("Yes - local mesh network (Reticulum / similar)",5),("No, but I know what Meshtastic is",2),("No and I haven't considered it",0)]},
    {"id":8,"vector":"Network awareness","text":"Do you know what's on your home network?","options":[("Yes - router-level monitoring, VLAN segmentation",8),("Yes - I run nmap or similar scans occasionally",5),("I know my main devices but not guests/IoT",2),("No idea what's connected",0)]},
    {"id":9,"vector":"App permissions","text":"How do you manage app permissions?","options":[("Regular audit - location/mic/camera all restricted",8),("I review permissions when installing",5),("I decline obvious ones but don't audit",2),("I accept defaults and never review",0)]},
    {"id":10,"vector":"Two-factor authentication","text":"How do you use 2FA?","options":[("Hardware key (YubiKey) or TOTP app for everything critical",8),("Authenticator app on most accounts",5),("SMS 2FA on some accounts",2),("No 2FA on any accounts",0)]},
    {"id":11,"vector":"Offline power","text":"Can you power critical devices without mains electricity?","options":[("Yes - solar + battery bank or generator",8),("Large power bank for phones and laptop",5),("Small power bank for phone only",2),("Nothing, fully dependent on mains",0)]},
    {"id":12,"vector":"Offline workflow","text":"Can you work if your internet connection fails?","options":[("Yes - local LLM, offline tools, no cloud dependency",8),("Most things work, a few cloud dependencies",5),("Limited - some offline apps but mostly cloud",2),("Completely dependent on internet connectivity",0)]},
]

MAX_SCORE = len(QUESTIONS) * 8

TIERS = [
    (76,"SOVEREIGN",GREEN,"Full operational autonomy. You are the threat model."),
    (51,"HARDENED",GREEN_DIM,"Strong posture. A few gaps worth closing."),
    (26,"AWARE",AMBER,"You know the landscape. Time to close the distance."),
    (0,"EXPOSED",RED_WARN,"Significant exposure. Fix this before it finds you."),
]

WEAKNESSES = {
    1:"Password hygiene  -> Get a password manager. Bitwarden is free and open source.",
    2:"VPN              -> Deploy WireGuard on a VPS or use Mullvad. Zero logs.",
    3:"Encryption       -> Enable LUKS on Linux. FileVault on Mac. BitLocker on Windows.",
    4:"Browser          -> Switch to Librewolf. Install uBlock Origin. Done.",
    5:"Backup           -> 3-2-1 rule: 3 copies, 2 media types, 1 offsite. Encrypt it.",
    6:"Comms            -> Signal. Non-negotiable for sensitive conversations.",
    7:"Mesh network     -> 30 quid Meshtastic node. Works when everything else fails.",
    8:"Network          -> Run nmap and see what is watching you.",
    9:"Permissions      -> Audit every app with location/mic/camera access. Now.",
    10:"2FA             -> TOTP app minimum. YubiKey for anything that matters.",
    11:"Power           -> 20000mAh bank keeps phone and laptop alive for 24hrs.",
    12:"Offline workflow -> Ollama plus local models. Your data stays on your machine.",
}


def get_qr_text(url="https://ghost-os.online"):
    qr = _qrcode.QRCode(version=1, box_size=1, border=1)
    qr.add_data(url)
    qr.make(fit=True)
    matrix = qr.get_matrix()
    lines = []
    for row in matrix:
        line = "".join(["██" if cell else "  " for cell in row])
        lines.append(line)
    return "\n".join(lines)

def get_tier(score):
    for threshold,label,color,desc in TIERS:
        if score >= threshold:
            return label,color,desc
    return TIERS[-1][1],TIERS[-1][2],TIERS[-1][3]

CSS = """
Screen { background: #000000; color: #00FF41; }
.splash-container { align: center middle; height: 100%; width: 100%; }
.splash-title { text-align: center; color: #00FF41; padding: 1 0; }
.splash-sub { text-align: center; color: #00AA00; padding: 0 0 1 0; }
.splash-detail { text-align: center; color: #006600; padding: 0 0 2 0; }
.start-btn { background: #000000; color: #00FF41; border: solid #00FF41; width: 30; content-align: center middle; margin: 1 0; }
.start-btn:hover { background: #003300; }
.question-container { height: 100%; padding: 1 3; }
.progress-bar { color: #00AA00; padding: 0 0 1 0; }
.vector-label { color: #006600; }
.question-text { color: #00FF41; text-style: bold; padding: 1 0; }
.option-btn { background: #000000; color: #00AA00; border: solid #003300; width: 100%; height: 3; content-align: left middle; padding: 0 1; margin: 0 0 1 0; }
.option-btn:hover { background: #001100; border: solid #00FF41; color: #00FF41; }
.results-container { height: 100%; padding: 1 3; overflow-y: auto; }
.score-art { text-align: center; padding: 0 0 1 0; }
.tier-label { text-align: center; text-style: bold; padding: 0 0 1 0; }
.tier-desc { text-align: center; color: #00AA00; padding: 0 0 1 0; }
.score-line { text-align: center; color: #006600; padding: 0 0 2 0; }
.weaknesses-header { color: #00AA00; text-style: bold; padding: 0 0 1 0; }
.weakness-item { color: #006600; padding: 0 0 0 2; }
.cta-block { padding: 2 0 1 0; text-align: center; color: #00AA00; }
.cta-url { text-align: center; color: #00FF41; text-style: bold; }
.qr-code { text-align: center; color: #00FF41; padding: 1 0; }
"""

class SplashScreen(Screen):
    def compose(self) -> ComposeResult:
        fig = pyfiglet.figlet_format("GHOST SCORE", font="doom")
        with Container(classes="splash-container"):
            with Vertical():
                yield Static(fig, classes="splash-title")
                yield Static("[ OFFLINE DIGITAL SECURITY AUDIT ]", classes="splash-sub")
                yield Static(f"12 vectors  {MAX_SCORE} points maximum  zero network calls", classes="splash-detail")
                yield Static(f"v{__version__}  |  ghost-os.online", classes="splash-sub")
                yield Button("[ INITIATE AUDIT ]", id="start", classes="start-btn")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "start":
            self.app.push_screen(QuestionScreen())


class QuestionScreen(Screen):
    current_q = reactive(0)

    def compose(self) -> ComposeResult:
        with Vertical(classes="question-container"):
            yield Static("", id="progress", classes="progress-bar")
            yield Static("", id="vector", classes="vector-label")
            yield Static("", id="question", classes="question-text")
            yield Static("", id="opt0", classes="option-btn")
            yield Static("", id="opt1", classes="option-btn")
            yield Static("", id="opt2", classes="option-btn")
            yield Static("", id="opt3", classes="option-btn")

    def on_mount(self) -> None:
        self.scores = {}
        self.current_q = 0
        self._render_question()

    def _render_question(self) -> None:
        q = QUESTIONS[self.current_q]
        total = len(QUESTIONS)
        idx = self.current_q + 1
        bar_filled = int((self.current_q / total) * 30)
        bar = f"[{'#' * bar_filled}{'.' * (30 - bar_filled)}] {idx}/{total}"
        self.query_one("#progress").update(bar)
        self.query_one("#vector").update(f"// {q['vector'].upper()}")
        self.query_one("#question").update(q["text"])
        for i,(text,points) in enumerate(q["options"]):
            self.query_one(f"#opt{i}").update(f"  [{i+1}]  {text}")

    def on_key(self, event: events.Key) -> None:
        key_map = {"1":0,"2":1,"3":2,"4":3}
        if event.key in key_map:
            self._select(key_map[event.key])

    def _select(self, option_idx: int) -> None:
        q = QUESTIONS[self.current_q]
        _,points = q["options"][option_idx]
        self.scores[q["id"]] = {"vector":q["vector"],"points":points,"max":8}
        if self.current_q + 1 < len(QUESTIONS):
            self.current_q += 1
            self._render_question()
        else:
            self.app.push_screen(ResultsScreen(self.scores))


class ResultsScreen(Screen):
    def __init__(self, scores: dict):
        super().__init__()
        self.scores = scores

    def compose(self) -> ComposeResult:
        total = sum(v["points"] for v in self.scores.values())
        tier_label,tier_color,tier_desc = get_tier(total)
        fig = pyfiglet.figlet_format(tier_label, font="doom")
        weak = [WEAKNESSES[qid] for qid,v in self.scores.items() if v["points"] < v["max"]]
        with Vertical(classes="results-container"):
            yield Static(fig, classes="score-art")
            yield Static(f"[ {tier_label} ]", classes="tier-label")
            yield Static(tier_desc, classes="tier-desc")
            yield Static(f"Score: {total} / {MAX_SCORE}  ({int(total/MAX_SCORE*100)}%)", classes="score-line")
            if weak:
                yield Static("-- PRIORITY FIXES --", classes="weaknesses-header")
                for w in weak:
                    yield Static(f"  > {w}", classes="weakness-item")
            else:
                yield Static("-- NO CRITICAL WEAKNESSES DETECTED --", classes="weaknesses-header")
            yield Static("Full remediation plan + hardware kit:", classes="cta-block")
            yield Static(get_qr_text(), classes="qr-code")
            yield Static("ghost-os.online", classes="cta-url")
            yield Static("[ Q ] quit    [ R ] restart", classes="score-line")

    def on_key(self, event: events.Key) -> None:
        if event.key == "q":
            self.app.exit()
        elif event.key == "r":
            self.app.pop_screen()
            self.app.pop_screen()
            self.app.push_screen(SplashScreen())


class GhostScore(App):
    CSS = CSS

    def on_mount(self) -> None:
        self.push_screen(SplashScreen())


if args.json:
    print(json.dumps({"tool":"ghost-score","version":__version__,"vectors":[q["vector"] for q in QUESTIONS],"max_score":MAX_SCORE,"tiers":[{"min":t[0],"label":t[1]} for t in TIERS]},indent=2))
    sys.exit(0)

if args.csv:
    import csv as _csv
    outfile = "ghost-score-schema.csv"
    with open(outfile, "w", newline="") as f:
        w = _csv.writer(f)
        w.writerow(["id","vector","option","points"])
        for q in QUESTIONS:
            for opt_text, opt_pts in q["options"]:
                w.writerow([q["id"], q["vector"], opt_text, opt_pts])
    print(f"Schema exported to {outfile}")
    sys.exit(0)

if __name__ == "__main__":
    app = GhostScore()
    app.run()
