"__Written By, S.SoltaniMoghadam__IIEES,Teh,2016"

import numpy as np
import os
from NordicReader import Read_Nordic as rn
import pylab as plt
from matplotlib import rcParams
from obspy.imaging.beachball import beach
import matplotlib.gridspec as gridspec
from matplotlib.widgets import CheckButtons

plt.rc('font',family='Times New Roman')
plt.style.use('ggplot')

rcParams['axes.labelsize'  ] = 15
rcParams['xtick.labelsize' ] = 13
rcParams['ytick.labelsize' ] = 13
rcParams['legend.fontsize' ] = 12

pid = 'path'

print ''
print '*****'.center(20," ")
print 20*'*'
print ' Nordic Plotter '.center(20,"*")
print 20*'*'
print '*****'.center(20," ")
print ''
print 'Short Key Usage in Map View:\n'
print 'Press c to clear map.'
print 'Press m to see more details.'
print 'Press a to save figure.\n'


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

for s in station_xyn:

    sta_dic[s[2]]=s[0],s[1]
    
#___________________SEC 02 Read Nordic file

inp = rn(inp_f) # Read Nordic file as a dic

event_dic = {}

for ev in sorted(inp.keys()):
    
    if ev not in sorted(event_dic.keys()):
        
        event_dic[ev] = {'evlon':None,'evlat':None,'evdep':None,'STA':{}}
        
    for hed in sorted(inp[ev]['Header']['L1'].keys()):
        
        event_dic[ev]['evlon'] = inp[ev]['Header']['L1']['Lon']
        event_dic[ev]['evlat'] = inp[ev]['Header']['L1']['Lat']
        event_dic[ev]['evdep'] = inp[ev]['Header']['L1']['Dep']
        
    for sta in sorted(inp[ev]['Pha_dat'].keys()):

        try:

            if sta not in sorted(event_dic[ev]['STA'].keys()):

                event_dic[ev]['STA'][sta]={'lon':None,'lat':None}
                event_dic[ev]['STA'][sta]['lon']=sta_dic[sta][0]
                event_dic[ev]['STA'][sta]['lat']=sta_dic[sta][1]

        except KeyError:
            
            print 'Warning! station %s not in STATION0.HYP.'%(sta)
            print ''
            
#___________________SEC 03 Plot event-station dist

st_x = [event_dic[i]['STA'][j]['lon'] for i in sorted(event_dic.keys()) for j in sorted(event_dic[i]['STA'].keys())]
st_y = [event_dic[i]['STA'][j]['lat'] for i in sorted(event_dic.keys()) for j in sorted(event_dic[i]['STA'].keys())]

ev_x = [event_dic[i]['evlon'] for i in sorted(event_dic.keys())]
ev_y = [event_dic[i]['evlat'] for i in sorted(event_dic.keys())]

#_________ SEC 03-01 Prepare to plot

fig = plt.figure(figsize=(16,10))
ax  = fig.add_subplot(111)
ax.set_xlabel('Longitude [deg]')
ax.set_ylabel('Latitude [deg]')
ax.plot(st_x,st_y,'^',ms=10,alpha=0.5,color='gray')
line, = ax.plot(ev_x,ev_y,'r*',ms=12, picker=5) # 5 points tolerance

#_________ SEC 03-02 Define a pick-event function

def func(label):
    if label == 'OK':
        print 111
    plt.draw()

def onpick(event):

    global tres
    global code
    global polr
    global stx_p
    global sty_p
    global xp
    global yp
    global event_id
    global evid
    global foc
    global mag
    global dep
    global xp
    global yp

    thispick = event.artist
    xdata    = thispick.get_xdata()
    ydata    = thispick.get_ydata()
    ind      = event.ind
    xp       = xdata[ind][0]
    yp       = ydata[ind][0]
    foc      = {}
    
    for evid in sorted(event_dic.keys()):

        if xp == event_dic[evid]['evlon'] and yp == event_dic[evid]['evlat']:

            stx_p    = [event_dic[evid]['STA'][s]['lon'] for s in sorted(event_dic[evid]['STA'].keys())]
            sty_p    = [event_dic[evid]['STA'][s]['lat'] for s in sorted(event_dic[evid]['STA'].keys())]
            code     = [s for s in sorted(event_dic[evid]['STA'].keys())]
            event_id = evid
            tres     = [inp[evid]['Pha_dat'][s]['TRES'] for s in sorted(inp[evid]['Pha_dat'].keys())]
            polr     = [inp[evid]['Pha_dat'][s]['POL']  for s in sorted(inp[evid]['Pha_dat'].keys())]
            mag      = inp[evid]['Header']['L1']['Mag1']
            dep      = inp[evid]['Header']['L1']['Dep']

            print 'Selected Event: %4s-%2s-%2sT%2s:%2s:%3s, Ml=%3s, Dep=%4s'%(event_id[0:4],event_id[4:6],
                                                                            event_id[6:8],event_id[8:10],
                                                                            event_id[10:12],event_id[12:],
                                                                            mag,dep)

            for p in ['FOCMEC','FPFIT','PINV']:

                if p in sorted(inp[event_id]['Header']['LF'].keys()):

                    foc[p] = inp[event_id]['Header']['LF'][p]

    ax.plot(xp,yp,'y*',ms=15)

    for i in range(len(stx_p)):
        
        ax.plot([xp,stx_p[i]],[yp,sty_p[i]],'b',ms=10)
        ax.text(stx_p[i],sty_p[i],code[i])

    fig.canvas.draw()

#_________ SEC 03-03 Define a press_key-event function
    
def press(event):

    global pid
    
    if event.key == 'c':

        pid = 'path'

        ax.cla()
        ax.set_xlabel('Longitude [deg]')
        ax.set_ylabel('Latitude [deg]')
        ax.plot(st_x,st_y,'^',ms=10,color='gray',alpha=0.5)
        line, = ax.plot(ev_x,ev_y,'r*', ms=12, picker=5) # 5 points tolerance
        ax.plot(xp,yp,'y*',ms=15)
        fig.canvas.draw()


    if event.key == 'm':

        pid = 'foc'

        fig_ = plt.figure(figsize=(16,10))
        ax_  = fig_.add_axes([0.1, 0.1, 0.8, 0.8])
        ax_.plot(xp,yp,'r*',ms=12)
        
        for i in range(len(stx_p)):

            ax_.text(stx_p[i],sty_p[i],code[i]+', '+str(polr[i]))
        
        ax_.set_title('Event ID: %4s-%2s-%2sT%2s:%2s:%4s, Ml=%3s, Dep=%4s'%(event_id[0:4],event_id[4:6],
                                                                            event_id[6:8],event_id[8:10],
                                                                            event_id[10:12],event_id[12:],
                                                                            mag,dep))
        cax  = ax_.scatter(stx_p, sty_p, c=tres, s=300, marker='^', vmin=-1.0, vmax=1.0)
        plt.colorbar(cax,label='Time Residual [sec]',pad=.01) 
        ax_.set_xlabel('Longitude [deg]')
        ax_.set_ylabel('Latitude [deg]')

        ax_f = fig_.add_axes([0.75, 0.1, 0.3, 0.8])
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
        
        plt.show()

        fig_.canvas.mpl_connect('key_press_event', press)

       
    if event.key == 'a':

        if not os.path.exists('outfig'):

            os.mkdir('outfig')

        plt.savefig(os.path.join('outfig',event_id+'_'+pid+'.png'),dpi=400)
        
fig.canvas.mpl_connect('pick_event', onpick)
fig.canvas.mpl_connect('key_press_event', press)



plt.show()
