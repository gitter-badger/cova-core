echo $PPID > router_logs.txt
port=5000
for value in {1..5}
do
    python router.py $port &
    echo $! >> router_logs.txt
    ((port++))
done

