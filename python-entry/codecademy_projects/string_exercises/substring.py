def substring_between_letters(word, start, end):
  start_ind = word.find(start)
  end_ind = word.find(end)
  if start_ind > -1 and end_ind > -1:
    breakpoint()
    return(word[start_ind+1:end_ind])
  return word

print(substring_between_letters("apple", "p", "e"))