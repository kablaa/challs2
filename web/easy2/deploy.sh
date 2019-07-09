docker build -t hidden_chall .
docker run -t -p 5001:80 --name hidden_chall --detach  hidden_chall
