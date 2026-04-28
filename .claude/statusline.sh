#!/bin/bash

# Claude JSON 입력 받기

# ---------------------------------------------------------------------------- #
#                                   Claude 정보                                  #
# ---------------------------------------------------------------------------- #
input=$(cat)

# ----------------------------------- model ---------------------------------- #
MODEL=$(echo "$input" | jq -r '.model.display_name // empty' 2>/dev/null)
[ -z "$MODEL" ] && MODEL="-"

DIR=$(echo "$input" | jq -r '.workspace.current_dir // empty' 2>/dev/null)

RAW_PCT=$(echo "$input" | jq -r '.context_window.used_percentage // 0' 2>/dev/null | cut -d. -f1)
RAW_PCT="${RAW_PCT:-0}"
PCT=$(printf "%3d" "$RAW_PCT")
# ------------------------------------ dir ----------------------------------- #
REPO=$(basename "$DIR")
[ -z "$REPO" ] && REPO="-"
# ------------------------------------ git ----------------------------------- #
BRANCH="----------"
GIT_STATUS="-"

if git -C "$DIR" rev-parse --git-dir > /dev/null 2>&1; then

    BRANCH_RAW=$(git -C "$DIR" branch --show-current 2>/dev/null)

    # branch 10칸 고정 (왼쪽 정렬)
    BRANCH=$(printf "%-10.10s" "$BRANCH_RAW")

    STAGED=$(git -C "$DIR" diff --cached --numstat 2>/dev/null | wc -l | tr -d ' ')
    MODIFIED=$(git -C "$DIR" diff --numstat 2>/dev/null | wc -l | tr -d ' ')
    UNTRACKED=$(git -C "$DIR" ls-files --others --exclude-standard 2>/dev/null | wc -l | tr -d ' ')

    GIT_STATUS=""

    [ "$STAGED" -gt 0 ] && GIT_STATUS="${GIT_STATUS}+${STAGED}"
    [ "$MODIFIED" -gt 0 ] && GIT_STATUS="${GIT_STATUS}~${MODIFIED}"
    [ "$UNTRACKED" -gt 0 ] && GIT_STATUS="${GIT_STATUS}?${UNTRACKED}"

    [ -z "$GIT_STATUS" ] && GIT_STATUS="✓"
fi

# -----------------------------
# Python / uv environment
# -----------------------------
VENV="Glob"

# uv project (.venv 우선)
if [ -d "$DIR/.venv" ]; then
    VENV=".venv"

elif [ -n "$VIRTUAL_ENV" ]; then
    VENV=$(basename "$VIRTUAL_ENV")

fi

# -----------------------------
# 시간
# -----------------------------
TIME=$(date +"%H:%M")

# -----------------------------
# 출력
# -----------------------------
echo "[$MODEL] $REPO@$BRANCH | $VENV | ${PCT}% context | $GIT_STATUS | $TIME"