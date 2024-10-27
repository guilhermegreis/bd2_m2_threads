import threading
import time
import random

class Recurso:
    def __init__(self, nome):
        self.nome = nome
        self.lock = threading.Lock()

class Transacao(threading.Thread):
    def __init__(self, id, recurso1, recurso2, timestamp):
        super().__init__()
        self.id = id
        self.recurso1 = recurso1
        self.recurso2 = recurso2
        self.timestamp = timestamp

    def run(self):
        print(f"Thread {self.id} iniciando.")
        while True:
            if self.adquirir_recursos():
                print(f"Thread {self.id} obtém {self.recurso1.nome} e {self.recurso2.nome}.")
                time.sleep(random.uniform(1, 3))
                self.liberar_recursos()
                print(f"Thread {self.id} finalizou.")
                break
            else:
                print(f"Thread {self.id} aguardando recursos.")
                time.sleep(random.uniform(0.5, 1.5))

    def adquirir_recursos(self):
        if self.recurso1.lock.acquire(timeout=1):
            print(f"Thread {self.id} bloqueou {self.recurso1.nome}.")
            if self.recurso2.lock.acquire(timeout=1):
                print(f"Thread {self.id} bloqueou {self.recurso2.nome}.")
                return True
            else:
                self.recurso1.lock.release()
                print(f"Thread {self.id} liberou {self.recurso1.nome} devido a deadlock.")
        return False

    def liberar_recursos(self):
        self.recurso1.lock.release()
        self.recurso2.lock.release()
        print(f"Thread {self.id} liberou {self.recurso1.nome} e {self.recurso2.nome}.")

def main():
    recurso_X = Recurso("Recurso X")
    recurso_Y = Recurso("Recurso Y")

    threads = []
    for i in range(5):
        timestamp = time.time()
        t = Transacao(i, recurso_X, recurso_Y, timestamp)
        threads.append(t)
        time.sleep(random.uniform(0.1, 0.5))
        t.start()

    for t in threads:
        t.join()

    print("Todas as threads finalizaram.")

if __name__ == "__main__":
    main()
