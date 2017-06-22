import numpy as np
from random import randint
def compute_cp(a, b):
    t = (a+b)*(a+b+1)
    # print t
    return t/2 + b

def cantor_pair(patch):
    if(len(patch) == 2):
        return compute_cp(patch[0], patch[1])

    return compute_cp(patch[0], cantor_pair(patch[1:]))

def compute_hash(patch):
    # median = float(np.median(patch))
    # patch = np.divide(patch,median)
    # print patch
    patch_trunc = ["{0:.2f}".format(x) for x in patch]
    con = ''.join(patch_trunc)
    # print con
    cp = hash(con)
    return cp
#Takes an image of dimensions height*width
#and outputs a dictionary of pairing for each filter_window
def average_out(image, height, width, channels, filter_width, filter_height, d):
    num_x_patches = width - filter_width + 1
    num_y_patches = height - filter_height + 1
    for k in xrange(num_y_patches):
        for j in xrange(num_x_patches):
            x_start = j
            x_end = j + filter_width
            y_start = k
            y_end = k + filter_height
            # patch=[]
            for i in xrange(channels):
                patch = image[y_start:y_end,x_start:x_end,i]
                # patch = np.concatenate([patch, patch_t])
                # print patch
                # median = float(np.median(patch))
                # patch = np.divide(patch,median)
                # print patch
                # patch_trunc = ["{0:.4f}".format(x) for x in patch]
                # con = ''.join(patch_trunc)
                # print con
                cp = compute_hash(patch.flatten())
                if cp not in d:
                    d[cp] = 1
                else:
                    d[cp] += 1
    return d

def build_dict(images, batch_size, height, width, channels):
    d={}
    filter_width = 3
    filter_height = 3
    for i in xrange(batch_size):
        # print images[i]
        print np.amax(images[i]), np.amin(images[i])

        d = average_out(images[i], height, width, channels, filter_width, filter_height, d)
    for i in d:
        if d[i] > 20:
            print i, d[i]
    print len(d)
    return d

def test(images, batch_size):
    # print np.shape(images)
    build_dict(images, batch_size, 224, 224, 3)

def distort(split, filter_size):
    mini = -10
    for i in range(filter_size):
        for j in range(filter_size):
            if split[i,j] > mini:
                mini = split[i,j]
                maxi, maxj = i, j
    median = float(np.median(split))
    split[maxi, maxj] += 0.00001
    median = float(np.median(split))
    return split
def copy(a, b, images, channel, split1, filter_size):
    split = split1.copy()
    split = distort(split, filter_size)
    for i in xrange(filter_size):
        for j in xrange(filter_size):
            images[0,a+i,b+j, channel] = split[i,j]
    return images

def populate(n, split, filter_size, channels):
    dist = {}
    for i in range(len(split)): dist[i] = 0
    k = n/filter_size
    images = np.random.rand(1,n,n,channels)
    for c in range(channels):
        for i in range(k):
            for j in range(k):
                r = randint(0,len(split)-1)
                dist[r] += 1
                images = copy(i*filter_size, j*filter_size, images, c, split[r], filter_size)
    return dist, images

def test_experiment(n, num_k, channels):
    sample =[]
    for i in xrange(num_k):
        sample.append(np.random.rand(3,3))
    dist, images = populate(n, sample, 3, channels)
    d = build_dict(images, 1, n, n, channels)
    print "Expected Distribution\n", dist
    print "Actual Distribution\n", d
    for i in sample:
        hsh = compute_hash(i.flatten())
        print hsh

# test_experiment(6, 2, 2)
