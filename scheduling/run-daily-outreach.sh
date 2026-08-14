#!/bin/bash
#
# Runs the daily-outreach skill headlessly, invoked by launchd.
#
# launchd gives a job almost no environment, so everything it needs is set
# explicitly here. Anything assumed from an interactive shell will be missing.

set -uo pipefail

REPO="/Users/maxfriedlander/code/Networking/Project_Contact"
cd "$REPO" || exit 1

mkdir -p scheduling/logs
echo "=== $(date '+%Y-%m-%d %H:%M:%S %Z') starting daily outreach ==="

# launchd's PATH is /usr/bin:/bin:/usr/sbin:/sbin, which has neither claude nor
# the homebrew tools.
export PATH="/opt/homebrew/bin:/usr/local/bin:$HOME/.local/bin:$PATH"

# Turn OMC off for this job only.
#
# OMC's autopilot detection fires on the prompt below and creates a fresh
# autopilot-state.json on every run, which the stop hook then has to clean up.
# Three test runs produced three state files and three cleanups, none of which
# had anything to do with outreach. Its MCP state tools are also gated behind a
# permission prompt that an unattended session cannot answer, so a run ends up
# editing the state file by hand instead.
#
# This is scoped to this script. Interactive sessions in this project, and every
# other project, keep OMC exactly as it was.
export DISABLE_OMC=1

# Each invocation below is a fresh Claude session, so this applies to it even
# though it cannot change an already-running one. The default 200 was exhausted
# mid-task by a single research pass, which left that person's checks incomplete.
export CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION=600

# Wait for the network before doing anything.
#
# launchd fires a missed calendar job the instant the machine wakes, which is
# usually seconds before Wi-Fi reassociates. On 2026-08-14 the job woke at
# 10:19, reported the Outlook session dead when it was fine, then failed with
# ENOTFOUND against the API and burned two hours before exiting 1. Both were DNS
# failures, not real ones.
wait_for_network() {
    local waited=0
    local limit=600          # ten minutes is generous for a laptop waking up
    until ping -c1 -W2 1.1.1.1 >/dev/null 2>&1 && \
          ping -c1 -W2 api.anthropic.com >/dev/null 2>&1; do
        if [ "$waited" -ge "$limit" ]; then
            echo "FATAL: no network after ${limit}s. Not starting; the next wake will retry."
            return 1
        fi
        [ $((waited % 60)) -eq 0 ] && echo "  waiting for network... (${waited}s)"
        sleep 10
        waited=$((waited + 10))
    done
    echo "Network up after ${waited}s."
    return 0
}

wait_for_network || exit 1

# Secrets. A cron-style run never sources the shell profile.
if [ -f credentials/.env ]; then
    set -a
    . ./credentials/.env
    set +a
else
    echo "WARNING: credentials/.env missing. Email finding will be unavailable."
fi

if [ ! -f credentials/google_sheets_key.json ]; then
    echo "FATAL: credentials/google_sheets_key.json missing. Cannot reach the sheet."
    exit 1
fi

if ! command -v claude >/dev/null 2>&1; then
    echo "FATAL: claude not on PATH. Checked: $PATH"
    exit 1
fi

# Is the Outlook session still good? Not fatal: the skill writes drafts to the
# repo either way, and a dead session should not cost a morning's research.
if ./.venv/bin/python outlook_drafter.py --check >/dev/null 2>&1; then
    echo "Outlook session: valid, drafts will be created."
else
    echo "Outlook session: DEAD. Drafts go to daily/ only."
    echo "  Fix with: ./.venv/bin/python outlook_drafter.py --login"
fi

claude -p "Run the daily-outreach skill for today's batch. Read BRIEF.md first for who and how many, then follow the skill end to end. This is an unattended run, so there is nobody to ask: follow the brief as written. Report what was found, who was dropped and why, and whether the Outlook drafts were created." \
    --permission-mode acceptEdits

status=$?
echo "=== $(date '+%Y-%m-%d %H:%M:%S %Z') finished, exit $status ==="
exit $status
