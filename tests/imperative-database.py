import seamless
seamless.database_cache.connect()
seamless.database_sink.connect()


from seamless.imperative import transformer

@transformer
def func(a, b):
    return 100 * a + b

result = func(88, 17) # takes 0.5 sec
print(result)
result = func(88, 17) # immediate
print(result)
result = func(21, 17) # immediate
print(result)

@transformer
def func2(a, b):
    @transformer
    def func(a, b):
        return 100 * a + b
    
    return func(a, b) + func(b, a)

result = func2(12, 18)
print(result)

# transformer within transformer within transformer...

@transformer
def func3(a, b):
    @transformer
    def func2(a, b):
        @transformer
        def func(a, b):
            return 100 * a + b
        return func(a,b)

    return func2(a, b) + func2(b, a)

result = func3(12, 18)
print(result)

result = func3(10, 12)
print(result)