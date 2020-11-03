Inainte de rulare trebuie instalata libraria pycrypto cu comanda:
pip3 install pycrypto
https://pypi.org/project/pycrypto/

1. Rulam Key Manager-ul (care este si server) cu python, folosind comanda:
python3 key_manager.py
2. Rulam nodul B (care este tot server) cu python, folosind comanda:
python3 node_B.py 
3. Rulam nodul A (care este client atat pentru Key Manager cat si pentru nodul B) folosind comanda:
python3 node_a.py 

Se va transfera continutul din fisierul "node_B.py" din nodul A spre nodul B, unde este afisat in consola si este salvat intr-un fisier cu numele "received_by_nodeB.py"