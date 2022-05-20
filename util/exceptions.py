class FilepathNotProvidedError(Exception):
    def __init__(self):
        self.message = 'Please provide a filepath after --path argument.'
        super().__init__(self.message)


class FileNotReadable(Exception):
    def __init__(self, filepath):
        self.message = f'Cannot read file: {filepath}'
        super().__init__(self.message)
