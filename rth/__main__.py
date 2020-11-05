import argparse
from rth.adapters.json_adapter import JSONAdapter
from rth.core.errors import WrongFileFormat


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="the file path which will be decoded")
    parser.add_argument("-O", "--output", help="outputs the results in a txt file")
    parser.add_argument("-I", "--ignore", help="Ignore errors due to unrecognised option name", action="store_true")

    args = parser.parse_args()

    ext = args.input.split('.')[-1]

    allowed_extensions = {'JSON': 'json'}

    if ext not in list(allowed_extensions.values()):
        raise WrongFileFormat(ext, allowed_extensions)

    adapter = JSONAdapter(args.input, args.ignore, debug=True)()

    if args.output:
        adapter.output_routing_tables(args.output)
    else:
        adapter.display_routing_tables()


if __name__ == '__main__':
    main()
