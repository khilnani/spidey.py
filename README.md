# spidey.py

> Web spiders are usually disliked by websites, but useful for recursive API/page downloads for offline analysis.

## Installation

> Pypi Location: https://pypi.python.org/pypi/spidey.py

- Using Pypi - `pip install spidey`

## Usage

> Run `spidey` for Detailed help.

- `spidey --dir NEW_DIR --filter DOMAIN --url URL [--base BASE_URL]`
- `spidey --dir NEW_DIR --filter DOMAIN --url URL --max MAX_DOWNLOADS`
- Example - `spidey --dir test --filter 'www.google.com' --url 'https://www.google.com/' --max 20`

### More Examples

```
spidey \
	-d test \
	-f 'www.google.com' \
	-u 'https://www.google.com/' \
    -b 'https://www.google.com/' \
	-hh '{"Accept" : "application/json"}' \
	-n 2 \
    -m 10 \
    -s 5
```
```
spidey \
	--dir test \
	--filter 'www.google.com' \
	--url 'https://www.google.com/'' \ \
    --base 'https://www.google.com/
	--headers '{"Accept" : "application/json"}' \
	--depth 2 \
    --max 10 \
    --sleep 5

```
