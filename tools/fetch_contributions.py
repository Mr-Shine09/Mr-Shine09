#!/usr/bin/env python3
"""fetch_contributions.py -- pulls the real contribution calendar and emits
the JSON that build_tracker.py consumes. Writes to stdout.

Needs a token in $GH_TOKEN with the read:user scope. The default
GITHUB_TOKEN that Actions injects does NOT have access to
contributionsCollection, so this must be a PAT stored as a repo secret.
"""
import json, os, sys
from datetime import date, timedelta
from urllib import request

USER = os.environ.get('GH_USER', 'Mr-Shine09')
TOKEN = os.environ.get('GH_TOKEN')

LEVELS = {
    'NONE': 0,
    'FIRST_QUARTILE': 1,
    'SECOND_QUARTILE': 2,
    'THIRD_QUARTILE': 3,
    'FOURTH_QUARTILE': 4,
}

QUERY = '''
query($user: String!, $from: DateTime!) {
  user(login: $user) {
    contributionsCollection(from: $from) {
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays { date contributionCount contributionLevel }
        }
      }
    }
  }
}'''


def fetch():
    if not TOKEN:
        sys.exit('GH_TOKEN is not set (needs a PAT with read:user)')
    frm = (date.today() - timedelta(days=364)).isoformat() + 'T00:00:00Z'
    payload = json.dumps({'query': QUERY,
                          'variables': {'user': USER, 'from': frm}}).encode()
    req = request.Request(
        'https://api.github.com/graphql', data=payload,
        headers={'Authorization': f'bearer {TOKEN}',
                 'Content-Type': 'application/json',
                 'User-Agent': f'{USER}-tracker'})
    with request.urlopen(req, timeout=30) as r:
        body = json.load(r)
    if 'errors' in body:
        sys.exit(f'GraphQL error: {body["errors"]}')
    return body['data']['user']['contributionsCollection']['contributionCalendar']


def flatten(cal):
    days = []
    for wk in cal['weeks']:
        for d in wk['contributionDays']:
            days.append((date.fromisoformat(d['date']),
                         d['contributionCount'],
                         LEVELS.get(d['contributionLevel'], 0)))
    days.sort(key=lambda t: t[0])
    return [d for d in days if d[0] <= date.today()]


def streaks(days):
    """Current streak counts back from today, or from yesterday if today is
    still empty -- a day in progress shouldn't read as a broken streak."""
    counts = {d: c for d, c, _ in days}
    longest = run = 0
    for _, c, _ in days:
        run = run + 1 if c > 0 else 0
        longest = max(longest, run)

    today = date.today()
    cur = 0
    start = today if counts.get(today, 0) > 0 else today - timedelta(days=1)
    d = start
    while counts.get(d, 0) > 0:
        cur += 1
        d -= timedelta(days=1)
    return cur, longest


def grid(days, weeks=12):
    """Column-major: 12 columns of 7, oldest column first, Sunday at top."""
    recent = days[-(weeks * 7):]
    # pad the front so the first column starts on a Sunday boundary
    pad = (7 - len(recent) % 7) % 7
    lvls = [0] * pad + [l for _, _, l in recent]
    return [lvls[i * 7:(i + 1) * 7] for i in range(weeks)]


if __name__ == '__main__':
    cal = fetch()
    days = flatten(cal)
    cur, longest = streaks(days)
    json.dump({
        'user': USER,
        'current_streak': cur,
        'longest_streak': longest,
        'this_year': cal['totalContributions'],
        'weeks': grid(days),
    }, sys.stdout)
