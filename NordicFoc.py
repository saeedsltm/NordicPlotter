"__Written By, S.SoltaniMoghadam__IIEES,Teh,2016"

import numpy as np
import os
from NordicReader import Read_Nordic as rn
import pylab as plt
from matplotlib import rcParams
from obspy.imaging.beachball import beach
import matplotlib.gridspec as gridspec
from matplotlib.widgets import CheckButtons
from matplotlib import ticker
from matplotlib.widgets import CheckButtons

plt.rc('font',family='Times New Roman')
plt.style.use('ggplot')

rcParams['axes.labelsize'  ] = 15
rcParams['xtick.labelsize' ] = 13
rcParams['ytick.labelsize' ] = 13
rcParams['legend.fontsize' ] = 12

if not os.path.exists('report'):
    os.mkdir('report')
    os.path.exists(os.path.join('report','psmeca.out'))

#__________________SEC 01 Prepare inputs

if not os.path.exists('STATION0.HYP'):

    print 'Warning! No STATION0.HYP was found in current directorty.\n'
    
inp_f = raw_input('Input Nordic file name: ')

print ''

seigmt_inp = file('seigmt.inp','w')
seigmt_inp.write(inp_f+'\n')
seigmt_inp.write('\n')
seigmt_inp.write('1\n')
seigmt_inp.close()
os.system('seigmt < seigmt.inp')

for f in ['gmtdays.out','gmttime.out','gmtxy.out','gmtpath.out',
          'maxmag.out', 'psmeca.out', 'seigmt.inp','gmtxyz.out']:

    os.remove(f)
    
station_xyn = np.genfromtxt('gmtstxy.out',dtype={'names':('lon','lat','code'),'formats':('f2','f2','S5')})
sta_dic     = {}
   
#___________________SEC 02 Read Nordic file & station information

inp = rn(inp_f) 
for s in station_xyn: sta_dic[s[2]]=s[0],s[1]

#___________________SEC 03 Run Analyser

for ID in sorted(inp.keys()):

    header = inp[ID]['Header']
    data   = inp[ID]['Pha_dat']

    ot  = '-'.join([ID[0:4],ID[4:6],ID[6:8]])+' '+':'.join([ID[8:10],ID[10:12],ID[12:]])
    lat = header['L1']['Lat']
    lon = header['L1']['Lon']
    dep = header['L1']['Dep']
    mag = header['L1']['Mag1']

    if header['LF']: foc = header['LF']

    sta   = {}
    pol   = {}
    res_p = {}
    res_s = {} # Not Implemented in NordicReader yet.
    
    for s in data.keys():

        if s in sta_dic.keys() and 'P' in data[s]['PH'].upper():
            sta[s] = {'lat':sta_dic[s][1],'lon':sta_dic[s][0]}
        if 'P' in data[s]['PH'].upper():
            res_p[s] = data[s]['TRES']
        if 'S' in data[s]['PH'].upper():
            res_s[s] = data[s]['TRES']
        if 'POL' in data[s].keys():
            pol[s] = data[s]['POL']

    
    fig = plt.figure(figsize=(18,10))
    ax  = fig.add_axes([0.06, 0.1, 0.7, 0.8])
    plt.locator_params(axis='x',nbins=5)
    plt.locator_params(axis='y',nbins=5)
    
    # 1- plot event

    ax.plot(lon,lat,'*',color='red',ms=20)
    title = ' '.join(['OT='+ot,', Lon='+str(lon),', Lat='+str(lat),', Dep='+str(dep),', Mag='+str(mag)])
    ax.set_title(title)

    # 2-plot station with RES colored, polaritis and name
    
    sta_x = [sta[s]['lon'] for s in sorted(sta.keys())]
    sta_y = [sta[s]['lat'] for s in sorted(sta.keys())]
    sta_r = [res_p[s] for s in sorted(res_p.keys())]
    sta_n = sorted(sta.keys())
    cax   = ax.scatter(sta_x,sta_y,marker='^',c=sta_r,s=400,cmap=plt.cm.jet,vmin=-1.0,vmax=1.0)
    cb    = fig.colorbar(cax, fraction=0.015, pad=0.01)
    cb.set_label(label='Time Residual [sec]',size=12)
    for i in sta_n: t=i+', '+str(pol[i]); plt.text(sta[i]['lon'],sta[i]['lat'],t)
    tick_locator = ticker.MaxNLocator(nbins=5)
    cb.locator = tick_locator
    cb.update_ticks()


    # 3- focal mechanism

    ax_f = fig.add_axes([0.75, 0.1, 0.3, 0.8])
    offset = 20
           
    for p in foc.keys():
            
        fp  = [foc[p]['STR'],foc[p]['DIP'],foc[p]['RAK']]
        bch = beach(fp, xy=(0, offset), width=10, linewidth=0.5, size=200)
        ax_f.add_collection(bch)
        ax_f.set_aspect("equal")
        ax_f.text(-2,offset+6,p)

        offset-=20
            
    ax_f.set_xlim((-6, 6))
    ax_f.set_ylim((-30, 30))
    ax_f.get_xaxis().set_visible(False)
    ax_f.get_yaxis().set_visible(False)

    # 4- plot foc-select
    
    plt.style.use('grayscale')    
    rax = plt.axes([0.77, 0.10, 0.07, 0.15])
    check = CheckButtons(rax, ('FPFIT', 'PINV', 'FOCMEC'), (False, False, False))
    plt.style.use('ggplot')
    
    def func(label):

        for l in ['PINV','FPFIT', 'FOCMEC']:

            if label == l:

                f = open(os.path.join('report','psmeca.out'),'a')
                print lon,lat,dep,foc[label]['STR'],foc[label]['DIP'],foc[label]['RAK'],mag, lon, lat, label
                f.write('%6s %6s %4s %5s %5s %5s %4s %6s %6s %6s\n'%(lon,lat,dep,foc[label]['STR'],foc[label]['DIP'],foc[label]['RAK'],mag, lon, lat, label))
                f.close()

    check.on_clicked(func)

    plt.show()


