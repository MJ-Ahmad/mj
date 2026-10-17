# QuranerFariwala — website

## Automatic "Last updated" stamp
- `js/site-meta.js` holds `QF_LAST_UPDATED` (UTC).
- The `pre-commit` hook sets it to the current time whenever site content is committed.
- Docs, scripts, hooks and deploy files do not change it.

## One-time setup (every clone)
    sh scripts/setup-hooks.sh

## Deploy on push -  (server)
1. Create a bare repository on the server:
       sudo git init --bare /srv/git/qf.git
2. Install the deploy hook:
       sudo cp deploy/post-receive /srv/git/qf.git/hooks/post-receive
       sudo chmod +x /srv/git/qf.git/hooks/post-receive
3. Set the web folder if it is not the default `/var/www/html/qf`:
       sudo sh -c 'echo "export QF_WEB_DIR=/var/www/html/qf" >> /etc/environment'
   (or edit the defaults at the top of the hook)
4. Make sure the user who pushes can write to the web folder.
5. On your computer:
       git remote add prod user@your-server:/srv/git/qf.git
       git push prod main

Every `git push prod main` deploys the new content and removes deleted files.
