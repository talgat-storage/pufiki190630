import os
import shutil


def delete_folder_contents(folder_name):
    for file in os.listdir(folder_name):
        filename = os.path.join(folder_name, file)
        if os.path.isfile(filename):
            os.remove(filename)
        elif os.path.isdir(filename):
            shutil.rmtree(filename)


def copy_folder_contents_to_another_folder(src, dst):
    for file in os.listdir(src):
        filename = os.path.join(src, file)
        dst_filename = os.path.join(dst, file)
        if os.path.isfile(filename):
            shutil.copyfile(filename, dst_filename)
        elif os.path.isdir(filename):
            shutil.copytree(filename, dst_filename)


if __name__ == '__main__':
    DIST_FOLDER_PATH = 'dist/'
    STATIC_FOLDER_PATH = '../static/'

    delete_folder_contents(STATIC_FOLDER_PATH)
    copy_folder_contents_to_another_folder(DIST_FOLDER_PATH, STATIC_FOLDER_PATH)
