import glob
import os
import time


class FileUtils(object):

    def __init__(self):

        repo_dir   = os.getcwd()
        data_dir   = os.path.join(repo_dir, "app/data")
        static_dir = os.path.join(repo_dir, "app/static")

        self.temp_dir      = os.path.join(data_dir,   "temp")
        self.mongodb_dir   = os.path.join(data_dir,   "mongodb")

        if not os.path.isdir(data_dir):
            os.mkdir(data_dir)

        for sub_dir_name, sub_dir in vars(self).items():
            if not os.path.isdir(sub_dir):
                os.mkdir(sub_dir)
                print("[INFO] mkdir [%s] => %s" % (sub_dir_name, sub_dir))

    def get_path(self, file_dir, file_name):
        file_path = "%s/%s" % (vars(self)[file_dir], file_name)
        return file_path

    def clean_dir(self, file_dir, max_seconds=300):
        file_dir = vars(self)[file_dir]
        for file_path in glob.glob("%s/*" % file_dir):
            if time.time() - os.path.getmtime(file_path) > max_seconds:
                os.remove(file_path)
                print("[INFO] remove file => %s" % file_path)
        return


file_utils = FileUtils()


if __name__ == "__main__":
    """
python -m utils.utils_file
    """

    file_utils.clean_dir(file_dir="temp_dir", max_seconds=300)
