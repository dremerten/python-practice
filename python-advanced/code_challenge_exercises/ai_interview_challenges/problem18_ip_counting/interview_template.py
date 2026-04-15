"""
1. Import the JSON module along with basic file handling.
   - You will use it to format output for display, not for file writing.

2. Define a function that takes a file path as input.
   - Its job is to compute which IP appears the most and return both the IP and its count.

3. Inside the function, create a dictionary variable for counting.
   - It starts empty
   - As lines are processed, each IP becomes a key
   - Its value becomes the number of times that IP appears

4. Open the log file in read mode using a context manager.
   - Ensures proper file handling without manual closing.

5. Iterate through the file line by line.
   - Efficient for large files.

6. Clean each line before processing.
   - Strip whitespace
   - Skip empty lines immediately

7. Split each valid line into parts using whitespace.
   - Treat it as columns of data

8. Extract the first column.
   - This represents the IP address

9. Update the dictionary count for that IP.
   - Increment if it exists
   - Otherwise initialize it to 1

10. Finish processing all lines before moving forward.
    - Do not calculate the maximum inside the loop

11. After the loop, determine the IP with the highest count.
    - Use Python’s max() function on the dictionary
    - By default it looks at keys, so you must guide it to compare using the dictionary’s values
    - This will return the key (IP address) with the highest associated count

12. Once you have that IP, retrieve its count
    - Use the dictionary and that IP as the key to get its value

12. Retrieve the corresponding count from the dictionary.

13. Return the result in a structured format.
    - A dictionary with clear keys for IP and count

14. In the main execution block, call the function.
    - Use the full path: access.log

15. Store the returned result in a variable.

16. Open "highestip.txt" in write mode.

17. Write only the IP address into the file.


20. Ensure the final structure is clean:
    - function definition
    - dictionary setup
    - file loop
    - counting logic
    - max calculation
    - return result
    - main execution
    - write to file
    - optional JSON print

21. Avoid common mistakes:
    - Calculating the max before finishing the loop
    - Writing structured data to the output file instead of a plain IP
    - Using incorrect file paths
    - Accessing split data before validating the line
"""