import time

def move():
    start_time = time.time()

    while True:
        print("L")
        if time.time() - start_time >= 3:
            break
        
while True:
    move()
    print("Done")
    break