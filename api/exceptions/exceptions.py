from werkzeug.exceptions import BadRequest


class NotPossibleReadSales(BadRequest):
    def __init__(self):
        super().__init__()
        self.message = "It's not possible to read the sales from your file. Check if the file content is correct."
        self.title = "Not Possible Read Sales"
        self.status = 400


class FileWrongFormat(BadRequest):
    def __init__(self):
        super().__init__()
        self.message = "The sent file should be a .txt."
        self.title = "File Wrong Format"
        self.status = 400
