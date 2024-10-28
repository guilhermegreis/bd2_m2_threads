#bibliotecas
import threading
import time
import random

#interromper com o Ctrl+C
parar_threads = False

#garantir o acesso ao recurso e espera
class Recurso:
    def __init__(self, nome):
        self.nome = nome
        self.lock = threading.Lock()

#competição por recursos, cada thread tem id e timestamp
class Transacao(threading.Thread):
    def __init__(self, id, recurso1, recurso2, timestamp):
        super().__init__()
        self.id = id
        self.recurso1 = recurso1
        self.recurso2 = recurso2
        self.timestamp = timestamp

    def run(self):
        print(f"Thread {self.id} iniciando com timestamp {self.timestamp}.")
        while not parar_threads:
            if self.adquirir_recursos():
                print(f"Thread {self.id} ganhou {self.recurso1.nome} e {self.recurso2.nome}.")
                time.sleep(random.uniform(1, 3))  #simula processamento
                self.liberar_recursos()
                print(f"Thread {self.id} finalizou.")
                break
            else:
                print(f"Thread {self.id} aguardando recursos.")
                time.sleep(random.uniform(0.5, 1.5))  #aguarda antes de tentar de novo

    def adquirir_recursos(self):
        #tenta adquirir o primeiro recurso usando o wait-die
        if self.tentativa_bloqueio(self.recurso1):
            if self.tentativa_bloqueio(self.recurso2):
                return True
            else:
                self.recurso1.lock.release()
                print(f"Thread {self.id} liberou {self.recurso1.nome} por deadlock.")
        return False

    def tentativa_bloqueio(self, recurso):
        if recurso.lock.acquire(timeout=1):
            print(f"Thread {self.id} bloqueou {recurso.nome}.")
            return True
        else:
            #verifica se tem uma thread mais antiga usando o wait-die
            for t in threading.enumerate():
                if isinstance(t, Transacao) and t.is_alive() and t.timestamp < self.timestamp:
                    print(f"Thread {self.id} morreu pelo wait-die.")
                    return False  #a thread morre qndo encontra uma mais antiga bloqueando
            return False

    def liberar_recursos(self):
        self.recurso1.lock.release()
        self.recurso2.lock.release()
        print(f"Thread {self.id} liberou {self.recurso1.nome} e {self.recurso2.nome}.")

def main():
    global parar_threads

    recurso_X = Recurso("Recurso X")
    recurso_Y = Recurso("Recurso Y")

    try:
        #loop até o usuário pressionar Ctrl+C
        while not parar_threads:
            threads = []
            #cria e inicia 5 threads em cada ciclo
            for i in range(5):
                timestamp = time.time()  #timestamp para cada thread
                t = Transacao(i, recurso_X, recurso_Y, timestamp)
                threads.append(t)
                time.sleep(random.uniform(0.1, 0.5))  #criação em tempos aleatórios
                t.start()

            #monitorar as threads até que todas terminem
            for t in threads:
                t.join(timeout=1)

    except KeyboardInterrupt:
        print("\nExecução interrompida pelo usuário.")
        parar_threads = True  #sinaliza pra todas as threads pararem

    print("Todas as threads finalizaram.")

if __name__ == "__main__":
    main()
