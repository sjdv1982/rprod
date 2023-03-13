import seamless

seamless.set_ncores(0)
from seamless import communion_server

seamless.database_sink.connect()
seamless.database_cache.connect()

communion_server.configure_master(
    transformation_job=True,
    transformation_status=True,
)

communion_server.start()

from rprod import transformer


@transformer
def func(a, b):
    import time

    time.sleep(0.5)
    return 100 * a + b


func.local = False

result = func(88, 17)  # takes 0.5 sec
print(result)
result = func(88, 17)  # immediate
print(result)
result = func(21, 17)  # takes 0.5 sec
print(result)

######################

from seamless.highlevel import Context

ctx = Context()

ctx.tf = func
ctx.tf.meta = {"local": False}
ctx.tf.a = 21
ctx.tf.b = 17
ctx.compute()
print(ctx.tf.logs)
print(ctx.tf.status)
print(ctx.tf.exception)
print(ctx.tf.result.value)
import sys

sys.exit(0)

seamless.set_ncores(8)


def func2(a, b):
    @transformer
    def func(a, b):
        import time

        time.sleep(2)
        return 100 * a + b

    func.local = False

    return func(a, b) + func(b, a)


ctx.tf = func2
ctx.tf.meta = {"local": True}
ctx.tf.a = 21
ctx.tf.b = 17
ctx.compute()
print(ctx.tf.logs)
print(ctx.tf.status)
print(ctx.tf.exception)
print(ctx.tf.result.value)

# transformer within transformer within transformer...


def func3(a, b):
    @transformer
    def func2b(a, b):
        @transformer
        def func(a, b):
            import time

            time.sleep(2)
            return 100 * a + b

        func.local = False
        return func(a, b)

    func2b.local = True

    return func2b(a, b) + func2b(b, a)


ctx.tf.code = func3
ctx.tf.meta = {"local": True}
ctx.compute()
print(ctx.tf.logs)
print(ctx.tf.status)
print(ctx.tf.result.value)

ctx.tf.a = 33
ctx.tf.b = 33
ctx.compute()
print(ctx.tf.logs)
print(ctx.tf.status)
print(ctx.tf.result.value)

ctx.tf.a = 7
ctx.tf.b = 22
ctx.compute()
print(ctx.tf.logs)
print(ctx.tf.status)
print(ctx.tf.result.value)
