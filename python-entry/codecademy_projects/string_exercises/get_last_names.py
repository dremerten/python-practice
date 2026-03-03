authors = "Audre Lorde,Gabriela Mistral,Jean Toomer,An Qi,Walt Whitman,Shel Silverstein,Carmen Boullosa,Kamala Suraiyya,Langston Hughes,Adrienne Rich,Nikki Giovanni"


def get_last_names(str):
  author_names = authors.split(",")
  author_last_names = [name.split()[-1] for name in author_names]
  return author_last_names


result = get_last_names(authors)
print("")
print(f"Last names are: {result}\n")