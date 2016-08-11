"__Written By, S.SoltaniMoghadam__IIEES,Teh,2016"
"""
Notes:

1- Reading S Phase IS NOT Implemented in This Version.
2- It just read line types 1,2,F and the other lines
   will be ignored 
"""
#___________________ Define Nordic Type Line:

line_1 = {'F1':   {'col':(0,1),    'fmt':'%1s'    ,'v':None},          'YEAR': {'col':(1,5),    'fmt':'%00004d','v':None},
          'F2':   {'col':(5,6),    'fmt':'%1s'    ,'v':None},          'Month':{'col':(6,8),    'fmt':'%002d'  ,'v':None},
          'Day':  {'col':(8,10),   'fmt':'%002d'  ,'v':None},          'FO':   {'col':(10,11),  'fmt':'%1s'    ,'v':None},
          'Hour': {'col':(11,13),  'fmt':'%002d'  ,'v':None},          'Min':  {'col':(13,15),  'fmt':'%002d'  ,'v':None},
          'F3':   {'col':(15,16),  'fmt':'%1s'    ,'v':None},          'Sec':  {'col':(16,20),  'fmt':'%4.1f'  ,'v':None},
          'LMI':  {'col':(20,21),  'fmt':'%1s'    ,'v':None},          'DI':   {'col':(21,22),  'fmt':'%1s'    ,'v':None},
          'EID':  {'col':(22,23),  'fmt':'%1s'    ,'v':None},          'Lat':  {'col':(23,30),  'fmt':'%7.3f'  ,'v':None},
          'Lon':  {'col':(30,38),  'fmt':'%8.3f'  ,'v':None},          'Dep':  {'col':(38,43),  'fmt':'%5.1f'  ,'v':None},
          'DepI': {'col':(43,44),  'fmt':'%1s'    ,'v':None},          'LocI': {'col':(44,45),  'fmt':'%1s'    ,'v':None},
          'AGC':  {'col':(45,48),  'fmt':'%3s'    ,'v':None},          'NumS': {'col':(48,51),  'fmt':'%002d'  ,'v':None},
          'RMS':  {'col':(51,55),  'fmt':'%4.1f'  ,'v':None},          'Mag1': {'col':(55,59),  'fmt':'%4.1f'  ,'v':None},
          'TMag1':{'col':(59,60),  'fmt':'%1s'    ,'v':None},          'MAGC1':{'col':(61,63),  'fmt':'%3s'    ,'v':None},
          'Mag2': {'col':(63,67),  'fmt':'%4.1f'  ,'v':None},          'TMag2':{'col':(67,68),  'fmt':'%1s'    ,'v':None},
          'MAGC2':{'col':(68,71),  'fmt':'%3s'    ,'v':None},          'MAG3': {'col':(71,75),  'fmt':'%4.1f'  ,'v':None},
          'TMag3':{'col':(75,76),  'fmt':'%1s'    ,'v':None},          'MAGC3':{'col':(76,79),  'fmt':'%3s'    ,'v':None},
          'TL'  : {'col':(79,80),  'fmt':'%1s'    ,'v':None}}

line_4 = {'F1':  {'col':(0,1),     'fmt':'%1s'    ,'v':None},          'STA':  {'col':(1,6),    'fmt':'%5s'    ,'v':None},
          'INST': {'col':(6,7),    'fmt':'%1s'    ,'v':None},          'COMP':{'col':(7,8),     'fmt':'%1s'    ,'v':None},
          'W':    {'col':(8,9),    'fmt':'%1s'    ,'v':None},          'QLTI':{'col':(9,10),    'fmt':'%1s'    ,'v':None},
          'PH':   {'col':(10,14),  'fmt':'%4s'    ,'v':None},          'WI':  {'col':(14,15),   'fmt':'%1s'    ,'v':None},
          'F2':   {'col':(15,16),  'fmt':'%1s'    ,'v':None},          'POL': {'col':(16,17),   'fmt':'%1s'    ,'v':None},
          'Hour': {'col':(18,20),  'fmt':'%002d'  ,'v':None},          'Min': {'col':(20,22),   'fmt':'%002d'  ,'v':None},
          'Sec':  {'col':(22,28),  'fmt':'%6.0f'  ,'v':None},          'F3':  {'col':(28,29),   'fmt':'%1sf'   ,'v':None},
          'DTN':  {'col':(29,33),  'fmt':'%4d'    ,'v':None},          'AMP': {'col':(33,40),   'fmt':'%7.1f'  ,'v':None},
          'F4':   {'col':(40,41),  'fmt':'%1s'    ,'v':None},          'PER': {'col':(41,45),   'fmt':'%4.0f'  ,'v':None},
          'F5':   {'col':(45,46),  'fmt':'%1s'    ,'v':None},          'DOA': {'col':(46,51),   'fmt':'%5.0f'  ,'v':None},
          'F6':   {'col':(51,52),  'fmt':'%1s'    ,'v':None},          'PVEL':{'col':(52,56),   'fmt':'%4.0f'  ,'v':None},
          'ANGI': {'col':(56,60),  'fmt':'%4.0f'  ,'v':None},          'ARES':{'col':(60,63),   'fmt':'%3d'    ,'v':None},
          'TRES': {'col':(63,68),  'fmt':'%5.1f'  ,'v':None},          'WI2': {'col':(68,70),   'fmt':'%2d'    ,'v':None},
          'AZ':   {'col':(76,79),  'fmt':'%3d'    ,'v':None},          'TL':  {'col':(79,80),   'fmt':'%1s'    ,'v':None}}

