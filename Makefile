install:
	pip3 install poetry
	poetry install

update:
	poetry update

run:
	poetry run python anp-city-extract/extract_anp.py

