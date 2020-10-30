import json
import glob
import argparse
import os
from murakami.exporters.http import HTTPExporter
def main():
    print(os.environ)
    parser = argparse.ArgumentParser(description='Uploads JSON results via HTTPExporter')
    parser.add_argument('-p', '-path', type=str, dest="path",
                    help='input path', default=os.environ.get('MURAKAMI_EXPORT_PATH'))
    parser.add_argument('-u', '-url', type=str, dest="url",
                    help='URL to send JSON data to', default=os.environ.get('MURAKAMI_EXPORTERS_HTTP0_URL'))
    args = parser.parse_args()
    exporter = HTTPExporter(config={'url': args.url})
    print("Reading path " + args.path)
    files = glob.glob(args.path, recursive=True)
    print("Files: " + str(files))
    for filename in files:
        with open(filename) as f:
            data = f.read()
            exporter.push(data=data)
if __name__ == "__main__":
    main()
