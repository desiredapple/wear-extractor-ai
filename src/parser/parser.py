from .parser_wildberries import WildberriesParser


class Parser():
    def __init__(self):
        pass
    def run(self):
        wb_parser = WildberriesParser()
        wb_parser.parse_all()