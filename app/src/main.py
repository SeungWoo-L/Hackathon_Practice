# Copyright (c) 2022 Robert Bosch GmbH and Microsoft Corporation
#
# This program and the accompanying materials are made available under the
# terms of the Apache License, Version 2.0 which is available at
# https://www.apache.org/licenses/LICENSE-2.0.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#
# SPDX-License-Identifier: Apache-2.0

"""A sample skeleton vehicle app."""

import asyncio
import json
import logging
import signal

from vehicle import Vehicle, vehicle  # type: ignore
from velocitas_sdk.util.log import (  # type: ignore
    get_opentelemetry_log_factory,
    get_opentelemetry_log_format,
)
from velocitas_sdk.vdb.reply import DataPointReply
from velocitas_sdk.vehicle_app import VehicleApp, subscribe_topic

# Configure the VehicleApp logger with the necessary log config and level.
logging.setLogRecordFactory(get_opentelemetry_log_factory())
logging.basicConfig(format=get_opentelemetry_log_format())
logging.getLogger().setLevel("DEBUG")
logger = logging.getLogger(__name__)

GET_SPEED_REQUEST_TOPIC = "sampleapp/getSpeed"
GET_SPEED_RESPONSE_TOPIC = "sampleapp/getSpeed/response"
CURRENT_SPEED_TOPIC = "sampleapp/currentSpeed"

GET_AMAIRTEMP_REQUEST_TOPIC = "sampleapp/getAmAirTemp"
GET_AMAIRTEMP_RESPONSE_TOPIC = "sampleapp/getAmAirTemp/response"
CURRENT_AMAIRTEMP_TOPIC = "sampleapp/currentAmAirTemp"

GET_EXAIRTEMP_REQUEST_TOPIC = "sampleapp/getExAirTemp"
GET_EXAIRTEMP_RESPONSE_TOPIC = "sampleapp/getExAirTemp/response"
CURRENT_EXAIRTEMP_TOPIC = "sampleapp/currentExAirTemp"

SET_HVACR1LTEMP_REQUEST_TOPIC = "sampleapp/setHVACR1LTemp"
SET_HVACR1LTEMP_RESPONSE_TOPIC = "sampleapp/setHVACR1LTemp/response"
SET_HVACR1LTEMP_SUBSCRIPTION_TOPIC = "sampleapp/currentHVACR1LTemp"

SET_HVACR1RTEMP_REQUEST_TOPIC = "sampleapp/setHVACR1RTemp"
SET_HVACR1RTEMP_RESPONSE_TOPIC = "sampleapp/setHVACR1RTemp/response"
SET_HVACR1RTEMP_SUBSCRIPTION_TOPIC = "sampleapp/currentHVACR1RTemp"

SET_HVACR2LTEMP_REQUEST_TOPIC = "sampleapp/setHVACR2LTemp"
SET_HVACR2LTEMP_RESPONSE_TOPIC = "sampleapp/setHVACR2LTemp/response"
SET_HVACR2LTEMP_SUBSCRIPTION_TOPIC = "sampleapp/currentHVACR2LTemp"

SET_HVACR2RTEMP_REQUEST_TOPIC = "sampleapp/setHVACR2RTemp"
SET_HVACR2RTEMP_RESPONSE_TOPIC = "sampleapp/setHVACR2RTemp/response"
SET_HVACR2RTEMP_SUBSCRIPTION_TOPIC = "sampleapp/currentHVACR2RTemp"

SET_HVACR3LTEMP_REQUEST_TOPIC = "sampleapp/setHVACR3LTemp"
SET_HVACR3LTEMP_RESPONSE_TOPIC = "sampleapp/setHVACR3LTemp/response"
SET_HVACR3LTEMP_SUBSCRIPTION_TOPIC = "sampleapp/currentHVACR3LTemp"

SET_HVACR3RTEMP_REQUEST_TOPIC = "sampleapp/setHVACR3RTemp"
SET_HVACR3RTEMP_RESPONSE_TOPIC = "sampleapp/setHVACR3RTemp/response"
SET_HVACR3RTEMP_SUBSCRIPTION_TOPIC = "sampleapp/currentHVACR3RTemp"

SET_HVACR4LTEMP_REQUEST_TOPIC = "sampleapp/setHVACR4LTemp"
SET_HVACR4LTEMP_RESPONSE_TOPIC = "sampleapp/setHVACR4LTemp/response"
SET_HVACR4LTEMP_SUBSCRIPTION_TOPIC = "sampleapp/currentHVACR4LTemp"

