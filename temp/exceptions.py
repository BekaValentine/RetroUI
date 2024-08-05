errors = {}
try:
    print(foo)
except Exception as e:
    errors['foo'] = e
try:
    print(bar)
except Exception as e:
    errors['bar'] = e


print(errors)
#raise errors['foo']

import inspect
for k, v in inspect.getmembers(errors['foo']):
  print(k, v)
