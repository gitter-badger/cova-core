echo $PPID > computer_logs.txt
port=5100
for value in {1..6}
do
    python computer.py $port &
    echo $! >> computer_logs.txt
    ((port++))
done

