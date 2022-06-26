from pathlib import Path
from os import path
from sys import exit

# Custom
from log import Log

class Archive():
    def __init__(self) -> None:
        self.log = Log()

    def sort_files(self, params):
        def search_result(src_path, search, result):
            result_tmp = []
            for txt_path in Path(src_path).glob(f"*{search}*.log"):
                txt_path = path.basename(txt_path)
                result_tmp.append(txt_path)

            if(len(result_tmp) != 0):
                result.append(result_tmp)

            return result
        
        def check_result_empty(result):
            if(len(result) == 0):
                print("Nie ma nic do archiwizacji")
                self.log.warning("No one files to archive")
                exit()

        src_path = params["source_path_arch"]
        iis_log = params["log_name_format_year_6char"]
        year = params["archive_year"]
        month = params["archive_month"]
        day_separate = params["day_separate"]

        if(iis_log == True):
            year = year[2:]

        search = f"{year}{month}"
        result = []
        self.log.info("Looking for candidates for transfer to archive")
        if(day_separate == True):
            for day in range(1, 32, 1):
                search = f"{year}{month}"
                day = str(day)

                if(len(day) == 1):
                    day = '0' + day
                    search = search + day

                else:
                    search = search + day

                result_final = search_result(src_path, search, result)
            check_result_empty(result_final)

        elif(day_separate == False):
            result_final = search_result(src_path, search, result)
            check_result_empty(result_final)
            result_final = result_final[0]

        return result_final

    def __del__(self) -> None:
        del self.log