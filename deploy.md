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
