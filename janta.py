import threading
import time

NUM_FILOSOFOS = 5

garfos = [threading.Semaphore(1) for _ in range(NUM_FILOSOFOS)]

bloqueio = threading.Lock()

tempo_de_comer = 4
tempo_de_pensar = 4

grupo_comendo = [0, 1]

def alternar_grupo():
    global grupo_comendo

    if grupo_comendo == [0, 1]:
        grupo_comendo = [2, 3]
    elif grupo_comendo == [2, 3]:
        grupo_comendo = [4, 0]
    elif grupo_comendo == [4, 0]:
        grupo_comendo = [1, 2]

def filosofo(posicao):
    global grupo_comendo
    while True:
        print(f"Filósofo {posicao} está pensando.")
        time.sleep(tempo_de_pensar)

        while True:
            with bloqueio:
                if posicao in grupo_comendo:
                    break

        print("....................................................................................................")
        print("\n")

        garfo_esquerdo = garfos[posicao]
        garfo_direito = garfos[(posicao + 1) % NUM_FILOSOFOS]

        garfo_esquerdo.acquire()
        garfo_direito.acquire()
        print(f"Filósofo {posicao} pegou o garfo da esquerda (garfo {posicao}) e o garfo da direita (garfo {(posicao + 1) % NUM_FILOSOFOS})")

        print(f"Filósofo {posicao} está comendo.")
        time.sleep(tempo_de_comer)

        print(f"Filósofo {posicao} terminou de comer e voltou a pensar.")

        garfo_esquerdo.release()
        garfo_direito.release()

        with bloqueio:
            alternar_grupo()

threads = []
for i in range(NUM_FILOSOFOS):
    thread = threading.Thread(target=filosofo, args=(i,))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()
