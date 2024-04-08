import time
import threading
from multiprocessing import Process, Pipe, Value, Array


def count_items(esteira, delay, weight, item_count, item_weight, method, lock=None, conn=None):
    last_sent_time = time.time()  # comment to test without pipe
    while True:
        time.sleep(delay)
        item_count[esteira] += 1
        if method == "ipc":
            item_weight[esteira] += weight.value
            current_time = time.time()  # comment to test without pipe
            if current_time - last_sent_time >= 2 and sum(item_count) % 26 == 0:
                conn.send(sum(item_count))  # comment to test without pipe
                last_sent_time = current_time  # comment to test without pipe
        else:
            lock.acquire()
            item_weight[esteira] += weight
            lock.release()

        if sum(item_count) % 1500 == 0:
            print(f"Peso total de itens processados: {sum(item_weight)} Kg")


def display(pipe, item_count, lock=None):
    while True:
        time.sleep(2)
        if pipe:  # comment to test without pipe
            count = pipe.recv()  # comment to test without pipe
            print(f"Contagem total: {count}")  # comment to test without pipe
        else:  # comment to test without pipe
            if lock:  # in case to test without pipe
                lock.acquire()
            print(f"Contagem total: {sum(item_count)}")
            if lock:  # in case to test without pipe
                lock.release()


def main():
    method = input("Você quer usar Pthreads ou IPC? ")

    if method.lower() == "pthreads":
        lock = threading.Lock()

        item_count = [0, 0, 0]
        item_weight = [0.0, 0.0, 0.0]

        t1 = threading.Thread(target=count_items, args=(
            0, 1, 5.0, item_count, item_weight, method, lock))
        t2 = threading.Thread(target=count_items, args=(
            1, 0.5, 2.0, item_count, item_weight, method, lock))
        t3 = threading.Thread(target=count_items, args=(
            2, 0.1, 0.5, item_count, item_weight, method, lock))

        t1.start()
        t2.start()
        t3.start()

        t_display = threading.Thread(
            target=display, args=(None, item_count, lock))
        t_display.start()

        t1.join()
        t2.join()
        t3.join()
        t_display.join()

    elif method.lower() == "ipc":
        parent_conn, child_conn = Pipe()

        item_count = Array('i', [0, 0, 0])
        item_weight = Array('d', [0.0, 0.0, 0.0])

        p1 = Process(target=count_items, args=(
            0, 1, Value('d', 5.0), item_count, item_weight, method, None, child_conn))
        p2 = Process(target=count_items, args=(
            1, 0.5, Value('d', 2.0), item_count, item_weight, method, None, child_conn))
        p3 = Process(target=count_items, args=(
            2, 0.1, Value('d', 0.5), item_count, item_weight, method, None, child_conn))

        p1.start()
        p2.start()
        p3.start()

        p_display = Process(target=display, args=(parent_conn, item_count))
        p_display.start()

        p1.join()
        p2.join()
        p3.join()

        parent_conn.send(item_count[:])

        p_display.join()

    else:
        print("Método desconhecido.")


if __name__ == '__main__':
    main()
