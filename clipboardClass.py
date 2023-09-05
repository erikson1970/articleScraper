# coding: utf-8
from sys import platform
import subprocess


class Clipboard(object):
    def __init__(self) -> None:
        if platform == "linux" or platform == "linux2":
            # linux
            self.system = "linux"
        elif platform == "darwin":
            # OS X
            self.system = "macOS"
        elif platform == "win32":
            # Windows...
            self.system = "windows"

    def get_clipboard_data(self):
        if self.system == "linux":
            p = subprocess.Popen(
                ["xclip", "-selection", "clipboard", "-o"], stdout=subprocess.PIPE
            )
        elif self.system == "macOS":
            p = subprocess.Popen(["pbpaste"], stdout=subprocess.PIPE)
        elif self.system == "windows":
            p = subprocess.Popen(["clip"], stdout=subprocess.PIPE)
        retcode = p.wait()
        data = p.stdout.read()
        return data

    def set_clipboard_data(self, data):
        data = bytes(data, "utf-8")
        if self.system == "linux":
            p = subprocess.Popen(
                ["xclip", "-selection", "clipboard"], stdin=subprocess.PIPE
            )
        elif self.system == "macOS":
            p = subprocess.Popen(["pbcopy"], stdin=subprocess.PIPE)
        elif self.system == "windows":
            p = subprocess.Popen(["clip"], stdin=subprocess.PIPE)
        p.stdin.write(data)
        p.stdin.close()
        retcode = p.wait()

if __name__ == "__main__":
    # our string data
    data = "Today is a nice day!"
    cl = Clipboard()
    print(f"System: {cl.system}")

    # Set the data
    cl.set_clipboard_data(data)

    # Get the new data
    new_data = cl.get_clipboard_data()

    # Print it out
    print(new_data)
