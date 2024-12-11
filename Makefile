pack:
	zip -r game.zip assets/* src/*.py Makefile README.md requirements.txt
run:
	python3 src/main.py