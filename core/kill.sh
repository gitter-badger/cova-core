filename="router_processes.txt"
while read -r line
do
    kill $line
done < "$filename"

rm Log/*

curl localhost:5002/clear_all/d