SET_HVACR4RTEMP_REQUEST_TOPIC = "sampleapp/setHVACR4RTemp"
SET_HVACR4RTEMP_RESPONSE_TOPIC = "sampleapp/setHVACR4RTemp/response"
SET_HVACR4RTEMP_SUBSCRIPTION_TOPIC = "sampleapp/currentHVACR4RTemp"

SET_HVACR1LFAN_REQUEST_TOPIC = "sampleapp/setHVACR1LFan"
SET_HVACR1LFAN_RESPONSE_TOPIC = "sampleapp/setHVACR1LFan/response"
SET_HVACR1LFAN_SUBSCRIPTION_TOPIC = "sampleapp/currentHVACR1LFan"

SET_HVACR1RFAN_REQUEST_TOPIC = "sampleapp/setHVACR1RFan"
SET_HVACR1RFAN_RESPONSE_TOPIC = "sampleapp/setHVACR1RFan/response"
SET_HVACR1RFAN_SUBSCRIPTION_TOPIC = "sampleapp/currentHVACR1RFan"

SET_HVACR2LFAN_REQUEST_TOPIC = "sampleapp/setHVACR2LFan"
SET_HVACR2LFAN_RESPONSE_TOPIC = "sampleapp/setHVACR2LFan/response"
SET_HVACR2LFAN_SUBSCRIPTION_TOPIC = "sampleapp/currentHVACR2LFan"

SET_HVACR2RFAN_REQUEST_TOPIC = "sampleapp/setHVACR2RFan"
SET_HVACR2RFAN_RESPONSE_TOPIC = "sampleapp/setHVACR2RFan/response"
SET_HVACR2RFAN_SUBSCRIPTION_TOPIC = "sampleapp/currentHVACR2RFan"

SET_HVACR3LFAN_REQUEST_TOPIC = "sampleapp/setHVACR3LFan"
SET_HVACR3LFAN_RESPONSE_TOPIC = "sampleapp/setHVACR3LFan/response"
SET_HVACR3LFAN_SUBSCRIPTION_TOPIC = "sampleapp/currentHVACR3LFan"

SET_HVACR3RFAN_REQUEST_TOPIC = "sampleapp/setHVACR3RFan"
SET_HVACR3RFAN_RESPONSE_TOPIC = "sampleapp/setHVACR3RFan/response"
SET_HVACR3RFAN_SUBSCRIPTION_TOPIC = "sampleapp/currentHVACR3RFan"

SET_HVACR4LFAN_REQUEST_TOPIC = "sampleapp/setHVACR4LFan"
SET_HVACR4LFAN_RESPONSE_TOPIC = "sampleapp/setHVACR4LFan/response"
SET_HVACR4LFAN_SUBSCRIPTION_TOPIC = "sampleapp/currentHVACR4LFan"

SET_HVACR4RFAN_REQUEST_TOPIC = "sampleapp/setHVACR4RFan"
SET_HVACR4RFAN_RESPONSE_TOPIC = "sampleapp/setHVACR4RFan/response"
SET_HVACR4RFAN_SUBSCRIPTION_TOPIC = "sampleapp/currentHVACR4RFan"


