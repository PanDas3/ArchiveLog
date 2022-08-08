from gc import collect
from sys import exc_info
from os import getcwd, path

# Custom
from config import Configuration
from log import Log
from sys_path import SysPath
from archive import Archive
from zipping import Zipping
from ftp import File_Transfer_Protocol
from mail import SendMail

if(__name__ == "__main__"):
    cfg = Configuration()
    log = Log()
    sys_path = SysPath()
    arch = Archive()
    zip = Zipping()
    ftp = File_Transfer_Protocol()
    mail = SendMail()

    file_config = path.join(getcwd(), "config.ini")

    log.info("##### Start Application #####")

    print("##########################")
    print("### Powered by Majster ###")
    print("##########################\n")
    
    try:
        # Verify config
        cfg.check_config(file_config)
        cfg.read_config(file_config)

        # Getting params (dict)
        archive_params = cfg.get_archive_params()
        SMTP_params = cfg.get_SMTP_params()
        FTP_params = cfg.get_FTP_params()

        # Checking password for FTP
        FTP_params = cfg.secure_pass(file_config, FTP_params)   # Sprawdzanie czy hasło szyforwane, jak nie -> Szyfruj
        FTP_params = cfg.decrypt_pass(FTP_params)               # Deszyfrowanie hasła

        # Checking path (if exists)
        sys_path.check_main_path(archive_params)
        
        # Sorting files (if noone files -> exit())
        sort_files = arch.sort_files(archive_params)
        sys_path.create_new_arch_path(archive_params)

        # Zipping and testing CRC
        zip.zip(sort_files, archive_params)
        result = zip.test_zip(archive_params)

        # Transfer archives to FTP
        if(result == False):
            ok = True
            if(FTP_params["move_to_FTP"] == True):
                try: 
                    conn = ftp.connect_ftp(FTP_params)
                    ftp.transfer_zip(conn, FTP_params)
                    ftp.disconnect_ftp(conn)
                
                except:
                    ok = False
                    log.error("Something was wrong - next operation will be aborted")
            
            if(ok == True):
                # Delete files
                sys_path.delete_log_files(sort_files, archive_params)
                sys_path.delete_archives(archive_params, FTP_params)

                # Change month to next month
                if(archive_params["auto_change_month"] == True):
                    cfg.change_config_to_next_month(file_config)

    except:
        if(type(exc_info()[1]) != SystemExit):
            print(exc_info())
            log.exception(exc_info()[:-1])
            raise

    finally:
        try:
            if(SMTP_params["send_error"] == True):
                errors = log.search_error()
                mail.send_mail(SMTP_params, errors)

        except:
            log.error(exc_info()[:-1])

        log.info("##### End Application #####")
        print("##########################")
        print("### Powered by Majster ###")
        print("##########################\n")

        # Del variables and clear RAM
        try:
            del archive_params
            del SMTP_params
            del FTP_params

            try:
                del sort_files
                del result

                try:
                    del ok
                    del conn
                    del errors

                except:
                    pass
            except:
                pass
        except:
            pass
        
        finally:
            del cfg
            del log
            del sys_path
            del arch
            del zip
            del ftp
            del mail
            collect()