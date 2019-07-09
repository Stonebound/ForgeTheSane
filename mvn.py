import urllib.request as req
import os.path
import re


mvn_pattern = re.compile(
    r"""
        \[
        (?P<group>[^:]+):
        (?P<artifact>[^:]+):
        (?P<version>[^:@]+)
        (?::(?P<classifier>\w+))?
        (?:@(?P<ext>\w+))?
        \]
    """, re.X)

def get_libraries(install_profile, archive, root):
    """Downloads or extracts libraries specified in the install profile to the
    location given by `root`.

    Return - a dict of { <library-name>: <path-to-library> }.
    """
    libs_prof = install_profile['libraries']
    libs = {}
    for lib_prof in libs_prof:
        artifact = lib_prof['downloads']['artifact']
        path = os.path.join(root, artifact['path'])
        libs[lib_prof['name']] = path
        url = artifact['url']
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if not os.path.exists(path):
            if url:
                print('Download', url)
                with open(path, 'wb') as f:
                    with req.urlopen(url) as data:
                        f.write(data.read())
            else:
                # local file inside the archive
                # does not use ZipFile.extract because the path is
                # structurally different
                entry_path = 'maven/' + artifact['path']
                print('Extract', entry_path)
                with archive.open(entry_path) as entry:
                    with open(path, 'wb') as f:
                        f.write(entry.read())
    return libs

def get_data(install_profile, archive, root):
    """Transforms client data specs in the install profile.

    Maven specifiers are transformed into paths starting from `root`.
    Literal paths are extracted from `archive` and placed relative to `root`.
    SHA hashes are stripped, since we don't need them.

    Return - a dict of { <data-name>: <path-to-data> }.
    """
    data_prof = install_profile['data']
    data = {}
    for datum_name in data_prof:
        path_spec = data_prof[datum_name]['client']
        if path_spec[0] == '[':
            # maven specifiers are in square brackets
            data[datum_name] = os.path.join(root, maven_to_path(path_spec))
            pass
        elif path_spec[0] == "'":
            # we don't use the SHA hashes
            pass
        else:
            # literal path, extract to new location
            data[datum_name] = os.path.join(root, path_spec[1:])
            os.makedirs(os.path.dirname(data[datum_name]), exist_ok=True)
            if not os.path.exists(data[datum_name]):
                print('Extract', path_spec[1:])
                with archive.open(path_spec[1:]) as entry:
                    with open(data[datum_name], 'wb') as f:
                        f.write(entry.read())
    return data

def maven_to_path(path_spec):
    match = mvn_pattern.search(path_spec).groupdict()
    return "{group}/{artifact}/{version}/{artifact}-{version}{d}{classifier}.{ext}".format(
            group=match['group'].replace('.', '/'),
            artifact=match['artifact'],
            version=match['version'],
            d='-' if match['classifier'] else '',
            classifier=match['classifier'] or '',
            ext=match['ext'] or 'jar',
        )
