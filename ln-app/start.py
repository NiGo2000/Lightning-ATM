import os
import subprocess

# Pfad zur Svelte-Anwendung
svelte_path = os.path.abspath('front-end/app/')

# Pfade zu den Python-Dateien
backend_path = os.path.abspath('back-end')
app_path = os.path.join(backend_path, 'app.py')
test_path = os.path.join(backend_path, 'test_money.py')

# Starte die Python-Dateien in neuen Konsolenfenstern
subprocess.Popen(['start', 'cmd', '/k', 'python', app_path], cwd=backend_path, shell=True)
subprocess.Popen(['start', 'cmd', '/k', 'python', test_path], cwd=backend_path, shell=True)

# Starte die Svelte-Anwendung in einem neuen Konsolenfenster
subprocess.Popen(['start', 'cmd', '/k', 'npm', 'run', 'dev'], cwd=svelte_path, shell=True, bufsize=1)


