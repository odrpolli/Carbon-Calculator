# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 07:42:40 2024

@author: owenp
"""
#necessary modules
import tkinter as tk
import csv
from tkinter import messagebox, ttk
import math



class GUI:
    def __init__(self):
        
        #init window size, title, etc
        self.window=tk.Tk()
        self.window.state('zoomed')
        self.window.title("Carbon Calculator")
        self.summary=tk.Label(self.window,text='Carbon Footprint Calculator',font=("Arial",18,"bold","underline"))
        self.summary.pack(fill='x')
        
        #bottom credits
        self.credits=tk.Label(self.window,text='Dr. Moresoli and Owen Pollitt         Last Updated: 18/11/2024',font=("Arial",10))
        self.credits.pack(side='bottom')
        
        #set calculation results variable
        self.res=0
        
        #menu buttons (Cacluate and Export)
        self.menu_buttonframe=tk.Frame(self.window)
        self.menu_buttonframe.columnconfigure(0,weight=1)
        self.menu_buttonframe.columnconfigure(1,weight=1)
        
        self.btn=tk.Button(self.menu_buttonframe, text="Calculate",font=("Arial",18),command=self.calc)
        self.btn.grid(row=1,column=0,sticky="we",ipadx=5,ipady=5)
        
        self.exportbtn=tk.Button(self.menu_buttonframe, text="Export Results",font=("Arial",18),command=self.exportresults)
        self.exportbtn.grid(row=1,column=1,sticky="we",ipadx=5,ipady=5)
        
        self.restitle=tk.Label(self.menu_buttonframe,text='   Total mT CO2e:',font=("Arial",20))
        self.restitle.grid(row=1,column=4)
        self.calcres=tk.Label(self.menu_buttonframe,text=self.res,font=("Arial",20))
        self.calcres.grid(row=1, column=5)
        
        
        #electricity - province based
        
        self.input_provframe=tk.Frame(self.window)
        self.input_provframe.columnconfigure(0, weight=5)
        self.input_provframe.columnconfigure(1, weight=1)
        self.input_provframe.columnconfigure(2, weight=1)
        
        self.provtitle=tk.Label(self.input_provframe,text='Electricity - Large Variation Between Provinces',font=("Arial",15,"bold"))
        self.provtitle.grid(row=1,column=1)
        
        self.provlabel=tk.Label(self.input_provframe,text="Province", font=("Arial",20))
        self.provlabel.grid(row=2,column=1)
        
        self.prov=ttk.Combobox(self.input_provframe,state="readonly",values=['CDN AVG','NL','PE','NS','NB','QC','ON','MB','SK','AB','BC','YT','NT','NU'],)
        self.prov.grid(row=2,column=2)
        self.prov.current(0)
        
        self.sources(self.prov.get())
        
        self.E_val = tk.Label(self.input_provframe, text="Electricity (kWh)", font=("Arial", 20))
        self.E_val.grid(row=3, column=1)
        
        self.E_inp = tk.Entry(self.input_provframe,validate="key", validatecommand=(self.window.register(self.datavalidation), '%S'))
        self.E_inp.grid(row=3, column=2)
        
        self.E_conv = tk.Label(self.input_provframe, text='×'+str(self.round_sigfig(self.econv)), font=("Arial", 20))
        self.E_conv.grid(row=3, column=3)
        
        self.Eunit = tk.Label(self.input_provframe, text=self.eunit, font=("Arial", 20))
        self.Eunit.grid(row=3, column=4)
        
        
        
        #Other co2 emission sources (natural gas, gasoline, diesel, fuel oil, propane)
        
        self.input_buttonframe = tk.Frame(self.window)
        self.input_buttonframe.columnconfigure(0, weight=5)
        self.input_buttonframe.columnconfigure(1, weight=1)
        self.input_buttonframe.columnconfigure(2, weight=1)
        self.input_buttonframe.columnconfigure(3, weight=1)
        self.input_buttonframe.columnconfigure(4, weight=1)
        self.input_buttonframe.columnconfigure(5, weight=1)
        self.input_buttonframe.columnconfigure(6, weight=1)
        
        self.other_title = tk.Label(self.input_buttonframe, text="Other Energy Sources", font=("Arial", 15,"bold"))
        self.other_title.grid(row=1, column=1)
        self.D_val = tk.Label(self.input_buttonframe, text="Diesel (Gal)", font=("Arial", 20))
        self.D_val.grid(row=2, column=1)
        self.G_val = tk.Label(self.input_buttonframe, text="Gasoline (Gal)", font=("Arial", 20))
        self.G_val.grid(row=3, column=1)
        self.N_val = tk.Label(self.input_buttonframe, text="Natural Gas (Gal)", font=("Arial", 20))
        self.N_val.grid(row=4, column=1)
        self.P_val = tk.Label(self.input_buttonframe, text="Propane (Gal)", font=("Arial", 20))
        self.P_val.grid(row=5, column=1)
        self.F_val = tk.Label(self.input_buttonframe, text="Fuel Oil (Gal)", font=("Arial", 20))
        self.F_val.grid(row=6, column=1)
    
        
        self.D_inp = tk.Entry(self.input_buttonframe,validate="key", validatecommand=(self.window.register(self.datavalidation), '%S'))
        self.D_inp.grid(row=2, column=2)
        self.G_inp = tk.Entry(self.input_buttonframe,validate="key", validatecommand=(self.window.register(self.datavalidation), '%S'))
        self.G_inp.grid(row=3, column=2)
        self.N_inp = tk.Entry(self.input_buttonframe,validate="key", validatecommand=(self.window.register(self.datavalidation), '%S'))
        self.N_inp.grid(row=4, column=2)
        self.P_inp = tk.Entry(self.input_buttonframe,validate="key", validatecommand=(self.window.register(self.datavalidation), '%S'))
        self.P_inp.grid(row=5, column=2)
        self.F_inp = tk.Entry(self.input_buttonframe,validate="key", validatecommand=(self.window.register(self.datavalidation), '%S'))
        self.F_inp.grid(row=6, column=2)
        
        self.D_conv = tk.Label(self.input_buttonframe, text='×'+str(self.round_sigfig(self.dconv)), font=("Arial", 20))
        self.D_conv.grid(row=2, column=3)
        self.G_conv = tk.Label(self.input_buttonframe, text='×'+str(self.round_sigfig(self.gconv)), font=("Arial", 20))
        self.G_conv.grid(row=3, column=3)
        self.N_conv = tk.Label(self.input_buttonframe, text='×'+str(self.round_sigfig(self.ngconv)), font=("Arial", 20))
        self.N_conv.grid(row=4, column=3)
        self.P_conv = tk.Label(self.input_buttonframe, text='×'+str(self.round_sigfig(self.pconv)), font=("Arial", 20))
        self.P_conv.grid(row=5, column=3)
        self.F_conv = tk.Label(self.input_buttonframe, text='×'+str(self.round_sigfig(self.fconv)), font=("Arial", 20))
        self.F_conv.grid(row=6, column=3)
        
        self.Dunit = tk.Label(self.input_buttonframe, text=self.dunit, font=("Arial", 20))
        self.Dunit.grid(row=2, column=4)
        self.Gunit = tk.Label(self.input_buttonframe, text=self.gunit, font=("Arial", 20))
        self.Gunit.grid(row=3, column=4)
        self.Ngunit = tk.Label(self.input_buttonframe, text=self.ngunit, font=("Arial", 20))
        self.Ngunit.grid(row=4, column=4)
        self.Punit = tk.Label(self.input_buttonframe, text=self.punit, font=("Arial", 20))
        self.Punit.grid(row=5, column=4)
        self.Funit = tk.Label(self.input_buttonframe, text=self.funit, font=("Arial", 20))
        self.Funit.grid(row=6, column=4)
        
        
        
        
        
        
        
        #sources
        self.sources_buttonframe = tk.Frame(self.window)
        self.sources_buttonframe.columnconfigure(0, weight=5)
        self.sources_buttonframe.columnconfigure(1, weight=1)
        self.sources_buttonframe.columnconfigure(2, weight=1)
        self.sources_buttonframe.columnconfigure(3, weight=1)
        self.sources_buttonframe.columnconfigure(4, weight=1)
        self.sources_buttonframe.columnconfigure(5, weight=1)
        self.sources_buttonframe.columnconfigure(6, weight=1)
        
        self.provsourcetitle=tk.Label(self.sources_buttonframe,text="Province", font=('Arial',10))
        self.provsourcetitle.grid(row=1,column=1)
        self.provsource=tk.Label(self.sources_buttonframe,text=self.prov.get(), font=('Arial',10))
        self.provsource.grid(row=1,column=2)
        
        self.esourcelabel = tk.Label(self.sources_buttonframe, text="Electricity", font=("Arial", 10))
        self.esourcelabel.grid(row=2, column=1)
        self.gsourcelabel = tk.Label(self.sources_buttonframe, text="Gasoline", font=("Arial", 10))
        self.gsourcelabel.grid(row=4, column=1)
        self.ngsourcelabel = tk.Label(self.sources_buttonframe, text="Natural Gas", font=("Arial", 10))
        self.ngsourcelabel.grid(row=5, column=1)
        self.dsourcelabel = tk.Label(self.sources_buttonframe, text="Diesel", font=("Arial", 10))
        self.dsourcelabel.grid(row=3, column=1)
        self.psourcelabel = tk.Label(self.sources_buttonframe, text="Propane", font=("Arial", 10))
        self.psourcelabel.grid(row=6, column=1)
        self.fsourcelabel = tk.Label(self.sources_buttonframe, text="Fuel Oil", font=("Arial", 10))
        self.fsourcelabel.grid(row=7, column=1)
        
        self.Esource = tk.Label(self.sources_buttonframe, text=self.esource, font=("Arial", 10))
        self.Esource.grid(row=2, column=2)
        self.Gsource = tk.Label(self.sources_buttonframe, text=self.gsource, font=("Arial", 10))
        self.Gsource.grid(row=4, column=2)
        self.Ngsource = tk.Label(self.sources_buttonframe, text=self.ngsource, font=("Arial", 10))
        self.Ngsource.grid(row=5, column=2)
        self.Dsource = tk.Label(self.sources_buttonframe, text=self.dsource, font=("Arial", 10))
        self.Dsource.grid(row=3, column=2)
        self.Psource = tk.Label(self.sources_buttonframe, text=self.psource, font=("Arial", 10))
        self.Psource.grid(row=6, column=2)
        self.Fsource = tk.Label(self.sources_buttonframe, text=self.fsource, font=("Arial", 10))
        self.Fsource.grid(row=7, column=2)
        
        self.Edate = tk.Label(self.sources_buttonframe, text=self.edate, font=("Arial", 10))
        self.Edate.grid(row=2, column=3)
        self.Gdate = tk.Label(self.sources_buttonframe, text=self.gdate, font=("Arial", 10))
        self.Gdate.grid(row=4, column=3)
        self.Ngdate = tk.Label(self.sources_buttonframe, text=self.ngdate, font=("Arial", 10))
        self.Ngdate.grid(row=5, column=3)
        self.Ddate = tk.Label(self.sources_buttonframe, text=self.ddate, font=("Arial", 10))
        self.Ddate.grid(row=3, column=3)
        self.Pdate = tk.Label(self.sources_buttonframe, text=self.pdate, font=("Arial", 10))
        self.Pdate.grid(row=6, column=3)
        self.Fdate = tk.Label(self.sources_buttonframe, text=self.fdate, font=("Arial", 10))
        self.Fdate.grid(row=7, column=3)
        
        self.Enote = tk.Label(self.sources_buttonframe, text=self.enotes, font=("Arial", 10))
        self.Enote.grid(row=2, column=4)
        self.Gnote = tk.Label(self.sources_buttonframe, text=self.gnotes, font=("Arial", 10))
        self.Gnote.grid(row=4, column=4)
        self.Ngnote = tk.Label(self.sources_buttonframe, text=self.ngnotes, font=("Arial", 10))
        self.Ngnote.grid(row=5, column=4)
        self.Dnote = tk.Label(self.sources_buttonframe, text=self.dnotes, font=("Arial", 10))
        self.Dnote.grid(row=3, column=4)
        self.Pnote = tk.Label(self.sources_buttonframe, text=self.pnotes, font=("Arial", 10))
        self.Pnote.grid(row=6, column=4)
        self.Fnote = tk.Label(self.sources_buttonframe, text=self.fnotes, font=("Arial", 10))
        self.Fnote.grid(row=7, column=4)
        
        
        
        
        #Fit data in window
        self.input_provframe.pack(side='top',pady=25)
        self.input_buttonframe.pack(side='top',pady=25)
        self.menu_buttonframe.pack(side='top')
        self.sources_buttonframe.pack(side='bottom',pady=0)
        
        
        #update conv factors and sources
        self.prov.bind('<<ComboboxSelected>>',self.conv_change)
        
        
        #main window loop
        self.window.mainloop()
        
        
        
        
        


    def calc(self):
        '''
        

        Final calculation carbon emissions
        -------

        '''
        try:
            if self.E_inp.get()=='':
                self.E=0
            else:
                self.E=float(self.E_inp.get())
            if self.D_inp.get()=='':
                self.D=0
            else:
                self.D=float(self.D_inp.get())
            if self.G_inp.get()=='':
                self.G=0
            else:
                self.G=float(self.G_inp.get())
            if self.N_inp.get()=='':
                self.N=0
            else:
                self.N=float(self.N_inp.get())
            if self.P_inp.get()=='':
                self.P=0
            else:
                self.P=float(self.P_inp.get())
            if self.F_inp.get()=='':
                self.F=0
            else:
                self.F=float(self.F_inp.get())
            self.res=self.E*self.econv+self.D*self.dconv+self.G*self.gconv+self.N*self.ngconv+self.F*self.fconv+self.P*self.pconv
            if self.res==0:
                self.calcres.config(text=self.res)
            else:
                self.calcres.config(text=self.round_sigfig(self.res))
            
        except:
            messagebox.showinfo(title="Error", message=" Check all entries and ensure they are numbers")
            
        
    
        
    def exportresults(self):
        '''
        

        Creates excel file with summary of calculation results and sources
        -------

        '''
        self.calc()
        data=[{'type':'Electricity','Use':self.E,'Conv':self.econv,'Unit':self.eunit, 'Source':self.esource,'Date':self.edate,'Notes':self.enotes},
              {'type':'Diesel','Use':self.D,'Conv':self.dconv,'Unit':self.dunit,'Source':self.dsource,'Date':self.ddate,'Notes':self.dnotes},
              {'type':'Gasoline','Use':self.G,'Conv':self.gconv,'Unit':self.gunit,'Source':self.gsource,'Date':self.gdate,'Notes':self.gnotes},
              {'type':'natural gas','Use':self.N,'Conv':self.ngconv,'Unit':self.ngunit,'Source':self.ngsource,'Date':self.ngdate,'Notes':self.ngnotes},
              {'type':'Propane','Use':self.P,'Conv':self.pconv,'Unit':self.punit,'Source':self.psource,'Date':self.pdate,'Notes':self.pnotes},
              {'type':'Fuel Oil','Use':self.F,'Conv':self.fconv,'Unit':self.funit,'Source':self.fsource,'Date':self.fdate,'Notes':self.fnotes},
              {'type':'Province','Use':self.prov.get()},
              {'type':'Total CO2e (mT)','Use':self.res}]
        with open('carbon_Calc.csv','w',newline='') as csvfile:
            fieldnames=['type','Use','Conv','Unit','Source','Date','Notes']
            writer=csv.DictWriter(csvfile,fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        
    def datavalidation(self,char):
        '''
        

        Parameters
        ----------
        char : User entry

        Returns: True/False
        -------
        Ensures Numeric input
            

        '''
        return (char.isdigit() or char=='.')
    
    
    def conv_change(self,e):
        '''
        

        Parameters
        ----------
        e : combobox change event

        Returns
        -------
        None.
        
        Updates labels based on combobox entry
        '''
        self.sources(self.prov.get())
        self.E_conv.config(text='×'+str(self.round_sigfig(self.econv)))
        self.D_conv.config(text='×'+str(self.round_sigfig(self.dconv)))
        self.G_conv.config(text='×'+str(self.round_sigfig(self.gconv)))
        self.N_conv.config(text='×'+str(self.round_sigfig(self.ngconv)))
        self.P_conv.config(text='×'+str(self.round_sigfig(self.pconv)))
        self.F_conv.config(text='×'+str(self.round_sigfig(self.fconv)))
        
        self.Esource.config(text=self.esource)
        self.Dsource.config(text=self.dsource)
        self.Ngsource.config(text=self.ngsource)
        self.Gsource.config(text=self.gsource)
        self.Psource.config(text=self.psource)
        self.Fsource.config(text=self.fsource)
        self.provsource.config(text=self.prov.get())
        
        self.Edate.config(text=self.edate)
        self.Ddate.config(text=self.ddate)
        self.Ngdate.config(text=self.ngdate)
        self.Gdate.config(text=self.gdate)
        self.Pdate.config(text=self.pdate)
        self.Fdate.config(text=self.fdate)
        
        self.Edate = tk.Label(self.sources_buttonframe, text=self.edate, font=("Arial", 10))
        self.Edate.grid(row=2, column=3)
        self.Gdate = tk.Label(self.sources_buttonframe, text=self.gdate, font=("Arial", 10))
        self.Gdate.grid(row=4, column=3)
        self.Ngdate = tk.Label(self.sources_buttonframe, text=self.ngdate, font=("Arial", 10))
        self.Ngdate.grid(row=5, column=3)
        self.Ddate = tk.Label(self.sources_buttonframe, text=self.ddate, font=("Arial", 10))
        self.Ddate.grid(row=3, column=3)
        self.Pdate = tk.Label(self.sources_buttonframe, text=self.pdate, font=("Arial", 10))
        self.Pdate.grid(row=6, column=3)
        self.Fdate = tk.Label(self.sources_buttonframe, text=self.fdate, font=("Arial", 10))
        self.Fdate.grid(row=7, column=3)
        
        self.Enote = tk.Label(self.sources_buttonframe, text=self.enotes, font=("Arial", 10))
        self.Enote.grid(row=2, column=4)
        self.Gnote = tk.Label(self.sources_buttonframe, text=self.gnotes, font=("Arial", 10))
        self.Gnote.grid(row=4, column=4)
        self.Ngnote = tk.Label(self.sources_buttonframe, text=self.ngnotes, font=("Arial", 10))
        self.Ngnote.grid(row=5, column=4)
        self.Dnote = tk.Label(self.sources_buttonframe, text=self.dnotes, font=("Arial", 10))
        self.Dnote.grid(row=3, column=4)
        self.Pnote = tk.Label(self.sources_buttonframe, text=self.pnotes, font=("Arial", 10))
        self.Pnote.grid(row=6, column=4)
        self.Fnote = tk.Label(self.sources_buttonframe, text=self.fnotes, font=("Arial", 10))
        self.Fnote.grid(row=7, column=4)
    
    def round_sigfig(self,x):
        '''
        

        Parameters
        ----------
        x : number

        Returns
        -------
        number rounded to 3 sig figs

        '''
        return round(x, -int(math.floor(math.log10(abs(x))))+3)
        
    
#####################################################################################################################################################    
    
    def sources(self,prov):
        '''
        

        Parameters
        ----------
        prov : Two letter Province code

        Returns
        -------
        None.

        Setsconversion factors and respective sources
        '''
        Econv={'CDN AVG':1*10**-4, 'ON':3.5*10**-5,'SK':0.00063,'YT':7*10**-5,'NT':0.00018,'NU':0.00078,'BC':1.4*10**-5,'AB':0.00047,'MB':1.3*10**-6,'QC':1.2*10**-6,'NB':0.00033,'NL':1.7*10**-5,'NS':0.00066,'PE':2*10**-6} #mt/kwh
        Esource={'ON':['https://www.cer-rec.gc.ca/en/data-analysis/energy-markets/provincial-territorial-energy-profiles/','2022','Converted from g to mT'],
                 'SK':['https://www.cer-rec.gc.ca/en/data-analysis/energy-markets/provincial-territorial-energy-profiles/','2022','Converted to mT'],
                 'CDN AVG':['https://www.cer-rec.gc.ca/en/data-analysis/energy-markets/provincial-territorial-energy-profiles/','2022','Converted from g to mT'],
                 'YT':['https://www.cer-rec.gc.ca/en/data-analysis/energy-markets/provincial-territorial-energy-profiles/','2022','Converted from g to mT'],
                 'NT':['https://www.cer-rec.gc.ca/en/data-analysis/energy-markets/provincial-territorial-energy-profiles/','2022','Converted from g to mT'],
                 'NU':['https://www.cer-rec.gc.ca/en/data-analysis/energy-markets/provincial-territorial-energy-profiles/','2022','Converted from g to mT'],
                 'BC':['https://www.cer-rec.gc.ca/en/data-analysis/energy-markets/provincial-territorial-energy-profiles/','2022','Converted from g to mT'],
                 'AB':['https://www.cer-rec.gc.ca/en/data-analysis/energy-markets/provincial-territorial-energy-profiles/','2022','Converted from g to mT'],
                 'MB':['https://www.cer-rec.gc.ca/en/data-analysis/energy-markets/provincial-territorial-energy-profiles/','2022','Converted from g to mT'],
                 'QC':['https://www.cer-rec.gc.ca/en/data-analysis/energy-markets/provincial-territorial-energy-profiles/','2022','Converted from g to mT'],
                 'NB':['https://www.cer-rec.gc.ca/en/data-analysis/energy-markets/provincial-territorial-energy-profiles/','2022','Converted from g to mT'],
                 'NL':['https://www.cer-rec.gc.ca/en/data-analysis/energy-markets/provincial-territorial-energy-profiles/','2022','Converted from g to mT'],
                 'NS':['https://www.cer-rec.gc.ca/en/data-analysis/energy-markets/provincial-territorial-energy-profiles/','2022','Converted from g to mT'],
                 'PE':['https://www.cer-rec.gc.ca/en/data-analysis/energy-markets/provincial-territorial-energy-profiles/','2022','Converted from g to mT']}
        
        Gconv={'CDN AVG': 8.887*10**-3,'ON':8.887*10**-3,'SK':8.887*10**-3,'YT':8.887*10**-3,'NT':8.887*10**-3,'NU':8.887*10**-3,'BC':8.887*10**-3,'AB':8.887*10**-3,'MB':8.887*10**-3,'QC':8.887*10**-3,'NB':8.887*10**-3,'NL':8.887*10**-3,'NS':8.887*10**-3,'PE':8.887*10**-3} # mt/gal
        Gsource={'CDN AVG':['https://www.epa.gov/energy/greenhouse-gases-equivalencies-calculator-calculations-and-references','2006','NA'], 
                 'ON':['https://www.epa.gov/energy/greenhouse-gases-equivalencies-calculator-calculations-and-references','2006','NA'],
                 'SK':['https://www.epa.gov/energy/greenhouse-gases-equivalencies-calculator-calculations-and-references','2006','NA'],
                 'YT':['https://www.epa.gov/energy/greenhouse-gases-equivalencies-calculator-calculations-and-references','2006','NA'],
                 'NT':['https://www.epa.gov/energy/greenhouse-gases-equivalencies-calculator-calculations-and-references','2006','NA'],
                 'NU':['https://www.epa.gov/energy/greenhouse-gases-equivalencies-calculator-calculations-and-references','2006','NA'],
                 'BC':['https://www.epa.gov/energy/greenhouse-gases-equivalencies-calculator-calculations-and-references','2006','NA'],
                 'AB':['https://www.epa.gov/energy/greenhouse-gases-equivalencies-calculator-calculations-and-references','2006','NA'],
                 'MB':['https://www.epa.gov/energy/greenhouse-gases-equivalencies-calculator-calculations-and-references','2006','NA'],
                 'QC':['https://www.epa.gov/energy/greenhouse-gases-equivalencies-calculator-calculations-and-references','2006','NA'],
                 'NB':['https://www.epa.gov/energy/greenhouse-gases-equivalencies-calculator-calculations-and-references','2006','NA'],
                 'NL':['https://www.epa.gov/energy/greenhouse-gases-equivalencies-calculator-calculations-and-references','2006','NA'],
                 'NS':['https://www.epa.gov/energy/greenhouse-gases-equivalencies-calculator-calculations-and-references','2006','NA'],
                 'PE':['https://www.epa.gov/energy/greenhouse-gases-equivalencies-calculator-calculations-and-references','2006','NA']}
        
        Ngconv={'CDN AVG': 1.93236/264.172/1000,'ON':1.93236/264.172/1000,'SK':1.93236/264.172/1000,'YT':1.93236/264.172/1000,'NT':1.93236/264.172/1000,'NU':1.93236/264.172/1000,'BC':1.93236/264.172/1000,'AB':1.93236/264.172/1000,'MB':1.93236/264.172/1000,'QC':1.93236/264.172/1000,'NB':1.93236/264.172/1000,'NL':1.93236/264.172/1000,'NS':1.93236/264.172/1000,'PE':1.93236/264.172/1000}#mt/gal
        Ngsource={'CDN AVG':['https://uwaterloo.ca/sustainability/our-progress/climate-data','2021','Converted from kg/m3 to mT/Gal'], 
                 'ON':['https://uwaterloo.ca/sustainability/our-progress/climate-data','2021','Converted from kg/m3 to mT/Gal'],
                 'SK':['https://uwaterloo.ca/sustainability/our-progress/climate-data','2021','Converted from kg/m3 to mT/Gal'],
                 'YT':['https://uwaterloo.ca/sustainability/our-progress/climate-data','2021','Converted from kg/m3 to mT/Gal'],
                 'NT':['https://uwaterloo.ca/sustainability/our-progress/climate-data','2021','Converted from kg/m3 to mT/Gal'],
                 'NU':['https://uwaterloo.ca/sustainability/our-progress/climate-data','2021','Converted from kg/m3 to mT/Gal'],
                 'BC':['https://uwaterloo.ca/sustainability/our-progress/climate-data','2021','Converted from kg/m3 to mT/Gal'],
                 'AB':['https://uwaterloo.ca/sustainability/our-progress/climate-data','2021','Converted from kg/m3 to mT/Gal'],
                 'MB':['https://uwaterloo.ca/sustainability/our-progress/climate-data','2021','Converted from kg/m3 to mT/Gal'],
                 'QC':['https://uwaterloo.ca/sustainability/our-progress/climate-data','2021','Converted from kg/m3 to mT/Gal'],
                 'NB':['https://uwaterloo.ca/sustainability/our-progress/climate-data','2021','Converted from kg/m3 to mT/Gal'],
                 'NL':['https://uwaterloo.ca/sustainability/our-progress/climate-data','2021','Converted from kg/m3 to mT/Gal'],
                 'NS':['https://uwaterloo.ca/sustainability/our-progress/climate-data','2021','Converted from kg/m3 to mT/Gal'],
                 'PE':['https://uwaterloo.ca/sustainability/our-progress/climate-data','2021','Converted from kg/m3 to mT/Gal']}
        
        Dconv={'CDN AVG': 10.180*10**-3,'ON':10.180*10**-3,'SK':10.180*10**-3,'YT':10.180*10**-3,'NT':10.180*10**-3,'NU':10.180*10**-3,'BC':10.180*10**-3,'AB':10.180*10**-3,'MB':10.180*10**-3,'QC':10.180*10**-3,'NB':10.180*10**-3,'NL':10.180*10**-3,'NS':10.180*10**-3,'PE':10.180*10**-3} #mt/gal 
        Dsource={'CDN AVG':['https://www.epa.gov/energy/greenhouse-gases-equivalencies-calculator-calculations-and-references','2006','NA'], 
                 'ON':['https://www.epa.gov/energy/greenhouse-gases-equivalencies-calculator-calculations-and-references','2006','NA'],
                 'SK':['https://www.epa.gov/energy/greenhouse-gases-equivalencies-calculator-calculations-and-references','2006','NA'],
                 'YT':['https://www.epa.gov/energy/greenhouse-gases-equivalencies-calculator-calculations-and-references','2006','NA'],
                 'NT':['https://www.epa.gov/energy/greenhouse-gases-equivalencies-calculator-calculations-and-references','2006','NA'],
                 'NU':['https://www.epa.gov/energy/greenhouse-gases-equivalencies-calculator-calculations-and-references','2006','NA'],
                 'BC':['https://www.epa.gov/energy/greenhouse-gases-equivalencies-calculator-calculations-and-references','2006','NA'],
                 'AB':['https://www.epa.gov/energy/greenhouse-gases-equivalencies-calculator-calculations-and-references','2006','NA'],
                 'MB':['https://www.epa.gov/energy/greenhouse-gases-equivalencies-calculator-calculations-and-references','2006','NA'],
                 'QC':['https://www.epa.gov/energy/greenhouse-gases-equivalencies-calculator-calculations-and-references','2006','NA'],
                 'NB':['https://www.epa.gov/energy/greenhouse-gases-equivalencies-calculator-calculations-and-references','2006','NA'],
                 'NL':['https://www.epa.gov/energy/greenhouse-gases-equivalencies-calculator-calculations-and-references','2006','NA'],
                 'NS':['https://www.epa.gov/energy/greenhouse-gases-equivalencies-calculator-calculations-and-references','2006','NA'],
                 'PE':['https://www.epa.gov/energy/greenhouse-gases-equivalencies-calculator-calculations-and-references','2006','NA']}
        
        Pconv={'CDN AVG': 0.236/42,'ON':0.236/42,'SK':0.236/42,'YT':0.236/42,'NT':0.236/42,'NU':0.236/42,'BC':0.236/42,'AB':0.236/42,'MB':0.236/42,'QC':0.236/42,'NB':0.236/42,'NL':0.236/42,'NS':0.236/42,'PE':0.236/42} #mt/gal
        Psource={'CDN AVG':['https://www.epa.gov/energy/greenhouse-gases-equivalencies-calculator-calculations-and-references','2023','kg/barrel to mT/gal'], 
                 'ON':['https://www.epa.gov/energy/greenhouse-gases-equivalencies-calculator-calculations-and-references','2023','kg/barrel to mT/gal'],
                 'SK':['https://www.epa.gov/energy/greenhouse-gases-equivalencies-calculator-calculations-and-references','2023','kg/barrel to mT/gal'],
                 'YT':['https://www.epa.gov/energy/greenhouse-gases-equivalencies-calculator-calculations-and-references','2023','kg/barrel to mT/gal'],
                 'NT':['https://www.epa.gov/energy/greenhouse-gases-equivalencies-calculator-calculations-and-references','2023','kg/barrel to mT/gal'],
                 'NU':['https://www.epa.gov/energy/greenhouse-gases-equivalencies-calculator-calculations-and-references','2023','kg/barrel to mT/gal'],
                 'BC':['https://www.epa.gov/energy/greenhouse-gases-equivalencies-calculator-calculations-and-references','2023','kg/barrel to mT/gal'],
                 'AB':['https://www.epa.gov/energy/greenhouse-gases-equivalencies-calculator-calculations-and-references','2023','kg/barrel to mT/gal'],
                 'MB':['https://www.epa.gov/energy/greenhouse-gases-equivalencies-calculator-calculations-and-references','2023','kg/barrel to mT/gal'],
                 'QC':['https://www.epa.gov/energy/greenhouse-gases-equivalencies-calculator-calculations-and-references','2023','kg/barrel to mT/gal'],
                 'NB':['https://www.epa.gov/energy/greenhouse-gases-equivalencies-calculator-calculations-and-references','2023','kg/barrel to mT/gal'],
                 'NL':['https://www.epa.gov/energy/greenhouse-gases-equivalencies-calculator-calculations-and-references','2023','kg/barrel to mT/gal'],
                 'NS':['https://www.epa.gov/energy/greenhouse-gases-equivalencies-calculator-calculations-and-references','2023','kg/barrel to mT/gal'],
                 'PE':['https://www.epa.gov/energy/greenhouse-gases-equivalencies-calculator-calculations-and-references','2023','kg/barrel to mT/gal']}
        
        
        Fconv={'CDN AVG': 2.90532/0.264172/1000,'ON':2.90532/0.264172/1000,'SK':2.90532/0.264172/1000,'YT':2.90532/0.264172/1000,'NT':2.90532/0.264172/1000,'NU':2.90532/0.264172/1000,'BC':2.90532/0.264172/1000,'AB':2.90532/0.264172/1000,'MB':2.90532/0.264172/1000,'QC':2.90532/0.264172/1000,'NB':2.90532/0.264172/1000,'NL':2.90532/0.264172/1000,'NS':2.90532/0.264172/1000,'PE':2.90532/0.264172/1000} #mt/gal
        Fsource={'CDN AVG':['https://uwaterloo.ca/sustainability/our-progress/climate-data','2021','Converted from kg/m3 to mT/Gal'], 
                 'ON':['https://uwaterloo.ca/sustainability/our-progress/climate-data','2021','Converted from kg/L to mT/Gal'],
                 'SK':['https://uwaterloo.ca/sustainability/our-progress/climate-data','2021','Converted from kg/L to mT/Gal'],
                 'YT':['https://uwaterloo.ca/sustainability/our-progress/climate-data','2021','Converted from kg/L to mT/Gal'],
                 'NT':['https://uwaterloo.ca/sustainability/our-progress/climate-data','2021','Converted from kg/L to mT/Gal'],
                 'NU':['https://uwaterloo.ca/sustainability/our-progress/climate-data','2021','Converted from kg/L to mT/Gal'],
                 'BC':['https://uwaterloo.ca/sustainability/our-progress/climate-data','2021','Converted from kg/L to mT/Gal'],
                 'AB':['https://uwaterloo.ca/sustainability/our-progress/climate-data','2021','Converted from kg/L to mT/Gal'],
                 'MB':['https://uwaterloo.ca/sustainability/our-progress/climate-data','2021','Converted from kg/L to mT/Gal'],
                 'QC':['https://uwaterloo.ca/sustainability/our-progress/climate-data','2021','Converted from kg/L to mT/Gal'],
                 'NB':['https://uwaterloo.ca/sustainability/our-progress/climate-data','2021','Converted from kg/L to mT/Gal'],
                 'NL':['https://uwaterloo.ca/sustainability/our-progress/climate-data','2021','Converted from kg/L to mT/Gal'],
                 'NS':['https://uwaterloo.ca/sustainability/our-progress/climate-data','2021','Converted from kg/L to mT/Gal'],
                 'PE':['https://uwaterloo.ca/sustainability/our-progress/climate-data','2021','Converted from kg/L to mT/Gal']}
        
        self.econv=Econv[prov]   
        self.esource,self.edate,self.enotes=tuple(Esource[prov])
        self.gconv=Gconv[prov]
        self.gsource,self.gdate,self.gnotes=tuple(Gsource[prov])
        self.ngconv=Ngconv[prov]
        self.ngsource,self.ngdate,self.ngnotes=tuple(Ngsource[prov])
        self.dconv=Dconv[prov]
        self.dsource,self.ddate,self.dnotes=tuple(Dsource[prov])
        self.pconv=Pconv[prov]
        self.psource,self.pdate,self.pnotes=tuple(Psource[prov])
        self.fconv=Fconv[prov]
        self.fsource,self.fdate,self.fnotes=tuple(Fsource[prov])
        self.eunit='mT CO2e/kWh'
        self.dunit='mT CO2e/Gal'
        self.ngunit='mT CO2e/Gal'
        self.gunit='mT CO2e/Gal'
        self.punit='mT CO2e/Gal'
        self.funit='mT CO2e/Gal'
        
###################################################################################################################################################        
        
        
    
    
        
if __name__ == '__main__':

    carbon_calculator= GUI()
        