import subprocess
from zipfile import ZipFile


def run_procs(procs):
    """Runs the given processes using the JVM."""
    for proc in procs:
        main_class = get_main_class(proc['jar'])
        args = [
            'java',
            '-cp',
            ';'.join([proc['jar'], *proc['classpath']]),
            main_class,
            *proc['args']
        ]
        print('Run', proc['jar'])
        complete = subprocess.run(
            args,
            encoding='UTF-8',
            stdout=subprocess.DEVNULL
        )
        if complete.returncode != 0:
            print('Process completed with exit code', complete.returncode)

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
