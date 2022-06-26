from sys import exc_info
from os import getcwd, path

# Custom
from config import Configuration
from log import Log
from sys_path import SysPath
from archive import Archive
from zipping import Zipping
from ftp import File_Transfer_Protocol

if(__name__ == "__main__"):
    cfg = Configuration()
    log = Log()
    sys_path = SysPath()
    arch = Archive()
    zip = Zipping()
    ftp = File_Transfer_Protocol()

    file_config = path.join(getcwd(), "config.ini")

    log.info("##### Start Application #####")

    print("##########################")
    print("### Powered by Majster ###")
    print("##########################\n")
    
    try:
        cfg.check_config(file_config)                           # Weryfikacja czy istnieje, jak nie -> Twórz domyślny
        cfg.read_config(file_config)                            # Czytanie + przekazanie parametrów
        archive_params = cfg.get_archive_params()               # Pobieranie parametrów
        FTP_params = cfg.get_FTP_params()                       # Pobieranie parametrów
        FTP_params = cfg.secure_pass(file_config, FTP_params)   # Sprawdzanie czy hasło szyforwane, jak nie -> Szyfruj
        FTP_params = cfg.decrypt_pass(FTP_params)               # Deszyfrowanie hasła

        sys_path.check_main_path(archive_params)        # Sprawdzanie ścieżek main
        sort_files = arch.sort_files(archive_params)    # Sortowanie plików -> Jeśli brak, przerwij skrypt
        sys_path.create_new_arch_path(archive_params)   # Tworzenie ścieżki docelowej
        zip.zip(sort_files, archive_params)             # Zippowanie
        result = zip.test_zip(archive_params)           # Testowanie CRC
        result = False
        if(result == False):
            if(FTP_params["move_to_FTP"] == True):
                conn = ftp.connect_ftp(FTP_params)                      # Połączenie FTP
                ftp.transfer_zip(conn, FTP_params)                      # Transfer plików na FTP
                ftp.disconnect_ftp(conn)                                # Disconnect FTP
                
            sys_path.delete_log_files(sort_files, archive_params)   # Usuwanie źródłowych logów
            sys_path.delete_archives(archive_params, FTP_params)    # Usuwanie archiwiów po przeniesieniu na FTP

            if(archive_params["auto_change_month"] == True):
                cfg.change_config_to_next_month(file_config)        # Zmiana miesiąca

    except:
        if(type(exc_info()[1]) != SystemExit):
            print(exc_info())
            log.exception(exc_info()[:-1])
            raise

    finally:
        log.info("##### End Application #####")
        print("##########################")
        print("### Powered by Majster ###")
        print("##########################\n")
        
        del cfg
        del log
        del sys_path
        del arch
        del zip
        del ftp