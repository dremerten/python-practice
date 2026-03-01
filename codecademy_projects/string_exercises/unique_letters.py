letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
# Write your unique_english_letters function here:
def unique_english_letters(word):
  unique_letters = 0
  for letter in letters:
    if letter in word:
      unique_letters += 1
  return f"Your word has {unique_letters} unique letters!"

print(unique_english_letters("mississippi"))