from zipfile import ZipFile, ZIP_DEFLATED
from sys import exc_info
from os import chdir, listdir

# Custom
from log import Log

class Zipping():
    def __init__(self) -> None:
        self.log = Log()

    def zip(self, sort_file, params):
        def zipping(filename, files, src_path, separate):
            if(separate == True):
                for file in files:
                    if(file[-13] != "_Messages.log"):
                        file_of_day = file[-6:-4]
                        filename = f"{filename}{file_of_day}"
                        break

            with ZipFile(filename, mode="w", compression=ZIP_DEFLATED, compresslevel=9) as archive:
                for file in files:
                    print(f"{src_path}\\{file}")
                    archive.write(file)
                archive.close()
            self.log.info(f"Zipping {filename} is complete")

        src_path = params["source_path_arch"]
        dest_path = params["dest_path_arch"]
        separate = params["day_separate"]
        end_file_name = params["end_file_name"]
        tmp_day = 1

        chdir(src_path)

        if(separate == True):
            for files in sort_file:
                zipping(f"{dest_path}\\{end_file_name}.zip", files, src_path)

        elif(separate == False):
            zipping(f"{dest_path}\\{end_file_name}.zip", sort_file, src_path)

    def test_zip(self, params):
        dest_path = params["dest_path_arch"]
        chdir(dest_path)

        self.log.info(f"Getting the name of the files in directory")

        files = listdir(dest_path)
        result_test = None
        try:
            self.log.info("Testing archives")
            for file in files:
                archive = ZipFile(file)
                if(archive.testzip() == None):
                    print(f"Correct file: {file}")
                    self.log.info(f"{file} - CRC OK")
                    result_test = False            

        except:
            print(f"Error file: {file}")
            self.log.error(f"{file} - CRC is incorrect")
            self.log.error("Stop script")
            result_test = True
            archive.close()
            print(exc_info())
            self.log.exception(exc_info()[:-1])
            # raise

        finally: 
            return result_test

    def __del__(self) -> None:
        del self.log