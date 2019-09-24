import data_setup
import lib_cache_setup
import procedures
import multimc
import sys
import argparse

force = False

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Turns the Forge Installer into a usable MultiMC instance')
    parser.add_argument(
        '-i', '--input', help='path to forge-installer jar file', required=True)
    parser.add_argument(
        '-f', '--force', help='force library redownload and instance recreation', action='store_true')
    args = parser.parse_args()
    # print(args)
    force = args.force
    forge_name = args.input
    lib_cache_setup.cache_setup()
    procs = data_setup.data_setup(forge_name)
    procedures.run_procs(procs)
    multimc.make_instance(forge_name)
