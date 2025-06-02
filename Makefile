all:
	parse_wb
	parse_lamoda

parse_wb:
	/home/omniscope/anaconda3/bin/python ./src/parser_wildberries.py

parse_lamoda:
	/home/omniscope/anaconda3/bin/python ./src/parser_lamoda.py

rm:
	rm -rfd data log
