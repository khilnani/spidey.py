# badspider.py

> Terrible web spider, but useful for recursive API downloads.

## Installation

- Using Pypi - `pip install badspider`

## Usage

> Run `badspider` for Detailed help.

- `badspider --dir NEW_DIR --filter DOMAIN --url URL`
- `badspider --dir NEW_DIR --filter DOMAIN --url URL --max MAX_DOWNLOADS`
- Example - `badspider --dir test --filter 'www.google.com' --url 'https://www.google.com/' --max 20`

### More Examples

```
badspider \
	-d test \
	-f 'www.google.com' \
	-u 'https://www.google.com/' \
	-hh '{"Accept" : "application/json"}' \
	-n 2 \
    -m 10
```
```
badspider \
	--dir test \
	--filter 'www.google.com' \
	--url 'https://www.google.com/' \
	--headers '{"Accept" : "application/json"}' \
	--depth 2 \
    --max 10
```
