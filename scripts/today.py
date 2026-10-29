"""Render the neofetch-style profile card (dark_mode.svg and light_mode.svg).

Fetches GitHub stats through the GraphQL API and writes both SVGs to the
repository root. Uses only the standard library.

    GITHUB_TOKEN=... python scripts/today.py
"""

import datetime
import json
import os
import urllib.request
from pathlib import Path
from xml.sax.saxutils import escape
from zoneinfo import ZoneInfo

USER = "pthormodsen"
BIRTHDAY = datetime.date(2003, 12, 6)
ROOT = Path(__file__).resolve().parent.parent

# Must match RAMP in ascii_art.py
RAMP = ".'`-:;~=+*xo%#&@"

WIDTH = 60  # characters per info line
ASCII_FONT, ASCII_LINE = 11, 13.75
INFO_FONT, INFO_LINE = 16, 20
PAD = 30
INFO_X = 430

THEMES = {
    "dark": {"bg": "#161b22", "text": "#c9d1d9", "ascii": "#c9d1d9", "key": "#ffa657",
             "value": "#a5d6ff", "cc": "#616e7f", "add": "#3fb950", "del": "#f85149"},
    "light": {"bg": "#f6f8fa", "text": "#24292f", "ascii": "#24292f", "key": "#953800",
              "value": "#0a3069", "cc": "#c2cfde", "add": "#1a7f37", "del": "#cf222e"},
}


def graphql(query, **variables):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query, "variables": variables}).encode(),
        headers={"Authorization": f"bearer {os.environ['GITHUB_TOKEN']}"},
    )
    with urllib.request.urlopen(req) as resp:
        body = json.load(resp)
    if "errors" in body:
        raise RuntimeError(body["errors"])
    return body["data"]


def fetch_stats():
    data = graphql("""
        query($login: String!) {
          user(login: $login) {
            id
            followers { totalCount }
            repositoriesContributedTo(privacy: PUBLIC, includeUserRepositories: false,
                contributionTypes: [COMMIT, PULL_REQUEST, REPOSITORY]) { totalCount }
            repositories(first: 100, privacy: PUBLIC,
                ownerAffiliations: [OWNER, COLLABORATOR, ORGANIZATION_MEMBER]) {
              nodes { name owner { login } stargazerCount }
            }
          }
        }""", login=USER)["user"]

    repos = data["repositories"]["nodes"]
    stats = {
        "repos": sum(r["owner"]["login"] == USER for r in repos),
        "contributed": data["repositoriesContributedTo"]["totalCount"],
        "stars": sum(r["stargazerCount"] for r in repos if r["owner"]["login"] == USER),
        "followers": data["followers"]["totalCount"],
        "commits": 0, "additions": 0, "deletions": 0,
    }
    for repo in repos:
        commits, additions, deletions = repo_contributions(repo["owner"]["login"], repo["name"], data["id"])
        stats["commits"] += commits
        stats["additions"] += additions
        stats["deletions"] += deletions
    return stats


def repo_contributions(owner, name, author_id):
    """Count commits, additions and deletions by the user on the default branch."""
    commits = additions = deletions = 0
    cursor = None
    while True:
        repo = graphql("""
            query($owner: String!, $name: String!, $author: ID!, $cursor: String) {
              repository(owner: $owner, name: $name) {
                defaultBranchRef { target { ... on Commit {
                  history(first: 100, after: $cursor, author: { id: $author }) {
                    pageInfo { hasNextPage endCursor }
                    nodes { additions deletions }
                  }
                } } }
              }
            }""", owner=owner, name=name, author=author_id, cursor=cursor)["repository"]
        if not repo["defaultBranchRef"]:  # empty repository
            return commits, additions, deletions
        history = repo["defaultBranchRef"]["target"]["history"]
        commits += len(history["nodes"])
        additions += sum(c["additions"] for c in history["nodes"])
        deletions += sum(c["deletions"] for c in history["nodes"])
        if not history["pageInfo"]["hasNextPage"]:
            return commits, additions, deletions
        cursor = history["pageInfo"]["endCursor"]


def uptime(today):
    years = today.year - BIRTHDAY.year
    months = today.month - BIRTHDAY.month
    days = today.day - BIRTHDAY.day
    if days < 0:
        months -= 1
        last_month = today.replace(day=1) - datetime.timedelta(days=1)
        days += max(last_month.day, BIRTHDAY.day)
    if months < 0:
        years -= 1
        months += 12

    def plural(n, unit):
        return f"{n} {unit}{'' if n == 1 else 's'}"

    text = f"{plural(years, 'year')}, {plural(months, 'month')}, {plural(days, 'day')}"
    if (today.month, today.day) == (BIRTHDAY.month, BIRTHDAY.day):
        text += " 🎂"
    return text


# A line is a list of (text, css class) segments.

def kv(key, value):
    *groups, last = key.split(".")
    segments = [(". ", "cc")]
    for group in groups:
        segments += [(group, "key"), (".", "text")]
    segments += [(last, "key"), (":", "text")]
    return fill(segments, [(value, "value")], WIDTH)


