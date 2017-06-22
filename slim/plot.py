import plotly.plotly as py
import plotly.figure_factory as ff
from datetime import datetime

def prepare_map():
    algo = {0:"algo_convolution",
            1:"algo_convolution_backprop_filter",
            2:"algo_convolution_backprop_data",
            }
    dlist=[]
    for i in xrange(3):
        d = {}
        f = open(algo[i], 'r')
        for lines in f:
            line = lines.split()
            d[line[1]] = line[3]
        dlist.append(d)
    return dlist

def is_convolution(ker):
    conv = "convolution:Conv2D"
    return ker.endswith(conv)

def is_backpropfilter(ker):
    conv = "/convolution_grad/Conv2DBackpropFilter:Conv2DBackpropFilter"
    return ker.endswith(conv)

def is_backpropdata(ker):
    conv = "/convolution_grad/Conv2DBackpropInput:Conv2DBackpropInput"
    return ker.endswith(conv)

def mod(ker, algo_map):
    if is_convolution(ker):
        i = (ker[:-19])[-1:]
        ker = "Convolution " + str(i) + " " +  algo_map[0][i]
    elif is_backpropfilter(ker):
        i = (ker[:-59])[-1:]
        ker = "BackPropFilter " + str(i) + " " + algo_map[1][i]
    elif is_backpropdata(ker):
        i = (ker[:-57])[-1:]
        ker = "BackPropData " + str(i) + " " + algo_map[2][i]
    return ker

def parse(f, algo_map):
    de={}
    min_start=10**20
    max_end = 0
    total = 0
    for lines in f:
        line = lines.split()
        ker = mod(line[0], algo_map)
        elapsed = float(line[1])
        start = float(line[2])
        end = float(line[3])
        min_start = min(min_start, start)
        max_end = max(max_end, end)
        total += elapsed
        if ker not in de:
            de[ker] = elapsed
        else:
            de[ker] += elapsed
    return min_start, max_end, total, de

def construct_dict(f, de, threshold, flag, algo_map):
    d={}
    for lines in f:
        line = lines.split()
        ker = mod(line[0], algo_map)
        start = float(line[2][9:18])
        end = float(line[3][9:18])
        if de[ker] > threshold:
            dt = datetime.fromtimestamp(start)
            start = dt.strftime('%Y-%m-%d %H:%M:%S')
            dt = datetime.fromtimestamp(end)
            end = dt.strftime('%Y-%m-%d %H:%M:%S')
            if flag == 1:
                print ker, de[ker], start, end, float(line[2][10:]), float(line[3][10:])
            # print ker, start, end
            if ker in d:
                d[ker].append([start, end])
            else:
                d[ker] = [[start, end]]
    return d

def add_entries(d, df, resource):
    for k in d:
        for j in d[k]:
            start = j[0]
            end = j[1]
            df.append(dict(Task=k, Start=start, Finish=end, Resource=resource))
    return df

algo_map = prepare_map()

f = open("ker_stats",'r')
min_start_k, max_end_k, total_k, dk = parse(f, algo_map)

f = open("mem_stats",'r')
min_start_m, max_end_m, total_m, dm = parse(f, algo_map)


print "Total Kernel Time: ", (max_end_k - min_start_k)/10**3
print "Total Mem Time: ", (max_end_m - min_start_m)/10**3
print "Total Time: ", total_k
print "Total Elapsed Time: ", (max(max_end_k, max_end_m) - min(min_start_k, min_start_m))/10**3

f = open("ker_stats",'r')
dk = construct_dict(f, dk, 4000.0, 0, algo_map)
f = open("mem_stats",'r')
dm = construct_dict(f, dm, 1000.0, 0, algo_map)

df = add_entries(dk, [], 'Kernel')
df = add_entries(dm, df, 'Memory')
colors = {'Memory': 'rgb(220, 0, 0)',
          'Kernel': 'rgb(0, 255, 100)'}
fig = ff.create_gantt(df, title='Tf Stats', index_col='Resource',
                      show_colorbar=True, bar_width=0.8, showgrid_x=True, showgrid_y=True, group_tasks=True)
py.plot(fig, filename='tf-hours', world_readable=True)
