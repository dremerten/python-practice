def painting(paint_colors, picture):
  painting_statement = "To paint the " + picture + " we need the following colors: "
  print(painting_statement)
  for color in paint_colors:
      print(color)
  print(locals())
painting(['Saffron', 'White', 'Green'], 'Indian Flag')