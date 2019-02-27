'''
Some nonsense to experiment with a Pololu Mini Maestro 18 and a T Pro SG90
servo. The Pololu needed to be set to "USB Dual Port" serial mode in the
"Maestro Control Center" software, and the minimum and maximum in "Channel
Settings" needed to be changed: I used 64 and 4080, which were as low and high
of values as it would accept.

The Pololu was connected via USB, and the stepper power rail was attached to a
bench supply set to 5V.

--jnm, jeffreylevine, clindsa1 20180125
'''
import time
import maestro
servo = maestro.Controller()
# Just tried to figure out the range empirically...
# Apparently the units are "the pulse width in of [sic] quarter-microseconds"
# (see https://github.com/FRC4564/Maestro/blob/3154bfb2b433d945b0d9a0ef7bfe262ac48b357f/maestro.py#L78)
# These values move about 180 degrees, without making nasty popping noises at
# the extrema
maybe_min = 1980
maybe_max = 10500
servo.setTarget(0, maybe_min)
servo.setTarget(0, maybe_max)
