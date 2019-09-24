import urllib.request as req
import json
import os.path


def minecraft_download_url(install_profile):
    mc_ver = install_profile['minecraft']
    mmc_meta_url = "https://meta.multimc.org/v1/net.minecraft/" + mc_ver + ".json"
    r = req.Request(mmc_meta_url, headers={'User-Agent': "Magic Browser"})
    with req.urlopen(r) as url:
        data = json.loads(url.read().decode())
        return data['mainJar']['downloads']['artifact']['url']


def download_minecraft(install_profile, base):
    path = os.path.join(base, 'client.jar')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    url = minecraft_download_url(install_profile)
    if not os.path.exists(path):
        print('Downloading', url, flush=True)
        with open(path, 'wb') as f:
            with req.urlopen(url) as data:
                f.write(data.read())
    return path
