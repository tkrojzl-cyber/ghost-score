# ghost-score

Offline digital security audit. No account. No network calls. One file.

## What it does

Scores your digital security posture across 12 vectors. Renders your tier in large ASCII art. Gives you a ranked list of weaknesses with specific, actionable fixes.

Takes 3 minutes. Nothing leaves your machine.

## Install

```bash
pip install textual pyfiglet colorama
python ghost-score.py
```

That is it.

Requirements:

```
textual>=0.50.0
pyfiglet>=0.8.2
colorama>=0.4.6
```

Or: `pip install -r requirements.txt`

## Verify it yourself

This tool makes one claim: it does not phone home. You can verify that in under 5 minutes.

```bash
grep -n "requests\|urllib\|http\|socket\|connect" ghost-score.py
```

You will find nothing. The entire tool is 150 lines of Python. Read it before you run it. That is exactly the kind of scrutiny this was built to survive.

## Scoring

12 questions. 8 points each. 96 points maximum.

| Score | Tier |
|---|---|
| 76-100 | SOVEREIGN |
| 51-75 | HARDENED |
| 26-50 | AWARE |
| 0-25 | EXPOSED |

## Vectors audited

1. Password hygiene
2. VPN usage
3. Device encryption
4. Browser privacy
5. Local backup
6. Encrypted communications
7. Mesh network capability
8. Network device awareness
9. App permissions audit
10. Two-factor authentication
11. Offline power capability
12. Offline workflow capability

## Flags

```bash
python ghost-score.py            # run the assessment
python ghost-score.py --version  # print version and exit
python ghost-score.py --help     # show usage
python ghost-score.py --csv      # export scoring schema to ghost-score-schema.csv
```

## Contributing

PRs welcome for additional question vectors, new audit categories, or platform-specific fixes. Open an issue first if you are adding a new scoring category. Want to keep the question count intentional.

## License

MIT. Use it, fork it, modify it, ship it.

Built by Brainiac Ltd.

Full remediation plan + hardware kit at [ghost-os.online](https://ghost-os.online).

