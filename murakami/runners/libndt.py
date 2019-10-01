from __future__ import division, print_function
from webthing import Action, Event, Property, Thing, Value

import logging
import os
import time

# import tornado.ioloop
import uuid


class LibndtClient(Thing):
    """Run LibNDT tests."""
    def __init__(self):

        Thing.__init__(
            self,
            "urn:dev:ops:libndt-client",
            "LibNDT Client",
            ["OnOffSwitch", "Client"],
            "A client running LibNDT tests",
        )

        self.run_test()

        self.add_property(
            Property(
                self,
                "on",
                Value(True, lambda v: print("On-State is now", v)),
                metadata={
                    "@type": "OnOffProperty",
                    "title": "On/Off",
                    "type": "boolean",
                    "description": "Whether the client is running",
                },
            ))

        self.add_available_action(
            "run",
            {
                "title": "Run",
                "description": "Run tests",
                "input": {
                    "type": "object",
                    "required": ["download", "upload"],
                    "properties": {
                        "download": {
                            "type": "integer",
                            "minimum": 0,
                            "unit": "Mbit/s"
                        },
                        "upload": {
                            "type": "integer",
                            "minimum": 0,
                            "unit": "Mbit/s"
                        },
                    },
                },
            },
            RunLibndt,
        )

        self.add_available_event(
            "error",
            {
                "description": "There was an error running the tests",
                "type": "string",
                "unit": "error",
            },
        )

    def run_test(self):
        os.system("ctest -a --output-on-failure .")
