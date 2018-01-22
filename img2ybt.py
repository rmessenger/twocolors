###############################################################################
# Convert RGB Image(s) to Yellow-Blue-Time Animation
# by Robin Messenger
# 
# This script creates an small video clip from an image wherein
# red and green colors are represented using yellows and blues, and
# alternated with the actual yellows and blues in the image.
###############################################################################


import sys
import math
import numpy
import imageio


# Matricies
m_yb =    numpy.array([[0.5,0.5,0.0],
                       [0.5,0.5,0.0],
                       [0.0,0.0,1.0]])

m_rg_yb = numpy.array([[0.75,0.75,0],
                       [0.25,0.25,1],
                       [0  ,0   ,0]])


# Mixing function
def h(t,T):
    return math.sin(math.pi*t/T)**4

# Print usage
def usage():
    print("Usage: python img2ybt.py T N file1.jpg file2.png ...")
    print("    T ==> Period (seconds)")
    print("    N ==> Duration (number of periods)")


if len(sys.argv)<4:
    usage()
else:
    try:
        # Parse arguments
        T=float(sys.argv[1])
        N=int(sys.argv[2])
        if T<=0.0 or N<=0:
            raise ValueError

        # Go through each file...
        for img in sys.argv[3:]:
            print("Converting %s..." % (img))

            # Output filename
            outfn=img.split('.')
            if len(outfn)>1:
                outfn.pop(-1)
            outfn.append("mp4")
            outfn=".".join(outfn)

            try:
                # Import the image, RG-YB and YB versions
                im=imageio.imread(img)
                im=im.astype(float)
                im=im/256.0
                im_rg_yb=numpy.matmul(im,m_rg_yb)
                im_yb=numpy.matmul(im,m_yb)

                # Create an animation using the images and mixing function
                try:
                    with imageio.get_writer(outfn, fps=30) as f:
                        for t in numpy.arange(0,N*T,1.0/30.0):
                            frame_rotate=h(t,T)*im_rg_yb+(1-h(t,T))*im_yb
                            f.append_data(frame_rotate)
                except:
                    print("Error writing video file!")
            except:
                print("Error loading image!")
    except:
        usage()