class SampleApp(VehicleApp):
    """
    Sample skeleton vehicle app.

    The skeleton subscribes to a getSpeed MQTT topic
    to listen for incoming requests to get
    the current vehicle speed and publishes it to
    a response topic.

    It also subcribes to the VehicleDataBroker
    directly for updates of the
    Vehicle.Speed signal and publishes this
    information via another specific MQTT topic
    """

    def __init__(self, vehicle_client: Vehicle):
        # SampleApp inherits from VehicleApp.
        super().__init__()
        self.Vehicle = vehicle_client

    async def on_start(self):
        """Run when the vehicle app starts"""
        # This method will be called by the SDK when the connection to the
        # Vehicle DataBroker is ready.
        # Here you can subscribe for the Vehicle Signals update (e.g. Vehicle Speed).
        await self.Vehicle.Speed.subscribe(self.on_speed_change)
        await self.Vehicle.Cabin.HVAC.AmbientAirTemperature.subscribe(self.am_air_temp)
        await self.Vehicle.Exterior.AirTemperature.subscribe(self.ex_air_temp)

    async def on_speed_change(self, data: DataPointReply):
        """The on_speed_change callback, this will be executed when receiving a new
        vehicle signal updates."""
        # Get the current vehicle speed value from the received DatapointReply.
        # The DatapointReply containes the values of all subscribed DataPoints of
        # the same callback.
        current_vehicle_speed = data.get(self.Vehicle.Speed).value

        # Do anything with the received value.
        # Example:
        # - Publishes current speed to MQTT Topic (i.e. DATABROKER_SUBSCRIPTION_TOPIC).
        await self.publish_event(
            CURRENT_SPEED_TOPIC,
            json.dumps({"speed": current_vehicle_speed}),
        )

    @subscribe_topic(GET_SPEED_REQUEST_TOPIC)
    async def am_air_temp(self, data: DataPointReply):
        am_air_temp = data.get(self.Vehicle.Cabin.HVAC.AmbientAirTemperature).value

        await self.publish_event(
            CURRENT_AMAIRTEMP_TOPIC,
            json.dumps({"Ambient_Air_Temp": am_air_temp}),
        )

    @subscribe_topic(GET_AMAIRTEMP_REQUEST_TOPIC)
    async def ex_air_temp(self, data: DataPointReply):
        ex_air_temp = data.get(self.Vehicle.Exterior.AirTemperature).value

        await self.publish_event(
            CURRENT_EXAIRTEMP_TOPIC,
            json.dumps({"Exterior_Air_Temp": ex_air_temp}),
        )

    @subscribe_topic(GET_EXAIRTEMP_REQUEST_TOPIC)
    async def on_get_speed_request_received(self, data: str) -> None:
        """The subscribe_topic annotation is used to subscribe for incoming
        PubSub events, e.g. MQTT event for GET_SPEED_REQUEST_TOPIC.
        """

        # Use the logger with the preferred log level (e.g. debug, info, error, etc)
        logger.debug(
            "PubSub event for the Topic: %s -> is received with the data: %s",
            GET_SPEED_REQUEST_TOPIC,
            data,
        )

        # Getting current speed from VehicleDataBroker using the DataPoint getter.
        current_vehicle_speed = (await self.Vehicle.Speed.get()).value

        # Do anything with the speed value.
        # Example:
        # - Publishes the vehicle speed to MQTT topic (i.e. GET_SPEED_RESPONSE_TOPIC).
        await self.publish_event(
            GET_SPEED_RESPONSE_TOPIC,
            json.dumps(
                {
                    "result": {
                        "status": 0,
                        "message": f"""Current Speed = {current_vehicle_speed}""",
                    },
                }
            ),
        )

    async def control_fan_speed(self, target_temperature: int):
        cabin_teamp = (await self.Vehicle.Cabin.HVAC.AmbientAirTemperature.get()).value
        cabin_temp_differ = cabin_teamp - target_temperature

        temp_differ_low = 10
        temp_differ_high = 10

        if cabin_temp_differ < 0:
            await self.set_fan_speed_all_seat(0)
        else:
            if cabin_temp_differ > 0 and cabin_temp_differ < temp_differ_low:
                await self.set_fan_speed_all_seat(5)

            elif cabin_temp_differ > 0 and cabin_temp_differ >= temp_differ_high:
                await self.set_fan_speed_all_seat(10)

    async def set_fan_speed_all_seat(self, fan_speed: int):

        await self.Vehicle.Cabin.HVAC.Station.Row1.Left.FanSpeed.set(fan_speed)
        await self.Vehicle.Cabin.HVAC.Station.Row1.Right.FanSpeed.set(fan_speed)
        await self.Vehicle.Cabin.HVAC.Station.Row2.Left.FanSpeed.set(fan_speed)
        await self.Vehicle.Cabin.HVAC.Station.Row2.Right.FanSpeed.set(fan_speed)
        await self.Vehicle.Cabin.HVAC.Station.Row3.Left.FanSpeed.set(fan_speed)
        await self.Vehicle.Cabin.HVAC.Station.Row3.Right.FanSpeed.set(fan_speed)
        await self.Vehicle.Cabin.HVAC.Station.Row4.Left.FanSpeed.set(fan_speed)
        await self.Vehicle.Cabin.HVAC.Station.Row4.Right.FanSpeed.set(fan_speed)

    async def get_user_input(self):
        while True:
            try:
                target_temperature = int(input("input temperature (or 'Q' to quit): "))
                return target_temperature
            except ValueError:
                if input("Do you want to quit? (Y/N): ").lower() == "y":
                    return None
                else:
                    continue

    async def main(self):
        logger.info("Starting SampleApp...")
        await self.run()

        while True:
            target_temperature = await self.get_user_input()
            if target_temperature is None:
                break

            await self.control_fan_speed(target_temperature)


LOOP = asyncio.get_event_loop()
app = SampleApp(vehicle)
LOOP.add_signal_handler(signal.SIGTERM, LOOP.stop)
LOOP.run_until_complete(app.main())
LOOP.close()
