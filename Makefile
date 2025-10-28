all: main

main:
	~/anaconda3/bin/python ./src/main.py

parse_wb:
	~/anaconda3/bin/python ./src/parser/parser_wildberries.py

parse_lamoda:
	~/anaconda3/bin/python ./src/parser/parser_lamoda.py

rebuild: clean all

install:
	pip install -r req

clean:
	rm -rfd data logs
