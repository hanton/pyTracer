import sys, time
from Scene import Scene

if __name__ == '__main__':
    start_time = time.time()
    
    if len(sys.argv) < 3:
        width   = 740
        height  = 740
        samples = 1
    else:
        width   = int(sys.argv[1])
        height  = int(sys.argv[2])
        samples = int(sys.argv[3])

    s = Scene()
    s.build(width, height, samples)
    s.camera.render(s)

    end_time = time.time()
    print "\r" + "Render Time: " + str(int(end_time - start_time)) + " seconds."
