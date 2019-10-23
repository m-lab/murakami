from datetime import datetime
import logging
import pkg_resources

from webthing import Property, Thing, Value

logger = logging.getLogger(__name__)


class MurakamiThing(Thing):
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
