def username_generator(first_name, last_name):
  password = first_name[:3] + last_name[:4]
  if len(first_name) <= 3 or len(last_name) <= 4:
    password = f"{first_name} {last_name}"
    return password
  else:
    return password

#result = username_generator("Abe","Simpson")
#print(result)

def password_generator(user_name):
    password = ""
    length = len(user_name)
    
    for i in range(length):
        password += user_name[i - 1]
    
    return password

def tell_me_about_icecream(favorite_icecream):
  response = "My favorite icecream is" + " " + favorite_icecream + "."
  print(response)

tell_me_about_icecream("chocolate")

# user_name = "AbeSimp"
# result = password_generator(user_name)
# print(result)