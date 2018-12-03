echo 'preinstall script called'

# git init
chmod +x scripts/pre-commit
chmod +x scripts/commit-msg
ln -s -f ../../scripts/pre-commit .git/hooks/pre-commit
ln -s -f ../../scripts/commit-msg .git/hooks/commit-msg

# npm start convert WOFF