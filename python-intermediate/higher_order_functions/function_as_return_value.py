'''
defines and returns a function that takes two numeric arguments,length &  width. 
returns the volume given the input height
'''
def make_box_volume_function(height):

    def volume(length, width):
        return length*width*height
    return volume
 
box_volume_height15 = make_box_volume_function(15)
print(box_volume_height15(3,2))