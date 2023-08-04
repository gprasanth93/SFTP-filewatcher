import paramiko
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class SftpHandler(FileSystemEventHandler):
    def __init__(self, sftp, local_dir):
        self.sftp = sftp
        self.local_dir = local_dir

    def on_created(self, event):
        if event.is_directory:
            return

        remote_path = event.src_path.replace(self.local_dir, '').lstrip('/')
        local_path = event.src_path
        self.sftp.get(remote_path, local_path)
        print(f"Downloaded file: {remote_path}")

def sftp_listen_and_download(host, port, username, password, remote_dir, local_dir):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=host, port=port, username=username, password=password)

    sftp_client = ssh_client.open_sftp()

    event_handler = SftpHandler(sftp_client, local_dir)
    observer = Observer()
    observer.schedule(event_handler, path=local_dir, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    host = "your_remote_sftp_host"
    port = 22  # Change to the appropriate port number if needed
    username = "your_username"
    password = "your_password"
    remote_dir = "/path/to/remote/directory"
    local_dir = "/path/to/local/directory"

    sftp_listen_and_download(host, port, username, password, remote_dir, local_dir)
