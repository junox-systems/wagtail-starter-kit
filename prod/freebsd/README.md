

# init

Ensure `www` has a home:

```
pw usermod www -d /home/www
```

If not:

```
mkdir -p /home/www
chown www:www /home/www
```

set shell for www:

```
pw unlock www
chsh -s /bin/sh www
```

## set up deploy keys 

as root.

```
install -d -m 700 -o www -g www /home/www/.ssh
ssh-keygen -t ed25519 -f /home/www/.ssh/deploy -N ""
cat /home/www/.ssh/deploy.pub
```

Add this key to GitHub:

- Repo → Settings → Deploy keys
- Add key
- ✔ Read access

ssh config for github:

```
cat > /home/www/.ssh/config <<EOF
Host github.com
  IdentityFile /home/www/.ssh/deploy
  IdentitiesOnly yes
  StrictHostKeyChecking accept-new
EOF
```

fix ownership:

```
chown www:www /home/www/.ssh/deploy*
chown www:www /home/www/.ssh/config
chmod 600 /home/www/.ssh/deploy
chmod 644 /home/www/.ssh/deploy.pub
chmod 600 /home/www/.ssh/config
```

### sanity check

```
su - www -c "ssh -T git@github.com"
```

it should return something like:

```
Hi fivehanz/hanz.jsmx.org! You've successfully authenticated, but GitHub does not provide shell access.
```

## clone repo


clone the repo to the `/usr/local/www/wagtail` directory

```
GIT_SSH_COMMAND="ssh -i /home/www/.ssh/deploy -o IdentitiesOnly=yes" \
git clone git@github.com:YOUR_USER/YOUR_REPO.git /usr/local/www/wagtail
```

fix ownerships:

```
chown -R www:www /usr/local/www/wagtail
```

## ssl certs 

i use cloudflare origin certs with 15 year validity

```
install -d -m 755 /usr/local/etc/ssl

chmod 600 /usr/local/etc/ssl/cf-origin.key
chmod 644 /usr/local/etc/ssl/cf-origin.pem
```

# setup pkgs

```
pkg install --yes nginx litestream just python311 uv
```

