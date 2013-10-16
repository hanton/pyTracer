import sys, time
from Scene import Scene

if __name__ == '__main__':
    start_time = time.time()

    s = Scene()
    s.build()
    s.camera.render(s)

    end_time = time.time()
    print int(end_time - start_time)
