filename="computer_logs.txt"
while read -r line
do
    kill $line
done < "$filename"

filename="router_logs.txt"
while read -r line
do
    kill $line
done < "$filename"

filename="data_user_logs.txt"
while read -r line
do
    kill $line
done < "$filename"

rm Log/*

rm Code/*

touch Code/__init__.py