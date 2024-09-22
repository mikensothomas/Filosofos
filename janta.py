import threading
import time

# Número de filósofos e garfos
NUM_FILOSOFOS = 5

# Semáforos para os garfos (1 semáforo por garfo)
garfos = [threading.Semaphore(1) for _ in range(NUM_FILOSOFOS)]

# Bloqueio global para controlar a alternância entre os grupos de filósofos
mutex = threading.Lock()

# Tempos fixos para comer e pensar
tempo_de_comer = 20  # Tempo de comer para todos os filósofos (em segundos)
tempo_de_pensar = 20  # Tempo de pensar para todos os filósofos (em segundos)

# Controle para saber quais filósofos podem comer
# Apenas 2 filósofos podem comer ao mesmo tempo
grupo_comendo = [0, 1]  # Começamos com os filósofos 0 e 1 comendo

# Função para alternar o grupo que pode comer
def alternar_grupo():
    global grupo_comendo
    # Primeiro grupo: filósofos 0 e 1
    if grupo_comendo == [0, 1]:
        grupo_comendo = [2, 3]  # Agora 2 e 3 podem comer
    elif grupo_comendo == [2, 3]:
        grupo_comendo = [4, 0]  # Agora filósofo 4 e filósofo 0 podem comer
    elif grupo_comendo == [4, 0]:
        grupo_comendo = [1, 2]  # Agora filósofo 1 e filósofo 2 podem comer

# Filósofo representa cada thread
def filosofo(posicao):
    global grupo_comendo
    while True:
        print(f"Filósofo {posicao} está pensando.")
        time.sleep(tempo_de_pensar)  # Todos os filósofos pensam por 3 segundos

        # Agora o filósofo está com fome e quer comer
        while True:
            with mutex:
                if posicao in grupo_comendo:
                    break

        # print(f"Filósofo {posicao} está com fome.")

        # Tentar pegar os dois garfos (da esquerda e da direita)
        garfo_esquerdo = garfos[posicao]
        garfo_direito = garfos[(posicao + 1) % NUM_FILOSOFOS]

        # Adquirir os dois garfos
        garfo_esquerdo.acquire()
        garfo_direito.acquire()

        # Come por um tempo fixo
        print(f"Filósofo {posicao} está comendo.")
        time.sleep(tempo_de_comer)

        # Largar os garfos depois de comer
        garfo_esquerdo.release()
        garfo_direito.release()

        print(f"Filósofo {posicao} terminou de comer e voltou a pensar.")

        # Após comer, bloquear para alterar o grupo de filósofos com permissão para comer
        with mutex:
            alternar_grupo()

# Inicializar e iniciar as threads para os filósofos
threads = []
for i in range(NUM_FILOSOFOS):
    thread = threading.Thread(target=filosofo, args=(i,))
    threads.append(thread)
    thread.start()

# Manter as threads rodando
for thread in threads:
    thread.join()
