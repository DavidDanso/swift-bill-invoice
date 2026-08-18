#!/bin/bash
echo "Today is " `date`

# echo -e "\nenter the path to directory"
# read the_path

# echo -e "\n you path has the following files and folders: "
# ls $the_path

# echo "What's your name?" 

# read entered_name 

# echo -e "\nWelcome to bash tutorial" $entered_name

# echo "Hello $1"

# echo "Hello, this is some text" > output.txt

# echo "More text" >> output.txt

# cat output.txt

# echo "Nice meeting you Mr $2"

# echo "Please enter a number: "
# read num

# if [ $num -gt 0 ]; then
#   echo "$num is positive"
# elif [ $num -lt 0 ]; then
#   echo "$num is negative"
# else
#   echo "$num is zero"
# fi

set -x 

if [ $? -ne 0 ]; then
    echo "Error occurred."
fi