'''
defines and returns a function that takes two numeric arguments,length &  width. 
returns the volume given the input height

In the example, we wrote a higher-order function, make_box_volume_function(), 
that takes a height as an argument and returns a new function that calculates the volume 
of any box with that height when it is passed the length and width of the box. 
As we can see, higher-order functions with functions as return values are just as reusable as higher-order
functions with functions as arguments and, therefore, also reduce repetition 
and the chances for mistakes to creep into code.
'''
def make_box_volume_function(height):

    def volume(length, width):
        return length*width*height
    return volume
 
box_volume_height15 = make_box_volume_function(15)
print(box_volume_height15(3,2))