import pysnooper

@pysnooper.snoop()
def do_something(x,y,z,a,b):
    q = x * z
    b = a + q
    return b

print(do_something(1,2,3,4,5))