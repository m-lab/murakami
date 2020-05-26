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
import json

logger = logging.getLogger(__name__)

DEFAULT_FORMAT = "csv"
DEFAULT_TEST = "speedtest"


class ConvertException(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return self.message
        else:
            return "ConvertException"

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


def import_dash_legacy(path):
    """
    Import function for legacy-format DASH tests..
    """
    record = {}
    with jsonlines.open(path, mode="r") as reader:
        data = reader.read()
        if "test_name" in data:
            record["test_name"] = data["test_name"]
            record["test_runtime"] = data["test_runtime"]
            record["test_start_time"] = data["test_start_time"]
            record["connect_latency"] = data["test_keys"]["simple"][
                "connect_latency"]
            record["median_bitrate"] = data["test_keys"]["simple"][
                "median_bitrate"]
            record["min_playout_delay"] = data["test_keys"]["simple"][
                "min_playout_delay"]
            record["probe_asn"] = data["probe_asn"]
            record["probe_cc"] = data["probe_cc"]
            return record


def import_ndt_legacy(path):
    """
    Import function for legacy-format NDT tests..
    """
    record = {}
    with jsonlines.open(path, mode="r") as reader:
        data = reader.read()
        if "probe_asn" in data:
            record["server_address"] = data["test_keys"]["server_address"]
            record["download"] = data["test_keys"]["simple"]["download"]
            record["upload"] = data["test_keys"]["simple"]["upload"]
            record["ping"] = data["test_keys"]["simple"]["ping"]
            record["avg_rtt"] = data["test_keys"]["advanced"]["avg_rtt"]
            record["max_rtt"] = data["test_keys"]["advanced"]["max_rtt"]
            record["min_rtt"] = data["test_keys"]["advanced"]["min_rtt"]
            record["congestion_limited"] = data["test_keys"]["advanced"][
                "congestion_limited"]
            record["packet_loss"] = data["test_keys"]["advanced"][
                "packet_loss"]
            record["sender_limited"] = data["test_keys"]["advanced"][
                "sender_limited"]
            record["receiver_limited"] = data["test_keys"]["advanced"][
                "receiver_limited"]
            record["probe_asn"] = data["probe_asn"]
            record["probe_cc"] = data["probe_cc"]
            return record

def import_ndt5(path):
    print("Converting {}...".format(path))
    with open(path) as f:
        data = json.load(f)

        # Check this is an NDT5 test summary.
        if data.get('TestName') != "ndt5":
            raise ConvertException("{}: Invalid ndt5 output file."
                .format(path))

        # Check this test completed without errors.
        if data.get('TestError') is not None:
            raise ConvertException(
                "{}: test did not complete successfully, skipping."
                    .format(path))
        return data

def import_ndt7(path):
    print("Converting {}...".format(path))
    with open(path) as f:
        data = json.load(f)

        # Check this is an ndt7 test summary.
        if data.get("TestName") != "ndt7":
            raise ConvertException("{}: Invalid ndt7 output file."
                .format(path))

        # Check this test completed without errors.
        if data.get('TestError') is not None:
            raise ConvertException(
                "{}: test did not complete successfully, skipping."
                    .format(path))
        return data

tests = {
    "speedtest": import_speedtest,
    "dash_legacy": import_dash_legacy,
    "ndt_legacy": import_ndt_legacy,
    "ndt5": import_ndt5,
    "ndt7": import_ndt7
}


def export_csv(path, data):
    """
    Export function for CSV-format output files.
    """
    with open(path, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys(), quotechar='"',
            quoting=csv.QUOTE_NONNUMERIC)
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
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set the logging level",
    )
    parser.add(
        "-f",
        "--format",
        dest="format",
        default=DEFAULT_FORMAT,
        choices=exporters.keys(),
        help="Set the output format.",
    )
    parser.add(
        "-t",
        "--test",
        dest="test",
        required=True,
        choices=tests.keys(),
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

    logging.basicConfig(
        level=settings.loglevel,
        format="%(asctime)s %(filename)s:%(lineno)s %(levelname)s %(message)s",
    )

    pathlist = []
    for i in settings.input:
        pathlist.append(glob.glob(i, recursive=settings.recurse))

    pathlist = list(set().union(*pathlist))

    records = []
    for path in pathlist:
        importer = tests.get(settings.test, DEFAULT_TEST)
        try:
            contents = importer(path)
        except Exception as ex:
            print(ex)
            continue

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
