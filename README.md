# recommit

When developing on platforms other than GitHub, trying to show active development and a profile of continued work is difficult.

To fix this, I decided to create a small python-based application to "repost" or "recommit" private contributions on GitHub.

These commits are empty "mocks" of the commits and are not intended to be viewed or compared to the true private contributions.

## Usage

Configure a `.env` file with the necessary variables. Keep them private.

```
GITLAB_API_KEY=
GITLAB_USERNAME=
REPOSITORY_PATH=
TIMEZONE=
```

The GitLab private key must be acquired from their API. You must have permissions to view contributions in the API.

The repository path is a path to a git repository that you want `recommit` to commit the mock contributions to. It will push
to the default upstream origin automatically when done.

Timezone is simply for Git. It is not required and when not set, will default to UTC.
See [here][common-timezones] for common timezones, or [here][all-timezones] for the full list.
You can also try guessing them, and if it's invalid, then the timezones that match closest will be recommended to you.

```bash
pipenv shell  # Load into a virtual environment
pipenv install  # Install dependencies from Pipfile
python ./main.py
```

[common-timezones]: https://gist.github.com/Xevion/4ba5269937864046dd558ff8ffe45013

[all-timezones]: https://gist.github.com/Xevion/18403255a2e52e21b4a7979f79b4ca3d
