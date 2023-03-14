# timekeeping

import time
start = time.time()
_timepoint = 0
def t():
    global _timepoint
    _timepoint += 1
    return 'Timepoint {:d}, time {:.1f}'.format(_timepoint, time.time() - start)

# /timekeeping

from rprod import transformer

@transformer
def func(a, b):
    import time
    time.sleep(1)
    return 100 * a + b

result = func(88, 17)  # takes 1+ sec
print(t(), result)
result = func(88, 17)  # immediate
print(t(), result)

@transformer
def func2(a, b):
    
    @transformer
    def func(a, b):
        import time
        time.sleep(1)
        return 100 * a + b

    return func(a, b) + func(b, a)


result = func2(12, 18) # takes 2+ sec
print(t(), result)
result = func2(12, 18) # immediate
print(t(), result)
result = func2(17, 88) # takes 1+ sec
print(t(), result)
result = func2(17, 88) # immediate
print(t(), result)

# transformer within transformer within transformer...


@transformer
def func3(a, b):
    
    @transformer
    def func2(a, b):
    
        @transformer
        def func(a, b):
            import time
            time.sleep(1)            
            return 100 * a + b

        return func(a, b)

    return func2(a, b) + func2(b, a)


result = func3(23, 18) # takes 2+ sec
print(t(), result)

result = func3(18, 23) # near immediate
print(t(), result)

result = func3(88, 17) # a few tenths of a second
print(t(), result)
