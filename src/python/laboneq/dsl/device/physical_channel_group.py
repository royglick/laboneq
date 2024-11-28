# Copyright 2022 Zurich Instruments AG
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict

import laboneq.core.path as qct_path
from laboneq.core.utilities.dsl_dataclass_decorator import classformatter
from laboneq.dsl.calibration import Calibratable
from laboneq.dsl.device.io_units.physical_channel import PhysicalChannel


@classformatter
@dataclass
class PhysicalChannelGroup:
    #: Unique identifier.
    uid: str = field(default=None)

    #: The physical channels in this group.
    channels: Dict[str, PhysicalChannel] = field(default_factory=dict)

    def get_calibration(self):
        """Retrieve the calibration of the physical channel group."""
        calibration = dict()
        for channel in self.channels.values():
            calibration[channel.path] = (
                channel.calibration if channel.is_calibrated() else None
            )

        return calibration

    def reset_calibration(self):
        """Reset the calibration on all the logical signals of the group."""
        for channel in self.channels.values():
            assert isinstance(channel, Calibratable)
            channel.reset_calibration()

    def list_calibratables(self):
        return {
            signal.path: signal.create_info()
            for signal in self.channels.values()
            if isinstance(signal, Calibratable)
        }

    @property
    def path(self):
        return qct_path.PhysicalChannelGroups_Path_Abs + qct_path.Separator + self.uid
