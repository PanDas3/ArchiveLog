from ftplib import FTP, error_perm
from os import listdir, path
from sys import exc_info

from log import Log

class File_Transfer_Protocol():
    def __init__(self) -> None:
        self.log = Log()

    def connect_ftp(self, ftp_params):
        ftp = FTP()
        ftp_server = ftp_params["FTP_server_name"]
        ftp_port = ftp_params["FTP_port"]
        ftp_login = ftp_params["FTP_login"]
        ftp_passwd = ftp_params["FTP_pass"]

        try:
            ftp.connect(ftp_server, ftp_port)
            ftp.login(ftp_login, ftp_passwd)
            print(ftp.getwelcome(),"\n")
            self.log.info(f"Connected to FTP: {ftp_server}")

            return ftp
        
        except:
            print(exc_info())
            self.log.error(exc_info())         

    def transfer_zip(self, ftp, params):

        if(type(params) == dict):
            dest_path = params["org_dest_path_arch"]
        else:
            dest_path = params
        
        try:
            for name_loop in listdir(dest_path):
                local_ftp_path = path.join(dest_path, name_loop)

                if(path.isfile(local_ftp_path) == True):
                    print("STOR", local_ftp_path)
                    self.log.info(f"Moving {local_ftp_path} to FTP")
                    ftp.storbinary('STOR ' + name_loop, open(local_ftp_path,'rb'))

                elif(path.isdir(local_ftp_path) == True):
                    print("MKD", name_loop)

                    try:
                        ftp.mkd(name_loop)

                    except error_perm as e:
                        if(e.args[0].startswith("550") == False):
                            self.log.warning(e.args[0])
                            raise

                    print("CWD", name_loop)
                    ftp.cwd(name_loop)
                    
                    self.transfer_zip(ftp, local_ftp_path)

                    print("CWD", "..")
                    ftp.cwd("..")

        except:
            print(exc_info()[1])
            if(str(exc_info()[1]).startswith("550 Directory")):
                self.log.warning(f"FTP: {str(exc_info()[1])}")
            elif(str(exc_info()[1]).startswith("550 Permission")):
                self.log.error(f"FTP: {str(exc_info()[1])}")
            else:
                self.log.error(f"FTP: {str(exc_info()[:-1])}")

    def disconnect_ftp(self, ftp):
        try:
            ftp.quit()
            self.log.info("Disconnect from FTP")

        except:
            print(exc_info())
            self.log.error(exc_info()[:-1])

    def __del__(self) -> None:
        del self.log