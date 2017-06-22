import sys
def find_map1(i):
    m ={0:"CUDNN_CONVOLUTION_FWD_ALGO_IMPLICIT_GEMM",
        1:"CUDNN_CONVOLUTION_FWD_ALGO_IMPLICIT_PRECOMP_GEMM",
        2:"CUDNN_CONVOLUTION_FWD_ALGO_GEMM",
        3:"CUDNN_CONVOLUTION_FWD_ALGO_DIRECT",
        4:"CUDNN_CONVOLUTION_FWD_ALGO_FFT",
        5:"CUDNN_CONVOLUTION_FWD_ALGO_FFT_TILING",
        6:"CUDNN_CONVOLUTION_FWD_ALGO_WINOGRAD",
        7:"CUDNN_CONVOLUTION_FWD_ALGO_WINOGRAD_NONFUSED"}
    return m[i]

def find_map2(i):
    m ={0:"CUDNN_CONVOLUTION_BWD_DATA_ALGO_0",
        1:"CUDNN_CONVOLUTION_BWD_DATA_ALGO_1",
        2:"CUDNN_CONVOLUTION_BWD_DATA_ALGO_FFT",
        3:"CUDNN_CONVOLUTION_BWD_DATA_ALGO_FFT_TILING",
        4:"CUDNN_CONVOLUTION_BWD_DATA_ALGO_WINOGRAD",
        5:"CUDNN_CONVOLUTION_BWD_DATA_ALGO_WINOGRAD_NONFUSED"}
    return m[i]

def find_map3(i):
    m ={0:"CUDNN_CONVOLUTION_BWD_FILTER_ALGO_0",
        1:"CUDNN_CONVOLUTION_BWD_FILTER_ALGO_1",
        2:"CUDNN_CONVOLUTION_BWD_FILTER_ALGO_FFT",
        3:"CUDNN_CONVOLUTION_BWD_FILTER_ALGO_3"}
    return m[i]

n = int(sys.argv[1])
m = int(sys.argv[2])
if n == 1:
    f = open('algo1', 'r')
    i = 1
    for lines in f:
        line = lines.split()
        algo = line[1]
        if algo <='9' and algo >='0':
            print "Convolution",i,"Algo:",find_map1(int(line[1]))
        else:
            print "Convolution",i,lines.strip()
        i += 1
elif n == 2:
    f = open('algo2', 'r')
    i = m
    for lines in f:
        line = lines.split()
        algo = line[1]
        if algo <='9' and algo >='0':
            print "BackPropData ",i,"Algo:",find_map2(int(line[1]))
        else:
            print "BackPropData",i,lines.strip()
        i -= 1
elif n == 3:
    f = open('algo3', 'r')
    i = m
    for lines in f:
        line = lines.split()
        algo = line[1]
        if algo <='9' and algo >='0':
            print "BackPropFilter",i,"Algo:",find_map3(int(line[1]))
        else:
            print "BackPropFilter",i,lines.strip()
        i -= 1
