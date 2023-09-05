"""
Tool for synchronization of Two directories
"""

import  argparse
from    datetime import datetime
import  hashlib
import  logging
import  os
import  shutil
import  warnings

class FolderSynchronization:
    """
    Folder sync: TODO Documentation
    """
    def __init__(
        self,
        source          : str = None,
        destination     : str = None,
        log_path        : str = None,
    ) -> None:
        """
        TODO: Documentation
        """
        self.src        = source
        self.dest       = destination
        self.log_path   = log_path

        logging.basicConfig(
            filename    = self.log_path,
            filemode    = 'a',
            level       = logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )


        if not os.path.isdir(self.src):
            logging.error(f"Folder not found at: {self.src}")
            raise ValueError(f"Folder not found at: {self.src}")

        if not os.path.isdir(self.dest):
            logging.warning(f"Folder doesn't exist at {self.dest}.\n "
                            "Enter Y to create a folder at destination")
            warnings.warn(f"Folder doesn't exist at {self.dest}.\n "
                            "Enter Y to create a folder at destination")

            text = input()
            if text == "Y":
                os.makedirs(self.dest)
                print(f"Creating directory at: {self.dest}")
            else:
                raise ValueError(f"Create a folder at {self.dest}")


    def synchronize_folders(self):
        """Wrapper function that synchornizes the source and destination
        folders"""
        logging.info(f"Started Logging for {self.src} \n {self.dest}")
        self._synchronize_folders(self.src, self.dest)
        logging.info(f"Finished folder sync {self.src} \n {self.dest}")


    def _synchronize_folders(self, src : str, dest : str) -> None:
        """TODO"""
        # Remove all files / directories in the replica folder that aren't in source
        for object_name in os.listdir(dest):
            src_path = os.path.join(src, object_name)
            dest_path = os.path.join(dest, object_name)
            if not os.path.exists(src_path) and os.path.exists(dest_path):
                if os.path.isfile(dest_path):
                    try:
                        os.remove(dest_path)
                        print(f"Removed file in destination {dest_path}")
                        logging.info(f"Removed file in destination {dest_path}")
                    except OSError:
                        print(f"Couldn't remove file at {dest_path}")
                        logging.error(f"Couldn't remove file at {dest_path}")
                elif os.path.isdir(dest_path):
                    try:
                        shutil.rmtree(dest_path)
                        print(f"Removed folder in destination {dest_path}")
                        logging.info(
                            f"Removed folder in destination {dest_path}"
                        )
                    except OSError:
                        print(f"Couldn't remove folder file at {dest_path}")
                        logging.error(
                            f"Removed folder in destination {dest_path}"
                        )


        # Working on files / directories
        for root, directories, files in os.walk(src):
            for file_name in files:
                src_path = os.path.join(src, file_name)
                dst_path = os.path.join(dest, file_name)
                if not os.path.isfile(dst_path):
                    # File does not exist in the destination folder
                    shutil.copy(src_path, dst_path)
                    print(f"Copied {src_path} to destination folder")
                    logging.info(f"Copied {src_path} to destination folder")
                elif not self.compare_files(src_path, dst_path):
                    # file exists in destination but is modified in source folder
                    shutil.copy(src_path, dst_path)
                    print(f"Copied {src_path} to destination folder")
                    logging.info(f"Copied {src_path} to destination folder")
                else:
                    pass # File already exists in the destination folder

            for dir_name in directories:
                src_path = os.path.join(src, dir_name)
                dst_path = os.path.join(dest, dir_name)

                if not os.path.isdir(dst_path):
                    os.mkdir(dst_path)
                    print(f"Created Directory in destination folder: {dst_path}")
                    logging.info(
                        f"Created Directory in destination folder: {dst_path}"
                    )

                # NOTE Recursively synchronizing the directories.
                self._synchronize_folders(src_path, dst_path)

    def compare_files(self, file1 : str = None, file2 : str = None) -> bool:
        """Compares is two files are same based on matching md5sum"""
        return self.file_md5sum(file1) == self.file_md5sum(file2)


    def file_md5sum(self, path : str) -> str:
        """Returns the md5sum of a file with a given path (str)"""
        md5hash = hashlib.md5()
        with open(path, "rb") as fobject:
            # Read 4096 bytes at a time in case the file doesn't fit in memory
            for spra in iter(lambda: fobject.read(4096), b""):
                md5hash.update(spra)

        return md5hash.hexdigest()


    def naive_copy(self) -> None:
        """
        Naive copy
        NOTE: This is a brute force method. It is not recommended and it is not
        optimized. Deletes and replaces the contents of destination folder
        with source folder. Used only for testing
        """
        for path in os.listdir(self.dest):
            os.remove(os.path.join(self.dest, path))
        shutil.copy(self.src, self.dest)


    def get_current_time(self) -> str:
        """
        Return the time in string
        """
        return str(datetime.now())