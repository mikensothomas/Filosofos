import threading
import time

NUM_FILOSOFOS = 5
tempo_de_comer = 4
tempo_de_pensar = 4

garfos = [threading.Semaphore(1) for _ in range(NUM_FILOSOFOS)]
bloqueio = threading.Lock()

grupo_comendo0 = [0, 2]
grupo_comendo1 = [1, 3]
grupo_comendo2 = [4, 2]

grupo_comendo = grupo_comendo0

def alternar_grupo():
    global grupo_comendo

    if grupo_comendo == grupo_comendo0:
        grupo_comendo = grupo_comendo1
    elif grupo_comendo == grupo_comendo1:
        grupo_comendo = grupo_comendo2
    elif grupo_comendo == grupo_comendo2:
        grupo_comendo = grupo_comendo0

def filosofo(posicao):
    global grupo_comendo
    while True:
        # print(f"Filósofo {posicao} está pensando.")
        time.sleep(tempo_de_pensar)

        while True:
            with bloqueio:
                if posicao in grupo_comendo:
                    break
           
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

        print(f"Filósofo {posicao} largou o garfo da esquerda (garfo {posicao}) e da direita (garfo {(posicao + 1) % NUM_FILOSOFOS})")

        with bloqueio:
            alternar_grupo()

threads = []
for i in range(NUM_FILOSOFOS):
    thread = threading.Thread(target=filosofo, args=(i,))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()