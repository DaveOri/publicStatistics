# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd

GDP    = pd.read_csv('./nama_10_gdp/nama_10_gdp_1_Data.csv')
RDpubl = pd.read_csv('./gba_nabsfin07/gba_nabsfin07_1_Data.csv')
RDpriv = pd.read_csv('./rd_e_gerdtot/rd_e_gerdtot_1_Data.csv')

GDP.drop('Flag and Footnotes',axis=1,inplace=True)
RDpubl.drop('Flag and Footnotes',axis=1,inplace=True)
RDpriv.drop('Flag and Footnotes',axis=1,inplace=True)

GDP.replace('\s+', '',regex=True,inplace=True)
RDpubl.replace('\s+', '',regex=True,inplace=True)
RDpriv.replace('\s+', '',regex=True,inplace=True)
#GDP[GDP==':'] = 'nan'
#RDpubl[RDpubl==':'] = 'nan'
#RDpriv[RDpriv==':'] = 'nan'

RDpriv = RDpriv[RDpriv.SECTPERF == 'Allsectors']
RDpubl = RDpubl[RDpubl.NABS07 == 'TotalR&Dappropriations']

RDpubl = RDpubl[RDpubl.UNIT == 'Millioneuro']
RDpriv = RDpriv[RDpriv.UNIT == 'Millioneuro']
GDP = GDP[GDP.UNIT == 'Currentprices,millioneuro']

GEOpubl = RDpubl['GEO'].drop_duplicates()
GEOpriv = RDpriv['GEO'].drop_duplicates()
GEOgdp = GDP['GEO'].drop_duplicates()

GEOpubl = GEOpubl[GEOpubl.isin(GEOpriv)]
GEOpubl = GEOpubl[GEOpubl.isin(GEOgdp)]
GEOpriv = GEOpriv[GEOpriv.isin(GEOpubl)]
GEOpriv = GEOpriv[GEOpriv.isin(GEOgdp)]
GEOgdp = GEOgdp[GEOgdp.isin(GEOpubl)]
GEOgdp = GEOgdp[GEOgdp.isin(GEOpriv)]

def plot_rd_gdp(ax,rd,gdp,geo):
    rdgeo=rd[rd['GEO']==geo]
    gdpgeo=gdp[gdp['GEO']==geo]
    rdgeo.TIME=pd.to_numeric(rdgeo.TIME)
    gdpgeo.TIME=pd.to_numeric(gdpgeo.TIME)
    rdgeo.set_index('TIME',drop=True,inplace=True)
    gdpgeo.set_index('TIME',drop=True,inplace=True)
    rdgeo.Value=pd.to_numeric(rdgeo.Value,errors='coerce')
    gdpgeo.Value=pd.to_numeric(gdpgeo.Value,errors='coerce')
    rdgeo['gdp']=gdpgeo.Value[rdgeo.index]
    rdgeo['rd_per_gdp'] = 100.0*rdgeo.Value/rdgeo.gdp
    return rdgeo, gdpgeo
ax = 0
rdgerl, gdpg = plot_rd_gdp(ax,RDpubl,GDP,'Germany(until1990formerterritoryoftheFRG)')
rdital, gdpi = plot_rd_gdp(ax,RDpubl,GDP,'Italy')