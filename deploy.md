To Push code to the university server make change to the `./_config.yml` and change the baseurl attribute to `/~kabilan` and url to `https://people.cs.vt.edu` and then run the `deploy.py` file.

I can also use `deploy.rb` ruby file to deploy using the devcontainer bash terminal.

```bash
chmod +x deploy.rb
./deploy.rb
```

## Redirecting the university site instead

If I'd rather point `people.cs.vt.edu/~kabilan` at my main site (`https://kabilanma.github.io/KabilanMA/`) instead of mirroring the full Jekyll build there, use the standalone [`redirect/`](redirect/) folder.

It contains just:

- `index.html` — a page with a meta-refresh + JS redirect to `https://kabilanma.github.io/KabilanMA/`
- `.htaccess` — an Apache rewrite rule that 301-redirects any path under `~kabilan` to the same URL

This folder is excluded from the Jekyll build (see `exclude:` in `_config.yml`), so it is never picked up by `bundle exec jekyll build` or the normal `deploy.py`/`deploy.rb` scripts. To deploy it, rsync it directly instead of the `_site/` build output:

```bash
rsync -avz --delete redirect/ kabilan@ap1.cs.vt.edu:/web/people/kabilan/
```

Note: this **replaces** everything currently at `/web/people/kabilan/` with just the redirect files (`--delete` wipes the remote directory to match). To go back to the full site later, just re-run `./deploy.rb` (or `deploy.py`) as before — that rebuilds and re-pushes the full `_site/` output.

## Local dev server (dev container)

The dev container runs `bin/entry_point.sh` every time VS Code attaches. It starts `jekyll serve` on port 8080 and restarts it whenever `_config.yml` changes. Each re-attach starts another copy of the script, so old copies pile up and can fight over restarts. Jekyll also only reads `_config.yml` at startup, so config changes need a restart.

### Restart the server

Quickest, from a VS Code terminal inside the container:

```bash
cd /workspaces/KabilanMA
pkill -f entry_point.sh; pkill -f inotifywait; pkill -f "jekyll serve"  # stop every old copy
./bin/entry_point.sh                                                      # start one clean server
```

Keep that terminal open; the site is ready at `http://localhost:8080` once it prints `Server running`. Hard-refresh the browser (Ctrl+Shift+R) afterwards.

If the build fails with `Permission denied` under `.jekyll-cache`, some cache files are owned by root. The cache is safe to delete:

```bash
sudo rm -rf .jekyll-cache
```

### Restart or rebuild the container

From the VS Code Command Palette (Ctrl+Shift+P):

- **Dev Containers: Reopen in Container** restarts the existing container (keeps installed packages).
- **Dev Containers: Rebuild Container** recreates it from `.devcontainer/` (use after changing the Dockerfile or `devcontainer.json`, or if things are badly broken).
- **Dev Containers: Rebuild Without Cache and Reopen in Container** does a full clean rebuild, re-downloading everything.

### Delete old containers

Run these on the host machine (not inside the container), after closing the VS Code window that uses it:

```bash
# list containers created for this project
docker ps -a --filter "label=devcontainer.local_folder"

# remove one (use the ID or name from the list above; -f stops it first if running)
docker rm -f <container-id>

# optionally free disk space from unused images and build cache
docker image prune
docker builder prune
```

The next time the folder is opened in VS Code, choose **Reopen in Container** and a fresh container is built.
