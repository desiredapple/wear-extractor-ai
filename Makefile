all:
	parse_wb
	parse_lamoda

parse_wb:
	~/anaconda3/bin/python ./src/parser_wildberries.py

parse_lamoda:
	~/anaconda3/bin/python ./src/parser_lamoda.py

rm:
	rm -rfd data logs
