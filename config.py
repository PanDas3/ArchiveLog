from configparser import ConfigParser, MissingSectionHeaderError
from cryptography.fernet import Fernet
from sys import exc_info, exit, path as script_path
from shutil import rmtree
from os import path
from configupdater import ConfigUpdater

# Custom
from log import Log

class Configuration():
    def __init__(self) -> None:
        self.log = Log()

    def read_config(self, config_name):
        def str_to_bool(string):
            if(string == 'false'):
                string = bool(string)
                string = False

            elif(string == 'true'):
                string = bool(string)
                string = True
            
            else:
                string = bool(string)
                string = False

            return string

        try:
            config = ConfigParser()
            config.read(config_name)
            self.log.info("Read config.ini")

            # Read Archive
            self.source_path_arch = config["Archive"]["Source_Path_Arch"]
            self.destination_path_arch = config["Archive"]["Destination_Path_Arch"]
            self.log_name_format_year_6char = config["Archive"]["Log_Name_Format_Year_6Char"].lower()
            self.day_separatley = config["Archive"]["Day_Separately"].lower()
            self.archive_year = config["Archive"]["Archive_Year"]
            self.archive_month = config["Archive"]["Archive_Month"]
            self.app_name = config["Archive"]["Application_Name"]
            self.instance_name = config["Archive"]["Instance_Name"]
            self.prefix_arch_file_name = config["Archive"]["Prefix_Arch_File_Name"]
            self.server_name = config["Archive"]["Server_Name"]
            self.delete_files = config["Archive"]["Delete_files"].lower()
            self.auto_change_month = config["Archive"]["Auto_Change_Month"].lower()

            # Read FTP
            self.move_to_FTP = config["FTP"]["Move_To_FTP"].lower()
            self.del_archives = config["FTP"]["Delete_archives_files"].lower()
            self.month_to_del_zip = int(config["FTP"]["Month_to_del_archives"])
            self.FTP_server_name = config["FTP"]["FTP_Server_Name"]
            self.FTP_port = int(config["FTP"]["FTP_Port"])
            self.FTP_login = config["FTP"]["FTP_Login"]
            self.FTP_pass = config["FTP"]["FTP_Pass"]

            # Change string to bool
            self.log_name_format_year_6char = str_to_bool(self.log_name_format_year_6char)
            self.day_separatley = str_to_bool(self.day_separatley)
            self.delete_files = str_to_bool(self.delete_files)
            self.auto_change_month = str_to_bool(self.auto_change_month)
            self.move_to_FTP = str_to_bool(self.move_to_FTP)
            self.del_archives = str_to_bool(self.del_archives)


        except AttributeError as err:
            self.log.error(f"Config Error: {err}")
        
        except UnicodeDecodeError as err:
            self.log.error(f"Config Error: {err}")

        except MissingSectionHeaderError as err:
            self.log.error(f"Config Error: {err}")
        
        except KeyError as err:
            self.log.error(f"Config Error: {err}")

        except UnboundLocalError as err:
            self.log.error(f"Config Error: {err}")
        
        except:
            print(exc_info())
            self.log.exception(exc_info())
            exit()

    def get_archive_params(self):
        end_file_name = f"{self.prefix_arch_file_name}_{self.server_name}_{self.archive_year}{self.archive_month}"
        new_path = f"{self.archive_year}{self.archive_month}\\{self.app_name}\\{self.instance_name}"
        dest_path = f"{self.destination_path_arch}\\{new_path}"

        return {
                "source_path_arch":self.source_path_arch,
                "dest_path_arch":dest_path,
                "log_name_format_year_6char":self.log_name_format_year_6char,
                "day_separate":self.day_separatley,
                "archive_year":self.archive_year,
                "archive_month":self.archive_month,
                "app_name":self.app_name,
                "instance_name":self.instance_name,
                "end_file_name":end_file_name,
                "auto_change_month":self.auto_change_month,
                "delete_files":self.delete_files,
                "prefix_file_name":self.prefix_arch_file_name
                    }

    def get_FTP_params(self):
        key = "TOP Secret"
        return {
            "move_to_FTP":self.move_to_FTP,
            "FTP_server_name":self.FTP_server_name,
            "FTP_port":self.FTP_port,
            "FTP_login":self.FTP_login,
            "FTP_pass":self.FTP_pass,
            "key":key,
            "org_dest_path_arch":self.destination_path_arch,
            "del_archives":self.del_archives,
            "month_to_del_zip":self.month_to_del_zip
        }
            
    def change_config_to_next_month(self, config_name):
        update_config = ConfigUpdater()
        update_config.read(config_name)
        year = int(self.archive_year)
        month = int(self.archive_month)

        if(month < 12):
            month += 1
            month = str(month)

        elif(month == 12):
            month = 1
            year += 1

        if(len(str(month)) == 1):
            month = f"0{month}"

        year = str(year)
        self.log.info(f"Creating new value for next month to configuration")

        update_config["Archive"]["Archive_Month"].value = month
        update_config["Archive"]["Archive_Year"].value = year
        update_config.update_file()

        self.log.info("Updated value in config.ini")

    def secure_pass(self, config_name, ftp_params):
        ftp_pass = ftp_params["FTP_pass"]
        key = ftp_params["key"]
        len_ftp_pass = len(str(ftp_pass))

        self.log.info("Checking FTP password")
        if((len_ftp_pass > 0) and (len_ftp_pass < 99)):

            update_config = ConfigUpdater()
            update_config.read(config_name)

            #
            # TOP SECRET
            #

            update_config["FTP"]["FTP_pass"].value = ftp_encrypt_pass
            update_config.update_file()
            self.log.info("Updated password in config.ini")

        return ftp_params

    def decrypt_pass(self, ftp_params):
        ftp_pass = ftp_params["FTP_pass"]
        key = ftp_params["key"]
        len_ftp_pass = len(str(ftp_pass))

        if(len_ftp_pass > 0):
           
           #
           # TOP SECRET
           #

            ftp_params["FTP_pass"] = ftp_pass_decrypt

        return ftp_params

    def check_config(self, file_config):

        default_cfg = """###############################################
############# POWERED BY MAJSTER ##############
###############################################
######## Skrypt dzia??a przy za??o??eniu, ########
###### ??e data w nazwie pliku ma format: ######
############ RRRRMMDD albo RRMMDD #############
###############################################

[Archive]
# ??cie??ka ??r??d??owa archiwizowania (Folder z logami)
Source_Path_Arch = D:\Skrypty\Logi
# ??cie??ka docelowa archiwizowania (Folder gdzie maj?? by?? archiwizowane)
Destination_Path_Arch = D:\Skrypty\Logi\Archiwum Logow
# Czy data w nazwie plik??w na 6 znak??w (logi IIS maj?? po 6 znak??w np. ext_210315.log)
Log_Name_Format_Year_6Char = False
# Archiwizowa?? ka??dy dzie?? osobno (True) czy ca??y miesi??c w jednym zipie (False)
Day_Separately = True
# Jaki rok archiwizowa???
Archive_Year = 2022
# Jaki miesi??c archiwizowa???
Archive_Month = 05
# Jaki system (sugeruj?? bez spacji je??eli idzie na FTP)
Application_Name = Python
# Nazwa instancji
Instance_Name = AP1
# Nazwa archiwizowanych log??w (prefix nazwy ZIP)
Prefix_Arch_File_Name = Logs_Python
# Nazwa serwera, z kt??rego b??d?? archiwizowane pliki
Server_Name = localhost
# Czy usuwa?? pliki po archiwizacji? (True/False)
Delete_files = False
# Automatyczna zmiana miesi??ca (program automatycznie zmieni w pliku config miesi??c na nast??pny)
Auto_Change_Month = True

# Struktura tworzenia katalog??w: .\\{year}{month}\\{system}\\{instance}\\{prefix}_{server_name}_{year}{month}<{day}>.zip
# Dla domy??lnego przyk??adu b??dzie nast??puj??ce: .\\202205\\Python\\AP1\\Logs_Python_localhost_202205<01-31>.zip
# Je??eli nie b??dzie True lub False - domy??lnie przyjmie False

[FTP]
# Czy wrzuci?? zipy na FTP?
Move_To_FTP = True
# Czy usuwa?? zipy po przeniesieniu na FTP?
Delete_archives_files = False
# Po ilu miesi??cach usuwa?? zipy (Przej??cie/Odpalenie skryptu)?
Month_to_del_archives = 3
# Serwer FTP
FTP_Server_Name = localhost
# Port FTP
FTP_Port = 21
# Passy FTP
FTP_Login = user
FTP_Pass = pass"""
        try:
            open(file_config)

        except IOError:
            err = "Config Error: Not found config.ini or is demaged !"
            print(err)
            self.log.error(f"{err}")

            if(path.isfile(file_config)):
                rmtree(file_config)
                self.log.warning("Removed config.ini")
 
            with open(file_config, mode="w", encoding="UTF-8") as default_config:
                default_config.write(default_cfg)
                default_config.close()
                
            self.log.warning("Created default config.ini")
            self.log.warning("Complete the config.ini")
            exit()
            

        except KeyError as err:
            print(err)
            self.log.error(f"Config Error: {err}")
            exit()

        except:
            print(exc_info())
            self.log.exception(exc_info())
            exit()

    def __del__(self) -> None:
        del self.log