"""
Murakami is a tool for creating an automated internet measurement service.
Results are saved as individual files in JSON new line format (.jsonl), and
this is a utility script designed to convert them to other formats.
"""

import difflib
import glob
import logging
import os

import configargparse
import csv
import jsonlines

logger = logging.getLogger(__name__)

DEFAULT_FORMAT = "csv"
DEFAULT_TEST = "speedtest"


def flatten_json(b, delim):
    """
    A simple function for flattening JSON by concatenating keys w/ a delimiter.
    """
    val = {}
    for i in b.keys():
        if isinstance(b[i], dict):
            get = flatten_json(b[i], delim)
            for j in get.keys():
                val[i + delim + j] = get[j]
        else:
            val[i] = b[i]

    return val


def extract_pattern(string, template):
    """
    A rudimentary function for extracting patterns from a string by comparing
    differences between it and a template string.
    """
    output = {}
    entry = ""
    value = ""

    for s in difflib.ndiff(string, template):
        if s[0] == " ":
            if entry != "" and value != "":
                output[entry] = value
                entry = ""
                value = ""
        elif s[0] == "-":
            value += s[2]
        elif s[0] == "+":
            if s[2] != "%":
                entry += s[2]

    # check ending if non-empty
    if entry != "" and value != "":
        output[entry] = value

    return output


def import_speedtest(path):
    """
    Import function for Speedtest.net tests.
    """
    with jsonlines.open(path, mode="r") as reader:
        line = reader.read()
        return flatten_json(line, "_")


tests = {"speedtest": import_speedtest}


def export_csv(path, data):
    """
    Export function for CSV-format output files.
    """
    with open(path, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        return writer.writerows(data)


exporters = {"csv": export_csv}


def main():
    """ The main function for the converter script."""
    parser = configargparse.ArgParser(
        auto_env_var_prefix="murakami_convert_",
        description="A Murakami test output file format parser.",
        ignore_unknown_config_file_keys=False,
    )
    parser.add(
        "-l",
        "--loglevel",
        dest="loglevel",
        default="DEBUG",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set the logging level",
    )
    parser.add(
        "-f",
        "--format",
        dest="format",
        default=DEFAULT_FORMAT,
        choices=["csv"],
        help="Set the output format.",
    )
    parser.add(
        "-t",
        "--test",
        dest="test",
        required=True,
        choices=["speedtest"],
        help="The type of test data that is being parsed.",
    )
    parser.add(
        "-o",
        "--output",
        required=True,
        dest="output",
        help="Path to output file.",
    )
    parser.add(
        "-p",
        "--pattern",
        dest="pattern",
        help=
        "An input filename pattern containing one or more of %%l (location type), %%n (network type), %%c (connection type), and %%d (datestamp).",
    )
    parser.add(
        "-r",
        "--recurse",
        action="store_true",
        dest="recurse",
        default=False,
        help="If the input is a directory, recursively search it for files.",
    )
    parser.add(
        "input",
        nargs="+",
        help=
        "The input filename, directory, or pattern containing test results.",
    )
    settings = parser.parse_args()

    pathlist = []
    for i in settings.input:
        pathlist.append(glob.glob(i, recursive=settings.recurse))

    pathlist = list(set().union(*pathlist))

    records = []
    for path in pathlist:
        importer = tests.get(settings.test, DEFAULT_TEST)
        contents = importer(path)
        if settings.pattern:
            pattern = extract_pattern(os.path.basename(path), settings.pattern)
            if "l" in pattern:
                contents["location"] = pattern["l"]
            if "n" in pattern:
                contents["network_type"] = pattern["n"]
            if "c" in pattern:
                contents["connection_type"] = pattern["c"]
            if "d" in pattern:
                contents["datestamp"] = pattern["d"]
        records.append(contents)

    exporter = exporters.get(settings.format, DEFAULT_FORMAT)
    exporter(settings.output, records)

    logging.basicConfig(
        level=settings.loglevel,
        format="%(asctime)s %(filename)s:%(lineno)s %(levelname)s %(message)s",
    )
