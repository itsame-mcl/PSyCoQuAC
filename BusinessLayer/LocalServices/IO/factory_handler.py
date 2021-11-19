from BusinessLayer.LocalServices.IO.csv_handler import CSVHandler


class HandlerFactory:
    @staticmethod
    def get_handler_from_ext(ext):
        if ext == ".csv":
            return CSVHandler()
