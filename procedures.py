import subprocess
from zipfile import ZipFile
from sys import platform as _platform


def run_procs(procs):
    """Runs the given processes using the JVM."""
    for proc in procs:
        main_class = get_main_class(proc['jar'])
        
        from sys import platform as _platform

        # yep..
        separator = ";"
        if _platform.startswith('linux'):
           # linux
           separator = ":"
        elif _platform == "darwin":
           # MAC OS X
           separator = ":"
        elif _platform.startswith('win'):
           # Windows
           separator = ";"

        args = [
            'java',
            '-cp',
            separator.join([proc['jar'], *proc['classpath']]),
            main_class,
            *proc['args']
        ]
        print('Running', proc['jar'], flush=True)
        complete = subprocess.run(
            args,
            encoding='UTF-8',
            stdout=subprocess.DEVNULL
        )
        if complete.returncode != 0:
            print('Process completed with exit code', complete.returncode, flush=True)

def get_main_class(jar_name):
    """Inspects the manifest file and retrieves the main class name."""
    main_class_attr = 'Main-Class: '
    with ZipFile(jar_name) as jar:
        with jar.open('META-INF/MANIFEST.MF') as manifest:
            for line in manifest:
                str_line = line.decode('UTF-8')
                if str_line.startswith(main_class_attr):
                    # assumes the main class attribute is < 72 bytes long
                    return str_line[len(main_class_attr):].strip()
    raise RuntimeError('Main class not found in manifest')
