import threading
import queue
import os

buffer_size = 5

lock = threading.Lock()
queue = queue.Queue(buffer_size)
file_count = 0

def producer(top_dir, queue_buffer):
    # Search sub-dir in top_dir and put them in queue 找目錄
    files = os.listdir(top_dir)
    queue_buffer.put(top_dir,timeout = 2)
    for f in files:
        file_path = os.path.join(top_dir,f)
        if os.path.isdir(file_path): #recursive
            producer(file_path,queue)
    
def consumer(queue_buffer):
    # search file in directory 找檔案
    global path
    global file_count
    try:
        path = queue_buffer.get(timeout = 3)
    except:
        return
    paths = os.listdir(path)
    for p in paths:
        temp_path = os.path.join(path,p)
        if os.path.isfile(temp_path):
            lock.acquire()
            lock.release()
            file_count += 1

def main():
    producer_thread = threading.Thread(target = producer, args = ('./testdata', queue))

    consumer_count = 20
    consumers = []
    for i in range(consumer_count):
        consumers.append(threading.Thread(target = consumer, args = (queue,)))

    producer_thread.start()
    for c in consumers:
        c.start()

    producer_thread.join()
    for c in consumers:
        c.join()

    print(file_count, 'files found.')

if __name__ == "__main__":
    main()
