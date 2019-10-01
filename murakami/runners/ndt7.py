from __future__ import division, print_function
from webthing import Action, Event, Property, Thing, Value

import logging
import os
import time

# import tornado.ioloop
import uuid


class RunNdt7(Action):
    def __init__(self, thing, input_):

        Action.__init__(self, uuid.uuid4().hex, thing, "run", input_=input_)

    def perform_action(self):
        print("perform speedtest action")
        # set properties; ex:
        # time.sleep(self.input['duration'] / 1000)
        # self.thing.set_property('brightness', self.input['brightness'])
        # self.thing.add_event(OverheatedEvent(self.thing, 102))


class Ndt7Client(Thing):
    """Run NDT7 tests."""
    def __init__(self):

        Thing.__init__(
            self,
            "urn:dev:ops:ndt7-client",
            "NDT7 Client",
            ["OnOffSwitch", "Client"],
            "A client running NDT7 tests",
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
            RunNdt7,
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
        # TODO: make the path configurable.
        os.system("/murakami/bin/libndt-client -ndt7 -download -upload -batch")
