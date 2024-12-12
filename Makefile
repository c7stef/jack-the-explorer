install:
	@python3 -m venv .venv
	. .venv/bin/activate ; python3 -m pip install -r requirements.txt
pack:
	zip -r game.zip assets/* src/*.py Makefile README.md requirements.txt
run:
	. .venv/bin/activate ; python3 src/main.py
