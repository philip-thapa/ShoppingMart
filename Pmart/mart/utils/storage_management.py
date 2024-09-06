from django.core.files.storage import FileSystemStorage
import os


class CustomStorage(FileSystemStorage):
    def __init__(self, location=None):
        self.location = os.path.realpath(location)
        FileSystemStorage.__init__(self, self.location)

    def save_file(self, file_name, data):
        if self.file_exists(file_name):
            self.delete(file_name)
        content = self.save(file_name, data)
        return content

    def save_file_without_replacing(self, file_name, data):
        content = self.save(file_name, data)
        return content

    def file_exists(self, file_name):
        return self.exists(file_name)
