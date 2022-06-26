from pathlib import Path
from os import path, listdir, remove, chdir
from shutil import rmtree
from sys import exc_info

# Custom
from log import Log

class SysPath():
    def __init__(self) -> None:
        self.log = Log()

    def check_main_path(self, params):
        src_path = params["source_path_arch"]

        self.log.info(f"Checking source path: {src_path}")
        try:
            listdir(src_path)

        except:
            print(exc_info())
            self.log.exception(exc_info())
            exit()

    def create_new_arch_path(self, params):
        dest_path = params["dest_path_arch"]

        try:
            self.log.info(f"Checking destination path: {dest_path}")
            if(path.isdir(dest_path) == False):
                Path(dest_path).mkdir(parents=True, exist_ok=True)
                self.log.info(f"Created destination path: {dest_path}")

        except:
            print(exc_info())
            self.log.exception(exc_info())
            exit()

    def delete_log_files(self, sort_files, params): #delete_log
        src_path = params["source_path_arch"]
        day_separate = params["day_separate"]

        try:
            self.log.info("Delete log files after finishing archiving")
            chdir(src_path)
            if(day_separate == True):
                for files in sort_files:
                    for file in files:
                        remove(file)

            elif(day_separate == False):
                for file in sort_files:
                    remove(file)

            self.log.info("Delete completed")

        except:
            print(exc_info())
            self.log.exception(exc_info())

    def delete_archives(self, archive_params, ftp_params):
        delete_files = archive_params["delete_files"]
        if(delete_files == True):
            try:
                month = int(archive_params["archive_month"])
                year = int(archive_params["archive_year"])
                del_archives = ftp_params["del_archives"]
                month_to_del_zip = ftp_params["month_to_del_zip"]
                dest_path = ftp_params["org_dest_path_arch"]

                if(del_archives == True):
                    chdir(dest_path)
                    if(month_to_del_zip > 0):
                        tmp_month = month - month_to_del_zip
                        if(tmp_month < 1):
                            tmp_month = 12 + tmp_month
                            year -= 1

                        if(len(str(tmp_month)) == 1):
                            tmp_month = str(tmp_month)
                            tmp_month = f"0{tmp_month}"

                        del_path = f"{dest_path}\\{year}{tmp_month}"

                    elif(month_to_del_zip == 0):
                        del_path = f"{dest_path}\\{year}{month}"

                    rmtree(del_path)
                    self.log.info(f"Removing path with archives: {del_path}")
            
            except:
                print(exc_info())
                self.log.exception(exc_info()[:-1])

    def __del__(self) -> None:
        del self.log