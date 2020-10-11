install:
	pip3 install poetry
	poetry install

update:
	poetry update

run:
	poetry run python extract_anp.py

