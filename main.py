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
        '-i', '--input', nargs='+', type=argparse.FileType('r'), help='one or more paths to forge-installer jar files', required=True)
    parser.add_argument(
        '-f', '--force', help='force library redownload and instance recreation', action='store_true')
    args = parser.parse_args()
    # print(args)
    force = args.force

    for file in args.input:
        forge_file = file.name
        # print(file.name)
        lib_cache_setup.cache_setup()
        procs = data_setup.data_setup(forge_file)
        procedures.run_procs(procs)
        multimc.make_instance(forge_file)
