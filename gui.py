import data_setup
import lib_cache_setup
import procedures
import multimc
import sys
import argparse
from gooey import Gooey, GooeyParser

force = False

@Gooey()
def main():
    parser = GooeyParser(description="Create Forge Instances for MultiMC")
    main = parser.add_argument_group('')
    main.add_argument('--input',
                      metavar='Forge Installer',
                      help='The Forge Installer Jar you want to process',
                      nargs='+',
                      gooey_options={
                          'validator': {
                              'test': 'user_input[-4:] in {".jar"}',
                              'message': 'some helpful message'
                          }
                      },
                      required=True,
                      widget='MultiFileChooser')
    options = parser.add_argument_group('Options')  
    options.add_argument('--force',
                      metavar='Force Redownload & Recreation',
                      help='Will force the redownload of all libraries and recreation of the instance',
                      widget='CheckBox')

    args = parser.parse_args()
    # print(args)
    force = args.force

    for file in args.input:
        forge_file = file
        # print(file.name)
        lib_cache_setup.cache_setup()
        procs = data_setup.data_setup(forge_file)
        procedures.run_procs(procs)
        multimc.make_instance(forge_file)

if __name__ == '__main__':
    main()
