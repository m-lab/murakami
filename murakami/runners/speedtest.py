from __future__ import division, print_function
from webthing import (Action, Event, MultipleThings, Property, Thing, Value, WebThingServer)

import logging
import time
import tornado.ioloop
import uuid

class RunSpeedtest(Action):

  def __init__(self, thing, input_):
    Action.__init__(self, uuid.uuid4().hex, thing, 'run', input_=input_)

  def perform_action(self):
    # set properties; ex:
    # time.sleep(self.input['duration'] / 1000)
    # self.thing.set_property('brightness', self.input['brightness'])
    # self.thing.add_event(OverheatedEvent(self.thing, 102))

class SpeedtestClient(Thing):
  """Run Speedtest.net tests."""

  def __init__(self):
    Thing.__init__(
      self,
      'urn:dev:ops:ndt7-client',
      'Speedtest Client',
      ['OnOffSwitch', 'Client'],
      'A client running Speedtest tests'
    )

    self.add_property(
      Property(self,
        'on',
        Value(True, lambda v: print('On-State is now', v)),
        metadata={
          '@type': 'OnOffProperty',
          'title': 'On/Off',
          'type': 'boolean',
          'description': 'Whether the client is running',
        }))

    self.add_available_action(
      'run',
      {
        'title': 'Run',
        'description': 'Run tests',
        'input': {
          'type': 'object',
          'required': [
            'download',
            'upload'
          ],
          'properties': {
            'download': {
              'type': 'integer',
              'minimum': 0,
              'unit': 'Mbit/s',
            },
            'upload': {
              'type': 'integer',
              'minimum': 0,
              'unit': 'Mbit/s',
            },
          },
        },
      },
      RunNdt7)

    self.add_available_event(
      'error',
      {
        'description':
        'There was an error running the tests',
        'type': 'string',
        'unit': 'error',
      })
