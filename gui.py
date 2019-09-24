from gooey import Gooey, GooeyParser


@Gooey(target="python3 main.py", program_name='Forge Downloader', suppress_gooey_flag=True)
def main():
    parser = GooeyParser(description="Create Forge Instances for MultiMC")
    main = parser.add_argument_group('')
    main.add_argument('--input',
                      metavar='Forge Installer',
                      help='The Forge Installer Jar you want to process',
                      gooey_options={
                          'validator': {
                              'test': 'user_input[-4:] in {".jar"}',
                              'message': 'some helpful message'
                          }
                      },
                      required=True,
                      widget='FileChooser')
    options = parser.add_argument_group('test')  
    options.add_argument('--force',
                      metavar='Force Redownload & Recreation',
                      help='Will force the redownload of all libraries and recreation of the instance',
                      widget='CheckBox')

    parser.parse_args()


if __name__ == '__main__':
    main()
