#!/bin/sh
git filter-branch -f --env-filter '
    GIT_AUTHOR_NAME="Hossein Zareinejad"
    GIT_AUTHOR_EMAIL="zarenejad83@gmail.com"
    GIT_COMMITTER_NAME="Hossein Zareinejad"
    GIT_COMMITTER_EMAIL="zarenejad83@gmail.com"
' HEAD
