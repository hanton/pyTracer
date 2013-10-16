import sys, time
from Scene import Scene

if __name__ == '__main__':
    start_time = time.time()
    
    if len(sys.argv) < 3:
        width  = 640
        height = 320
    else:
        width = int(sys.argv[1])
        height = int(sys.argv[2])
    
    s = Scene()
    s.build(width, height)
    s.camera.render(s)

    end_time = time.time()
    print "Render Time: " + str(int(end_time - start_time)) + " seconds."
