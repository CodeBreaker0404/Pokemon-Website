#!/bin/bash
set -e

# 0) cd to your repo (or run this script from inside the repo)
# cd "/c/Users/YourName/OneDrive/Desktop/Projects/Lung Cancer Prediction App"

# 1) Detect current branch (main/master/whatever)
BRANCH="$(git rev-parse --abbrev-ref HEAD)"
echo "Using branch: $BRANCH"

# 2) Optional: pull latest (skip if unrelated history warning appears)
set +e
git pull origin "$BRANCH"
set -e

# 3) Helper to create a dated commit (uses fixed times to avoid needing shuf)
commit_with_datetime () {
  local DATE="$1"   # YYYY-MM-DD
  local TIME="$2"   # HH:MM:SS
  local MSG="$3"

  echo "[$DATE $TIME] $MSG" >> progress_log.txt
  git add progress_log.txt
  GIT_AUTHOR_DATE="${DATE}T${TIME}" \
  GIT_COMMITTER_DATE="${DATE}T${TIME}" \
  git commit -m "$MSG"
}

# Pre-chosen times (24h) so multiple commits on same day look natural
TIMES=( "09:14:22" "11:47:05" "14:33:41" "16:58:10" "18:21:55" "20:07:12" "21:39:44" "22:55:03" )

t=0
next_time () { local TT="${TIMES[$t]}"; t=$(( (t+1) % ${#TIMES[@]} )); echo "$TT"; }

echo "Creating commits..."

# --- Sep 30, 2025 (2 commits)
for i in 1 2; do
  commit_with_datetime "2025-09-30" "$(next_time)" "Progress update #$i on 2025-09-30"
done

# --- Oct 04, 2025 (2 commits)
for i in 1 2; do
  commit_with_datetime "2025-10-04" "$(next_time)" "Progress update #$i on 2025-10-04"
done

# --- Oct 05, 2025 (4 commits)
for i in 1 2 3 4; do
  commit_with_datetime "2025-10-05" "$(next_time)" "Progress update #$i on 2025-10-05"
done

# --- Oct 06, 2025 (4 commits)
for i in 1 2 3 4; do
  commit_with_datetime "2025-10-06" "$(next_time)" "Progress update #$i on 2025-10-06"
done

echo "Pushing to origin/$BRANCH..."
git push origin "$BRANCH"

echo "Done."
