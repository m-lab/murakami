from __future__ import division, print_function
from webthing import (Action, Event, MultipleThings, Property, Thing, Value, WebThingServer)

import logging
import time
import tornado.ioloop
import uuid

class RunAction(Action):

  def __init__(self, thing, input_):
    Action.__init__(self, uuid.uuid4().hex, thing, 'run', input_=input_)

  def perform_action(self):
    # set properties; ex:
    # time.sleep(self.input['duration'] / 1000)
    # self.thing.set_property('brightness', self.input['brightness'])
    # self.thing.add_event(OverheatedEvent(self.thing, 102))

class NDT7Runner(Thing):
  """Run tests using chosen build."""

  def __init__(self):
    Thing.__init__(
      self,
      # set context; ex:
      # 'urn:dev:ops:my-lamp-1234',
      # 'My Lamp',
      # ['OnOffSwitch', 'Light'],
      # 'A web connected lamp'
    )

    self.add_property(
      Property(self,
        'on',
        Value(True, lambda v: print('On-State is now', v)),
        metadata={
          '@type': 'OnOffProperty',
          'title': 'On/Off',
          'type': 'boolean',
          'description': 'Whether the runner is turned on',
        }))

    self.add_available_action(
      'run',
      {
        'title': 'Run',
        'description': 'Run tests',
        'input': {
          'type': 'object',
          'required': [
            # set these, ex:
            # 'brightness',
            # 'duration',
          ],
          'properties': {
            # set these, ex:
            # 'brightness': {
            #   'type': 'integer',
            #   'minimum': 0,
            #   'maximum': 100,
            #   'unit': 'percent',
            # },
            # 'duration': {
            #   'type': 'integer',
            #   'minimum': 1,
            #   'unit': 'milliseconds',
            # },
          },
        },
      },
      RunAction)

def run_server():
  # Create a thing that represents a device running ndt7
  ndt7runner = NDT7Runner()

  # If adding more than one thing, use MultipleThings() with a name.
  # In the single thing case, the thing's name will be broadcast.
  server = WebThingServer(MultipleThings([ndt7runner],'NDT7Device'), port=8888)
  try:
    logging.info('starting the server')
    server.start()
  except KeyboardInterrupt:
    logging.debug('canceling the sensor update looping task')
    sensor.cancel_update_level_task()
    logging.info('stopping the server')
    server.stop()
    logging.info('done')

if __name__ == '__main__':
  logging.basicConfig(
    level=10,
    format="%(asctime)s %(filename)s:%(lineno)s %(levelname)s %(message)s"
  )
  run_server()
