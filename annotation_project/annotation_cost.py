#!/usr/bin/env python3

import os

# Wanted annotations per person
agoal = int(os.environ.get('AGOAL', 400))

# Expected Annotations per hour
arate = int(os.environ.get('ARATE', 45))

# Paid Euros per hour
wage = int(os.environ.get('WAGE', 15))

# Fixed hours for tutorial plus guideline reading
fixtime = int(os.environ.get('FIXTIME', 1))

time = agoal / arate + fixtime
cost = time * wage

print('Annotation Goal: {} a'.format(agoal))
print('Annotation Rate: {} a/h'.format(arate))
print('Wage: €{}'.format(wage))
print('Fixtime: {} h'.format(fixtime))
print()
print('=>')
print()
print('Time: {:.2f} h'.format(time))
print('Cost: €{:.2f}'.format(cost))
