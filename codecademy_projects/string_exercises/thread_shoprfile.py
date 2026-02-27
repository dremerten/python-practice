PATH = ""

def read_sales(path: str):
    try:
        with open(path, 'r') as file:
            daily_sales = file.read()  # string
            daily_sales = daily_sales.replace(";,;", "|")  # string
            daily_sales_split = daily_sales.split(",")  # list
            transactions = []
            for index in daily_sales_split:
                transactions.append(index.split("|"))
            
            transactions_clean = [
                [item.replace("\n", "").strip(" ") for item in transaction] 
                for transaction in transactions
            ]

            customers = [index[0] for index in transactions_clean]
            sales = [index[1] for index in transactions_clean]
            thread_sold = [index[2] for index in transactions_clean]

            total_sales = 0
            for price in sales:
                total_sales += float(price.strip("$"))

            thread_sold_split = []
            for colors in thread_sold:
                if "&" in colors:
                    for color in colors.split("&"):
                        thread_sold_split.append(color)
                else:
                    thread_sold_split.append(colors)

            # list comprehension version
            #thread_sold_split = [color for colors in thread_sold for color in (colors.split("&") if "&" in colors else [colors])]

            # Define the color_count function outside of the loop
            def color_count(color):
                count = 0
                for item in thread_sold_split:
                    if item == color:
                        count += 1
                return count

            # List of colors to check for
            colors = ['red', 'yellow', 'green', 'white', 'black', 'blue', 'purple']
            
            # Loop over each color and print the count
            for color in colors:
                print(f"Thread Shed sold {color_count(color)} threads of {color} thread today")
            print("#" * 50)
            print(f"Total Sales for today were: ${total_sales:.2f}")

    except FileNotFoundError as e:
        raise FileNotFoundError(
            f"The file {path} cannot be found or does not exist"
        )

read_sales(PATH)