def fill(left, right, width):
    """Join two segment lists with a dot leader so the line is `width` long."""
    used = sum(len(t) for t, _ in left + right)
    dots = max(width - used - 2, 1)
    return left + [(" " + "." * dots + " ", "cc")] + right


def rule(title, prefix="- "):
    segments = [(prefix, "cc"), (title, "text"), (" ", "text")]
    used = sum(len(t) for t, _ in segments)
    return segments + [("—" * (WIDTH - used), "cc")]


def info_lines(stats, today):
    half = 30
    repos = fill([(". ", "cc"), ("Repos", "key"), (":", "text")],
                 [(f"{stats['repos']}", "value"), (" {", "text"), ("Contributed", "key"), (": ", "text"),
                  (f"{stats['contributed']}", "value"), ("}", "text")], half)
    stars = fill([(" | ", "cc"), ("Stars", "key"), (":", "text")],
                 [(f"{stats['stars']:,}", "value")], WIDTH - half)
    commits = fill([(". ", "cc"), ("Commits", "key"), (":", "text")],
                   [(f"{stats['commits']:,}", "value")], half)
    followers = fill([(" | ", "cc"), ("Followers", "key"), (":", "text")],
                     [(f"{stats['followers']:,}", "value")], WIDTH - half)
    loc = fill([(". ", "cc"), ("Lines of Code on GitHub", "key"), (":", "text")],
               [(f"{stats['additions'] - stats['deletions']:,}", "value"), (" ( ", "text"),
                (f"{stats['additions']:,}++", "add"), (", ", "text"),
                (f"{stats['deletions']:,}--", "del"), (" )", "text")], WIDTH)

    return [
    rule("patrik@thormodsen", prefix=""),
    kv("OS", "macOS, Fedora, Windows"),
    kv("Uptime", uptime(today)),
    kv("Host", "Bergen, Norway"),
    kv("Kernel", "Computer Engineering @ HVL"),
    kv("IDE", "IntelliJ IDEA, VS Code"),
    [],
    kv("Languages.Programming", "Java, TypeScript, Python, Haskell"),
    kv("Languages.Web", "JavaScript, HTML, CSS"),
    kv("Languages.Real", "Norwegian, English"),
    [],
    kv("Stack.Backend", "Spring Boot, FastAPI"),
    kv("Stack.Frontend", "React, Vite, Tailwind CSS"),
    kv("Stack.Database", "PostgreSQL, SQL"),
    kv("Stack.Infrastructure", "Docker, Proxmox, Linux"),
    [],
    kv("Hobbies.Software", "Self-hosting, Personal projects"),
    kv("Hobbies.Hardware", "Homelab: luffy, zoro, sanji"),
    kv("Hobbies.Other", "Gym, Padel, Gaming (Soulslikes)"),
    [],
    rule("Contact"),
    kv("Portfolio", "portfolio.patreek.no"),
    kv("LinkedIn", "linkedin.com/in/pthormodsen"),
    [],
    rule("GitHub Stats"),
    repos + stars,
    commits + followers,
    loc,
]


def render(theme, ascii_art, lines):
    colors = THEMES[theme]
    rows = ascii_art.splitlines()
    height = max(len(rows) * ASCII_LINE, len(lines) * INFO_LINE) + 2 * PAD
    width = INFO_X + WIDTH * INFO_FONT * 0.6 + PAD

    if theme == "light":  # dense characters for dark pixels on a light background
        flip = str.maketrans(RAMP, RAMP[::-1])
        rows = [row.translate(flip) for row in rows]

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" font-family="ConsolasFallback,Consolas,Menlo,monospace" '
        f'width="{width:.0f}px" height="{height:.0f}px">',
        "<style>",
        *(f".{name} {{fill: {color};}}" for name, color in colors.items() if name != "bg"),
        "text, tspan {white-space: pre;}",
        "</style>",
        f'<rect width="{width:.0f}px" height="{height:.0f}px" fill="{colors["bg"]}" rx="15"/>',
        f'<text x="{PAD}" y="{PAD}" class="ascii" font-size="{ASCII_FONT}px" xml:space="preserve">',
        *(f'<tspan x="{PAD}" dy="{ASCII_LINE if i else ASCII_FONT}">{escape(row)}</tspan>'
          for i, row in enumerate(rows)),
        "</text>",
        f'<text x="{INFO_X}" y="{PAD}" font-size="{INFO_FONT}px" xml:space="preserve">',
    ]
    for i, line in enumerate(lines):
        dy = INFO_LINE if i else INFO_FONT
        spans = "".join(f'<tspan class="{cls}">{escape(text)}</tspan>' for text, cls in line)
        out.append(f'<tspan x="{INFO_X}" dy="{dy}">{spans or " "}</tspan>')
    out += ["</text>", "</svg>", ""]
    return "\n".join(out)


def main():
    today = datetime.datetime.now(ZoneInfo("Europe/Oslo")).date()
    ascii_art = (ROOT / "ascii.txt").read_text()
    lines = info_lines(fetch_stats(), today)
    for theme in THEMES:
        (ROOT / f"{theme}_mode.svg").write_text(render(theme, ascii_art, lines))


if __name__ == "__main__":
    main()
