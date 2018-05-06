
def square(x):
    return(x*x)

my_list = [1,2,3,4]
result = map(square, my_list )

for r in result:
    print(r)


my_func = lambda x: x*x
result = map(my_func,my_list)
for r in result:
    print(r)


def is_value(d):

    try:

        if d["name"]=="pablo":
            return True
        else:
            return False

    except:

        return False
    


my_list = [{"name":"pablo", "age":42}, {"name":"jose", "age":25} ]
print(my_list)

result = filter(is_value, my_list)
for r in result:
    print(r)






