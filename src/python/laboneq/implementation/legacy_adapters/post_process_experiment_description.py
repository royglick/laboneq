# Copyright 2023 Zurich Instruments AG
# SPDX-License-Identifier: Apache-2.0

from laboneq.data.experiment_description import Experiment, PlayPulse

PULSES = {}


def post_process(source, target, conversion_function_lookup: dict):
    global PULSES

    # todo(Pol): replace both of these by Pulse?

    if type(target) is Experiment:
        target.pulses = list(PULSES.values())
        PULSES = {}
        return target
    elif type(target) is PlayPulse:
        if source.pulse is not None:
            if source.pulse.uid not in PULSES:
                PULSES[source.pulse.uid] = conversion_function_lookup.get(
                    type(source.pulse)
                )(source.pulse)
            target.pulse = PULSES[source.pulse.uid]
        target.signal = source.signal

    return target
