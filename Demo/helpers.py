__author__ = 'Aleksander'



#pipes a value through a series of functions
def pipe(inital_value, functions):
    for function in functions:
        inital_value = function(inital_value)
    return inital_value

