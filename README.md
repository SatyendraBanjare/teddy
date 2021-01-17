# Teddy

Small cli to manage projects & notes.

```sh
Usage: teddy [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  initrepos  initialize with the WIP repos in PROJECTS.md
  publish    publish to index.md of notes repo
  sync       sync the NOTES repo
  todo       count To-Do items in README.md of WIP projects
```

# config
- edit `PROJECTS.md` with the repository names under `WIP`, `Hold` & `Backlog`.
- edit `notes_repo_path` in teddy.py to change the `notes` repository location.
- edit `projects_path` in teddy.py to change the directory location where all projects will be stored.
- edit `git_ssh_prefix` according to your github username & preference.

# installation
Easily install using `pip install -e /path/to/teddy` to use teddy from anywhere.