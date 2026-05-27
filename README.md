# ghost-score

![Python](https://img.shields.io/badge/python-3.8%2B-brightgreen?style=flat-square&color=00AA00&labelColor=000000)
![Platform](https://img.shields.io/badge/platform-linux%20%7C%20macOS%20%7C%20windows-brightgreen?style=flat-square&color=00AA00&labelColor=000000)
![License](https://img.shields.io/badge/license-MIT-brightgreen?style=flat-square&color=00AA00&labelColor=000000)
![Offline](https://img.shields.io/badge/network-zero%20calls-brightgreen?style=flat-square&color=00AA00&labelColor=000000)

**Offline digital security audit. No account. No network calls. One file.**

![ghost-score screenshot](screenshot.png)

---

## What it does

Scores your digital security posture across 12 vectors. Renders your tier in large ASCII art. Gives you a ranked list of weaknesses with specific, actionable fixes.

Takes 3 minutes. Nothing leaves your machine.

---

## Install

```bash
pip install textual pyfiglet colorama
python ghost-score.py
```

That's it.

---

## Requirements

```
textual>=0.50.0
pyfiglet>=0.8.0
colorama>=0.4.6
```

Or:

```bash
pip install -r requirements.txt
```

---

## Verify it yourself

This tool makes one claim: it does not phone home. You can verify that in under 5 minutes.

```bash
# Check for any network calls in the source
grep -n "requests\|urllib\|http\|socket\|connect" ghost-score.py
```

You'll find nothing. The entire tool is 150 lines of Python. Read it before you run it. That's exactly the kind of scrutiny this was built to survive.

---

## Scoring

12 questions. 8 points each. 96 points maximum.

| Score | Tier |
|---|---|
| 76-100 | SOVEREIGN |
| 51-75 | HARDENED |
| 26-50 | AWARE |
| 0-25 | EXPOSED |

---

## Vectors audited

- Password hygiene
- VPN usage
- Device encryption
- Browser privacy
- Local backup
- Encrypted communications
- Mesh network capability
- Network device awareness
- App permissions audit
- Two-factor authentication
- Offline power capability
- Offline workflow capability

---

## Flags

```bash
python ghost-score.py           # run the assessment
python ghost-score.py --version # print version and exit
python ghost-score.py --help    # show usage
python ghost-score.py --csv    # export results to ghost-score-results.csv
```

---

## Contributing

PRs welcome for additional question vectors, new audit categories, or platform-specific fixes.

Open an issue first if you're adding a new scoring category - want to keep the question count intentional.

---

## License

MIT. Use it, fork it, modify it, ship it.

---

*Built by [Brainiac Ltd](https://superchargebuilds.pro). Full remediation plan + hardware kit at [ghost-os.online](https://ghost-os.online).*
