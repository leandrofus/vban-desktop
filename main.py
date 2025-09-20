import sys
import shutil
import threading
import subprocess
from PyQt5 import QtWidgets, QtCore
from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageDraw
from vban_config import config, load_config, save_config

vban_process = None
icon_instance = None

def run_vban_receptor(host=None, port=None, stream=None, vban_path=None, stop=False):
    global vban_process

    if stop:
        if vban_process and vban_process.poll() is None:
            vban_process.terminate()
            vban_process.wait()
        return False

    host = host or config["host"]
    port = port or config["port"]
    stream = stream or config["stream"]
    vban_path = vban_path or config.get("vban_path", "/usr/local/bin/vban_receptor")

    if vban_process and vban_process.poll() is None:
        vban_process.terminate()
        vban_process.wait()

    if not shutil.which(vban_path):
        print(f"[WARN] VBAN receptor not found at {vban_path}. Skipping execution.")
        return False

    cmd = [vban_path, "-i", host, "-p", port, "-s", stream, "-b", "alsa"]
    vban_process = subprocess.Popen(cmd)
    return True

# GUI
class ConfigWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VBAN Config")
        self.setGeometry(100, 100, 300, 150)
        layout = QtWidgets.QFormLayout()
        self.host_input = QtWidgets.QLineEdit(config["host"])
        self.port_input = QtWidgets.QLineEdit(str(config["port"]))
        self.stream_input = QtWidgets.QLineEdit(config["stream"])
        self.vban_path_input = QtWidgets.QLineEdit(config["vban_path"])
        layout.addRow("Host:", self.host_input)
        layout.addRow("Port:", self.port_input)
        layout.addRow("Stream:", self.stream_input)
        layout.addRow("VBAN Path:", self.vban_path_input)
        save_btn = QtWidgets.QPushButton("Save and Restart")
        save_btn.clicked.connect(self.save_and_restart)
        layout.addRow(save_btn)
        self.setLayout(layout)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.destroyed.connect(self.cleanup_on_close)

    def closeEvent(self, event):
        event.ignore()
        self.hide()

    def save_and_restart(self):
        config.update({
            "host": self.host_input.text(),
            "port": self.port_input.text(),
            "stream": self.stream_input.text(),
            "vban_path": self.vban_path_input.text(),
        })
        save_config()
        threading.Thread(target=run_vban_receptor, args=(config["host"], config["port"], config["stream"], config["vban_path"]), daemon=True).start()
        QtWidgets.QMessageBox.information(self, "VBAN", "VBAN restarted with the new configuration.")
        self.hide()

    def cleanup_on_close(self):
        if icon_instance:
            icon_instance.stop()
        if vban_process and vban_process.poll() is None:
            vban_process.terminate()
            vban_process.wait()

# Bandeja
def create_image():
    size = 64
    image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    dc = ImageDraw.Draw(image)
    dc.ellipse((0, 0, size-1, size-1), fill=(30, 144, 255, 255))
    center = size // 2
    for r in range(12, 40, 8):
        dc.ellipse((center-r, center-r, center+r, center+r), outline=(255, 215, 0, 255), width=3)
    dc.ellipse((center-6, center-6, center+6, center+6), fill=(255, 215, 0, 255))
    return image

def show_config(icon, item):
    window.show()
    window.raise_()
    window.activateWindow()

def on_quit(icon, item=None):
    if vban_process and vban_process.poll() is None:
        vban_process.terminate()
        vban_process.wait()
    icon.stop()
    QtWidgets.QApplication.quit()

def tray_thread():
    global icon_instance
    menu = Menu(
        MenuItem("Configure VBAN", show_config),
        MenuItem("Exit", on_quit)
    )
    icon_instance = Icon("VBAN Tray", create_image(), "VBAN", menu)
    icon_instance.run()

# MAIN
if __name__ == "__main__":
    load_config()
    threading.Thread(target=run_vban_receptor, daemon=True).start()
    app_qt = QtWidgets.QApplication(sys.argv)
    window = ConfigWindow()
    threading.Thread(target=tray_thread, daemon=True).start()
    sys.exit(app_qt.exec_())
