import sys

from statkube.wrapper import (
    get_parsed_args,
    GithubWrapper,
    DEFAULT_SETTING_FILE,
    GH_TOKEN_FILE,
)

def main(args=None):
    if args is None:
        args = sys.argv[1:]

    parsed = get_parsed_args(args)

    if parsed.show_default_settings:
        print ("Copy file below, change it and set env var "
               "STATKUBE_SETTINGS_FILE.")
        print DEFAULT_SETTING_FILE
        sys.exit(0)

    if parsed.show_token_path:
        print GH_TOKEN_FILE
        sys.exit(0)

    GithubWrapper(parsed).run()


if __name__ == '__main__':
    main()
