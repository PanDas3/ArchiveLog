from pathlib import Path
from os import path, listdir, remove, chdir
from shutil import rmtree
from sys import exc_info
from datetime import datetime
from dateutil.relativedelta import relativedelta

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

    def delete_log_files(self, sort_files, params):

        delete_files = params["delete_files"]

        if(delete_files == True):
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
        del_archives = ftp_params["del_archives"]
        if(del_archives == True):
            try:
                month = int(archive_params["archive_month"])
                year = int(archive_params["archive_year"])
                month_to_del_zip = int(ftp_params["month_to_del_zip"])
                dest_path = ftp_params["org_dest_path_arch"]
                app_name = archive_params["app_name"]
                instance = archive_params["instance_name"]

                chdir(dest_path)

                date = datetime(year, month, 1)
                date = date + relativedelta(months =- month_to_del_zip)
                date = str(date.strftime("%Y%m"))
                del_path = f"{dest_path}\\{date}"

                if(len(listdir(f"{del_path}\\{app_name}")) >= 2):
                    del_path = f"{del_path}\\{app_name}\\{instance}"

                rmtree(del_path)
                self.log.info(f"Removing path with archives: {del_path}")

            except FileNotFoundError:
                print(exc_info()[:-1])
                self.log.exception(exc_info()[:-1])
            
            except:
                print(exc_info())
                self.log.exception(exc_info()[:-1])

    def __del__(self) -> None:
        del self.log