"""
This module contains the Thing wrapper, used for accessing tests via WebThings.
"""
from webthing import Property, Thing, Value


class MurakamiThing(Thing):
    """
    This class wraps a (Web)Thing instance that includes properties for all test
    runners.

    ####Arguments
    * `runners`: a List of MurakamiRunner instances passed from MurakamiServer
    """
    def __init__(self, runners):
        super().__init__(
            id_="https://github.com/throneless-tech/murakami",
            title="Murakami",
            type_=["NetworkTest"],
            description="The M-Lab Murakami network measurement tap.",
        )

        for runner in runners:
            self.add_property(
                Property(
                    self,
                    "" + runner.title + "_onoff",
                    Value(runner.enabled, runner.set_enabled),
                    metadata={
                        "@type": "OnOffProperty",
                        "id": runner.title + "on",
                        "title": runner.title,
                        "type": "boolean",
                        "description": runner.description,
                    },
                ))
