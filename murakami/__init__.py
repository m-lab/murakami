"""
Murakami is a tool for creating an automated internet measurement service,
running in a Docker container. A Murakami measurement container can be
configured to automatically run supported tests four times a day using a
randomized schedule, and export each test result to a local storage device, to
one or more remote servers via SCP, or to a Google Cloud Storage bucket.
Results are saved as individual files in JSON new line format (.jsonl).
"""
__version__ = "0.1.0"
