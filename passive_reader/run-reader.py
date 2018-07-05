import os
import subprocess

dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
process_name = 'sudo python ' + dir_path + '/rfid_python_lib/background_reader.py'
print(process_name)
subprocess.Popen(process_name, shell=True)
