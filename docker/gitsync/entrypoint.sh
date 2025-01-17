#!/bin/sh


# should we do our start up things
if [ ! -d "/root/.ssh/known_hosts" ]; then
  if [ -n "$GIT_SYNC_FORCE_ACCEPT_SSH_HOST_KEY" ]; then
    ssh-keyscan -p $GIT_SYNC_FORCE_ACCEPT_SSH_PORT_KEY $GIT_SYNC_FORCE_ACCEPT_SSH_HOST_KEY >> ~/.ssh/known_hosts
  fi
fi

# should we do our start up things
if [ ! -d "/git/.git" ]; then
  # perform a sparse checkout
  cd /git
  git init
  git remote add origin $GIT_SYNC_REPO
  git fetch
  git reset --hard origin/${GIT_SYNC_BRANCH}
  run-parts /etc/after/pull
fi

/etc/periodic/15min/update_repo

exec "$@"