line_F = {'STR':  {'col':(0,10),   'fmt':'%10.0f' ,'v':None},          'DIP': {'col':(10,20),   'fmt':'%10.0f' ,'v':None},
          'RAK':  {'col':(20,30),  'fmt':'%10.0f' ,'v':None},          'EHST':{'col':(30,35),   'fmt':'%5.1f'  ,'v':None},
          'EHD':  {'col':(35,40),  'fmt':'%5.1f'  ,'v':None},          'EHR': {'col':(40,45),   'fmt':'%5.1f'  ,'v':None},
          'EF1':  {'col':(45,50),  'fmt':'%5.1f'  ,'v':None},          'EF2': {'col':(50,55),   'fmt':'%5.1f'  ,'v':None},
          'AMR':  {'col':(55,60),  'fmt':'%5.1f'  ,'v':None},          'NBP': {'col':(60,65),   'fmt':'%2d'    ,'v':None},
          'AGC':  {'col':(66,69),  'fmt':'%3s'    ,'v':None},          'PRO': {'col':(70,77),   'fmt':'%7s'    ,'v':None},
          'QUA':  {'col':(77,78),  'fmt':'%1s'    ,'v':None}}
 

def Read_Nordic(inp='select.out'):

    """
    A python tool for readin seisan nordic format.
    input: select.out or any nordic file
    output: a dictionary containing the followings key/val:

    out_dic:
            Event_ID_dic:
                        Station_dic:
                                    key:val [ex: 'Lat':54.43]
    """

    nor_dic = {}
    
    with open(inp) as f:

        flag_l4 = False
        flag_l1 = True

        #__________ Sec 01 Read Line Type 1:

        for l in f:

            if l[79:80] == '1' and flag_l1:

                flag_l4 = False
                flag_l1 = False

                EID = '%4d%002d%002d%002d%002d%4.1f'%(float(l[1:5]), float(l[6:8]), float(l[8:10]),
                                                  float(l[11:13]), float(l[13:15]), float(l[16:20]))
                nor_dic[EID] = {}
                nor_dic[EID]['Header'] = {}
                nor_dic[EID]['Header']['L1'] = {}
                nor_dic[EID]['Header']['LF'] = {}
                nor_dic[EID]['Pha_dat'] = {}
                
                for i in sorted(line_1.keys()):

                    a,b = line_1[i]['col']

                    if l[a:b].strip():

                        u = l[a:b]

                        if '.' in u:

                            u = float(u.strip())

                        elif u.strip().isdigit():

                            u = int(u.strip())

                        else:

                            u = u.strip()
                    else:

                        u = None

                    nor_dic[EID]['Header']['L1'][i] = u

        #__________ Sec 02 Read Line Type F:

            if l[79:80] == 'F':

                for p in ['FOCMEC','FPFIT','PINV']:

                    if p in l[70:77]:

                        nor_dic[EID]['Header']['LF'][p] = {}

                        for k in sorted(line_F.keys()):

                            a,b = line_F[k]['col']

                            if l[a:b].strip():

                                z = l[a:b]

                                if '.' in z:

                                    z = float(z.strip())

                                elif z.strip().isdigit():

                                    z = int(z.strip())

                                else:

                                    z = z.strip()
                            else:

                                z = None

                            nor_dic[EID]['Header']['LF'][p][k] = z

                    

        #__________ Sec 03 Read Line Type 2:

            if l[1:5] == 'STAT':

                flag_l4 = True

            if l[1:5] == '    ':

                flag_l4 == False

            if flag_l4 and l[1:5] != 'STAT':

                flag_l1 = True

                s = l[1:5].strip()

                if s and s not in nor_dic[EID]['Pha_dat'].keys():

                    nor_dic[EID]['Pha_dat'][s] = {}

                    for j in sorted(line_4.keys()):

                        a,b = line_4[j]['col']

                        if l[a:b].strip():

                            v = l[a:b]

                            if '.' in v:

                                v = float(v.strip())
                        
                            elif v.strip().isdigit():

                                v = int(v.strip()) 

                            else:

                                v = v.strip()

                        else:

                            v = None

                        nor_dic[EID]['Pha_dat'][s][j] = v
    return nor_dic
