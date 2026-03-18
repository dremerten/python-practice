import csv

with open('1kSalesRec.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # skip header

    # count Belgium rows
    count_belgiums = sum(1 for row in reader if row[1] == "Belgium")
    print(count_belgiums)

    # reset file
    csvfile.seek(0)
    reader = csv.reader(csvfile)
    next(reader)

    # average for Portugal
    values = (float(row[13]) for row in reader if row[1] == "Portugal")
    total, count = 0, 0
    for v in values:
        total += v
        count += 1

    avg_portugal = total / count if count else 0
    print(avg_portugal)