import multiprocessing
import os
import sys
import time
import importlib.util
from multiprocessing.managers import BaseManager
from queue import Queue
import queue
import threading
from multiprocessing import Pool
import socket

absolute_start=time.time()
hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)


class QueueManager(BaseManager):
    pass

QueueManager.register('get_job_queue')
QueueManager.register('get_result_queue')




def execute_job(job_path, directory):
    global ip, absolute_start
    # Obtenir l'ID du processus actuel pour identifier sur quel processeur le job est exécuté
    processor_id = multiprocessing.current_process().pid
    
    # Préparer le chemin du fichier où le résultat sera sauvegardé
    result_file_path = job_path.replace('.py', '.result')

    # Enregistrer le moment où le job commence à s'exécuter
    start_time = time.time()

    try:
        # Ajouter le répertoire 'modules' au chemin de recherche des modules si nécessaire
        modules_path = os.path.join(directory, "modules")
        sys.path.insert(0, modules_path)
        
        # Charger le module du job dynamiquement à partir du chemin du fichier
        spec = importlib.util.spec_from_file_location("job_module", job_path)
        job_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(job_module)
        
        # Exécuter la fonction 'run' du module du job et récupérer le résultat
        result = job_module.run()

        # Écrire le résultat dans un fichier correspondant au job
        with open(result_file_path, 'w') as result_file:
            result_file.write(str(result))

        # Calculer la durée d'exécution du job
        duration = time.time() - start_time

        # Renvoyer un message indiquant que le job a été exécuté avec succès, incluant la durée et le processeur utilisé
        return f"[{ip}] Job {job_path} terminé normalement sur le processeur {processor_id}. Start: {(start_time-absolute_start):.2f}. Durée totale: {duration:.2f} secondes\n"

    except Exception as e:
        # Si une exception est levée, l'écrire dans le fichier de résultat
        with open(result_file_path, 'w') as result_file:
            result_file.write(f"Exception: {str(e)}")

        # Calculer la durée jusqu'à l'exception
        duration = time.time() - start_time

        # Renvoyer un message indiquant que le job a échoué, incluant l'exception, la durée et le processeur utilisé
        return f"[{ip}] Job {job_path} a levé une exception sur le processeur {processor_id}. Start: {(start_time-absolute_start):.2f}. Durée totale: {duration:.2f} secondes\n"

def worker_start(server_ip, server_port, authkey, directory, n_processors=1):
    m = QueueManager(address=(server_ip, server_port), authkey=authkey)
    m.connect()
    
    print(f"Connected to server at {server_ip}:{server_port}")

    job_queue = m.get_job_queue()
    result_queue = m.get_result_queue()

    # while True:
    #     try:
    #         job_path = job_queue.get(timeout=1)
    #         # Exécuter le job en utilisant la fonction execute_job
    #         result = execute_job(job_path, directory)
    #         # Envoyer le résultat dans la file d'attente des résultats
    #         result_queue.put(result)
    #     except queue.Empty:
    #         print("No more jobs available.")
    #         break

    # Créer un pool de processus
    with Pool(n_processors) as pool:
        while True:
            try:
                jobs = []
                for _ in range(n_processors):  # Remplir le pool avec des jobs
                    try:
                        job_path = job_queue.get_nowait()
                        jobs.append((job_path, directory))
                    except queue.Empty:
                        break

                if not jobs:
                    break  # Aucun job disponible, sortir de la boucle

                results = pool.starmap(execute_job, jobs)
                for result in results:
                    result_queue.put(result)
            except Exception as e:
                print(f"Error processing jobs: {e}")

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python worker.py <server_ip> <server_port> <directory>")
        sys.exit(1)

    # Déterminer le nombre de processeurs à utiliser, en laissant un processeur libre pour les autres tâches du système
    n_processors = multiprocessing.cpu_count() - 1




    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])  # Convertir le port en entier
    directory = sys.argv[3]
    worker_start(server_ip, server_port, b'secretkey', directory, n_processors)

