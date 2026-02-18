print("I have information for the following planets:\n")

print("   1. Venus   2. Mars    3. Jupiter")
print("   4. Saturn  5. Uranus  6. Neptune\n")
 
weight = 185

planet_rg = {
    "Venus": 0.91, "Mars": 0.38,           
    "Jupiter": 2.34, "Saturn": 1.06, 
    "Uranus": 0.92, "Neptune": 1.19
    }


for k, v in planet_rg.items():
    planet = input("Please select a planet base on it number:  ")
    planet = int(planet)

    if planet not in range(1, 7):
        print(f"Must select a number between 1 - 6. You entered: {planet}! Please try again\n")
        continue

    if planet == 1:
        print(f"The planet's relative gravity for planet: Venus is {v}")
        break
    elif planet == 2:
        print(f"The planet's relative gravity for planet: Mars is {v}")
        break
    elif planet == 3:
        print(f"The planet's relative gravity for planet: Jupiter is {v}")
        break
    elif planet == 4:
        print(f"The planet's relative gravity for planet: Saturn is {v}")
        break
    elif planet == 5:
        print(f"The planet's relative gravity for planet: Uranus is {v}")
        break
    else:
        print(f"The planet's relative gravity for planet: Neptune is {v}")
        break
