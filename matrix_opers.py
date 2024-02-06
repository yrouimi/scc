import pandas as pd
import numpy as np
import plotly.graph_objs as go
import itertools
import networkx as nx
import h5py
import time

#Tell the program which files to import and how to crop each vector
Dsheets={'Leontief': {'Lstart': 0, 'Cstart': 1, 'Bnumvals': True},
      'A': {'Lstart': 0, 'Cstart': 1, 'Bnumvals': True},
      'FD': {'Lstart': 2, 'Cstart': 3,'Bnumvals': True},
      'Intensities': {'Lstart': 2, 'Cstart': 3,'Bnumvals': True},
      'Slicing_vecs': {'Lstart': 0, 'Cstart': 3, 'Bnumvals': False},
      'Slicing_vecs_FD': {'Lstart': 0, 'Cstart': 3, 'Bnumvals': False},
      'Slicing_vecs_intensities': {'Lstart': 0, 'Cstart': 3, 'Bnumvals': False}}

####################################################
######## File imports and vector creations #########
####################################################

#Take a directory and create a pandas dataframe
def fn_createdffrom_txtfile(Sfilename):
    
    print(Sfilename + ' - Loading')
    Dtxt = pd.read_csv(Sfilename, header = 0,index_col=0)
    return Dtxt

# Take an HDF5 file and create a pandas dataframe
def create_df_from_hdf5(Sfilename):
    
    print(Sfilename + ' - Loading')
  
    with pd.HDFStore(Sfilename + '.h5') as store:
  
        print(store.keys())
        df = pd.read_hdf(store, key=Sfilename)
        
    return df



#Take a dataframe and slice it to keep only what's needed
def fn_convert_dftoVmat(df,Lstart,Cstart,Bnumvals):
    
    #By default, a view is returned, so any modifications made will affect the original. If you need a copy instead, use to_numpy(copy=True).   
    if Bnumvals == True:
        df = df.apply(pd.to_numeric, errors='coerce')     # Convert non-numeric values to NaN
    Vmat = df.to_numpy(copy=True)      # Get the values as a NumPy array
    Vmat = Vmat[Lstart:, Cstart:]
    
    return Vmat

def fn_create_permdictionaries(Dsheets):

    Ddic = {}

    for Sfilename in Dsheets.keys():
    
        #Ddic[Sfilename] = fn_createdffrom_txtfile(Sfilename + ".txt")
        Ddic[Sfilename] = create_df_from_hdf5(Sfilename)
    
    return Ddic

def fn_create_permarrays():

    Ddic = {}

    for Skey, Dsubdict in Dsheets.items():
        
        
        Ddic[Skey] = fn_convert_dftoVmat(Dimportedfiles[Skey],Dsubdict['Lstart'], Dsubdict['Cstart'], Dsubdict['Bnumvals'])
        
    Ddic['Coordinates'] = {'ARG':{'lat':-34,'lon':-64},'AUS':{'lat':-27,'lon':133},'AUT':{'lat':47.3333,'lon':13.3333},'BEL':{'lat':50.8333,'lon':4},'BGR':{'lat':43,'lon':25},'BRA':{'lat':-10,'lon':-55},'BRN':{'lat':4.5,'lon':114.6667},
    'CAN':{'lat':60,'lon':-95},'CHE':{'lat':47,'lon':8},'CHL':{'lat':-30,'lon':-71},'CHN':{'lat':35,'lon':105},'COL':{'lat':4,'lon':-72},'CRI':{'lat':10,'lon':-84},'CYP':{'lat':35,'lon':33},'CZE':{'lat':49.75,'lon':15.5},'DEU':{'lat':51,'lon':9},
    'DNK':{'lat':56,'lon':10},'ESP':{'lat':40,'lon':-4},'EST':{'lat':59,'lon':26},'FIN':{'lat':64,'lon':26},'FRA':{'lat':46,'lon':2},'GBR':{'lat':54,'lon':-2},'GRC':{'lat':39,'lon':22},'HKG':{'lat':22.25,'lon':114.1667},'HRV':{'lat':45.1667,'lon':15.5},
    'HUN':{'lat':47,'lon':20},'IDN':{'lat':-5,'lon':120},'IND':{'lat':20,'lon':77},'IRL':{'lat':53,'lon':-8},'ISL':{'lat':65,'lon':-18},'ISR':{'lat':31.5,'lon':34.75},'ITA':{'lat':42.8333,'lon':12.8333},'JPN':{'lat':36,'lon':138},'KAZ':{'lat':48,'lon':68},
    'KHM':{'lat':13,'lon':105},'KOR':{'lat':37,'lon':127.5},'LAO':{'lat':18,'lon':105},'LTU':{'lat':56,'lon':24},'LUX':{'lat':49.75,'lon':6.1667},'LVA':{'lat':57,'lon':25},'MAR':{'lat':32,'lon':-5},'MEX':{'lat':23,'lon':-102},
    'MLT':{'lat':35.8333,'lon':14.5833},'MMR':{'lat':22,'lon':98},'MYS':{'lat':2.5,'lon':112.5},'NLD':{'lat':52.5,'lon':5.75},'NOR':{'lat':62,'lon':10},'NZL':{'lat':-41,'lon':174},'PER':{'lat':-10,'lon':-76},'PHL':{'lat':13,'lon':122},
    'POL':{'lat':52,'lon':20},'PRT':{'lat':39.5,'lon':-8},'ROU':{'lat':46,'lon':25},'ROW':{'lat':0,'lon':25},'RUS':{'lat':60,'lon':100},'SAU':{'lat':25,'lon':45},'SGP':{'lat':1.3667,'lon':103.8},'SVK':{'lat':48.6667,'lon':19.5},
    'SVN':{'lat':46,'lon':15},'SWE':{'lat':62,'lon':15},'THA':{'lat':15,'lon':100},'TUN':{'lat':34,'lon':9},'TUR':{'lat':39,'lon':35},'TWN':{'lat':23.5,'lon':121},'USA':{'lat':38,'lon':-97},'VNM':{'lat':16,'lon':106},'ZAF':{'lat':-29,'lon':24}}

    return Ddic

#Fetches the right vector for intensities (among PROD,VA,EM,CO2) and returns it
def fn_fetch_intensityvec(Scon): 

    Vcons = Dstructuralarrays['Slicing_vecs_intensities'][0] #'It is a 2d array that we have, just with one element, made of 4 (for now) elements
    i = np.where(Vcons == Scon)[0] 
        
    return Dstructuralarrays['Intensities'][i][0]

#Converts a matrix of flows of PROD into VA, EM, Co2...
def fn_convert_prodmat(Vmat,Svar):        

    if Svar == 'Output':
    
        return Vmat
        
    else:

        Vintensities = fn_fetch_intensityvec(Svar)
        
        if len(Vmat.shape) == 1: #Case where Vmat is a simple vector: element-wise multiplication
            
            return Vmat*Vintensities
        
        else: #Case where Vmat is a 2d array: dot multiplication
                          
            return np.dot(np.diag(Vintensities),Vmat)

def fn_removelist_duppli(Vlist,Bsort = False): 

    if Bsort == False:

        res,ind = np.unique(Vlist, return_index=True) # Applying unique function on array
        Vres = res[np.argsort(ind)]

    else:
    
        Vres = np.unique(Vlist)

    return Vres

#Function converting string (or array of strings) into hexadecimal values (or array of hexadecimal values)
def fn_generate_hexcolor(Stxt):
    
    if type(Stxt) == str:
    
        # Convert the string to a unique integer using a hash function
        hash_val = hash(Stxt)
        
        # Convert the hash value to a 6-digit hexadecimal color code
        color_code = '#' + format(abs(hash_val) % (2**24), '06x')

        return color_code
    
    elif type(Stxt) == list:
            
        Vcolor_codes = []
            
        for txt in Stxt:
    
            # Convert the string to a unique integer using a hash function
            hash_val = hash(Stxt)
            
            # Convert the hash value to a 6-digit hexadecimal color code
            color_code = '#' + format(abs(hash_val) % (2**24), '06x')
        
            Vcolor_codes.append(color_code)

def fn_filter_df(df, column_name, condition= '*'): #Accepts both numerical and string tests

    try:
        # Try to convert the condition to a float
        condition = float(condition)
        filtered_df = df[df[column_name] > condition]
    except ValueError:
        # If the condition can't be converted to a float, assume it's a string pattern
        filtered_df = df[df[column_name].str.contains(condition)]
    
    return filtered_df
    
def fn_keep_topdfvals(df, Scolsort, n, B_residcalc=False, Scolfilter = None,Scritfilter = '*'):

    filtered_df = df

    #Filter the dataframe to keep only some values you are interested
    if Scolfilter != None:
        filtered_df = fn_filter_df(df,Scolfilter,Scritfilter)    

    # Sort the dataframe based on values in column Scolsort
    df_sorted = filtered_df.sort_values(by=[Scolsort])

    # Get the n largest values in column 'A'
    largestvals = df_sorted[Scolsort].nlargest(n)
    
    # Filter the dataframe to keep only rows with the n largest values in column 'A'
    df_cropped = df_sorted[df_sorted[Scolsort].isin(largestvals)].reset_index(drop=True)

    nrows = df_cropped.index[-1]+1

    if B_residcalc==True:   
        
        for Scol in df_cropped.columns:
        
            if all(isinstance(item, (int, float)) for item in df_cropped[Scol]):
                print('here')
                df_cropped.loc[0, Scol] = sum(df_sorted[Scol]) - sum(df_cropped[Scol])#df_cropped.loc[nrows, Scol] = sum(df_sorted[Scol]) - sum(df_cropped[Scol])#df_cropped[Scol].iloc[0] = sum(df_sorted[Scol]) - sum(df_cropped[Scol])
            else:
                df_cropped.loc[0, Scol] = 'Other segments' + Scritfilter#df_cropped[Scol].iloc[0] = 'Other segments' + Scritfilter

    return df_cropped


####################################################
############### Permanent variables ################
####################################################
     
Dimportedfiles = fn_create_permdictionaries(Dsheets)
Dstructuralarrays = fn_create_permarrays()

# for Skey in Dsheets.keys():

    # print(Skey)
    # print(Dstructuralarrays[Skey])
    
##############################
#########IO algrebra##########
##############################

# Calculate a vector of total requirements. If Svar is not given then calculate just for output
def fn_calc_totreqs(VFD,VLeontief,Svar = 'Output'):
        
    Vtotreqs = np.dot(VLeontief,VFD)
    
    return fn_convert_prodmat(Vtotreqs,Svar)

#Calculate matrix of all intermediate transactions - no final product!
def fn_calc_intermediatereqs(VA,Vtotreqs,Svar = 'Output'):
        
    Vireqs = np.array([Vtotreqs*a for a in VA])
    #Vireqs = np.dot(VA,np.diag(Vtotreqs))
    #sparse_matrix = csr_matrix((np.diag(Vtotreqs), (rows, columns)),

    return fn_convert_prodmat(Vireqs,Svar)

######### Standalone functions
def fn_calc_intermediatereqs_stal(Sisoref,Ssecref,Svar = 'Output',Scustomshock = None):

    Vfdbase = Dstructuralarrays['FD']
    Vgroups = Dstructuralarrays['Slicing_vecs']
    Vfdgroups=Dstructuralarrays['Slicing_vecs_FD']
    Vleontief=Dstructuralarrays['Leontief']
    Va=Dstructuralarrays['A']

    Vfdshock = fn_assemble_FDvec(Vfdbase,Vgroups,Vfdgroups, [Sisoref,Ssecref], ['Final demand'])

    if Scustomshock != None:
        factor = float(Scustomshock)/np.sum(Vfdshock)
        Vfdshock = np.array(Vfdshock) * factor

    Vtotreqs = fn_calc_totreqs(Vfdshock,Vleontief)
    Vinterreqs= fn_calc_intermediatereqs(Va,Vtotreqs)
    
    return fn_convert_prodmat(Vinterreqs,Svar)

def fn_calc_totreqs_stal(Sisoref,Ssecref,BsubstractFD = False,Svar = 'Output',Scustomshock = None):

    Vfdbase = Dstructuralarrays['FD']
    Vgroups = Dstructuralarrays['Slicing_vecs']
    Vfdgroups=Dstructuralarrays['Slicing_vecs_FD']
    Vleontief=Dstructuralarrays['Leontief']
    Va=Dstructuralarrays['A']
    
    Vfdshock = fn_assemble_FDvec(Vfdbase,Vgroups,Vfdgroups, [Sisoref,Ssecref], ['Final demand'])
    
    if Scustomshock != None:
        factor = float(Scustomshock)/np.sum(Vfdshock)
        Vfdshock = np.array(Vfdshock) * factor
    
    Vtotreqs = fn_calc_totreqs(Vfdshock,Vleontief)
    
    if BsubstractFD == True: #Case where one wants to remove the output for final use
        Vtotreqs = Vtotreqs-Vfdshock
    
    return fn_convert_prodmat(Vtotreqs,Svar)


###################################################
#########End matrix tailored calculations##########
###################################################

#Take a matrix, labels for rows and columns and calculates a filtered array (zeros, except for the targeted cells) based on some filters
def fn_calcconditional_array(V2Dmat,Vcatsrows,Vcatscols, Vfilterrows,Vfiltercols):

    Vmat2 = np.vstack(V2Dmat)
    
    #fn_print_Vmat(Vmat2,'Vmat2')
    
    #########################
    # Deal with filtered row#  
    #########################
    
    #1) Go around every filtered value in the Vfilterrows array, and figure in which Vcat they appear
    Vwhichcat = np.zeros(len(Vfilterrows))
    for i,filteredval in enumerate(Vfilterrows):
        #Find in which Vcats it appears
        for j, Vcat in enumerate(Vcatsrows):
            if filteredval in Vcat:
                Vwhichcat[i]=j
                break
    
    #2)At that point we have a vector indicating the category to which each filtered value belongs ("Western Europe" will be the regional vector, "DEU" the ISO one)
    Vusedcats, _ = np.unique(Vwhichcat, return_index=True)
    
    Vrows = np.ones(len(Vcatsrows[0]), dtype=bool)
    
    for icat in Vusedcats:
        Vcrits = Vcatsrows[int(icat)] #Range of related values
        Vrow = np.zeros(len(Vcatsrows[0]), dtype=bool)
        for Sfiltrelem in Vfilterrows:
            Vrow = np.isin(Vcrits, Sfiltrelem) | Vrow
        Vrows = Vrow * Vrows

    #############################
    ##Deal with filtered column##  
    #############################

    #1) Go around every filtered value in the Vfiltercols array, and figure in which Vcat they appear
    Vwhichcat = np.zeros(len(Vfiltercols))
    for i,filteredval in enumerate(Vfiltercols):
        #Find in which Vcats it appears
        for j, Vcat in enumerate(Vcatscols):
            if filteredval in Vcat:
                Vwhichcat[i]=j
                break
   
    #At that point we have a vector indicating the category to which each filtered value belongs ("Western Europe" will be the regional vector, "DEU" the ISO one)
    Vusedcats, _ = np.unique(Vwhichcat, return_index=True)

    Vcols = np.ones(len(Vcatscols[0]), dtype=bool)

    for icat in Vusedcats:
        Vcrits = Vcatscols[int(icat)] #Range of related values
        Vcol = np.zeros(len(Vcatscols[0]), dtype=bool)
        for Sfiltrelem in Vfiltercols:
            Vcol = np.isin(Vcrits, Sfiltrelem) | Vcol
        Vcols = Vcol * Vcols            
    
    # Convert boolean arrays to integer indices
    Vrows = np.where(Vrows)[0]
    Vcols = np.where(Vcols)[0]  

    Vrows = np.concatenate([Vrows])
    Vcols = np.concatenate([Vcols])

    Vmatnew = np.zeros(Vmat2.shape)

    #Vmatnew[Vrows, Vcols] = Vmat2[Vrows, Vcols]
    for i in range(len(Vrows)):
        for j in range(len(Vcols)):
            Vmatnew[Vrows[i], Vcols[j]] = Vmat2[Vrows[i], Vcols[j]]


    return Vmatnew#np.sum(Vmat2[np.ix_(Vrows, Vcols)])  

#Take a matrix, labels for rows and columns and calculates a filtered array (zeros, except for the targeted cells) based on some filters
def fn_calcconditional_sum(V2Dmat,Vcatsrows,Vcatscols, Vfilterrows,Vfiltercols):

    return np.sum(fn_calcconditional_array(V2Dmat,Vcatsrows,Vcatscols, Vfilterrows,Vfiltercols))

#Take the vector of final demands (several columns) and makes it into one depending on what we want
def fn_assemble_FDvec(Vfullfd,Vcatsrows,Vcatscols, Vfilterrows,Vfiltercols):
       
    Vfiltmat = fn_calcconditional_array(Vfullfd,Vcatsrows, Vcatscols,Vfilterrows,Vfiltercols)
    return Vfiltmat.sum(axis=1)
  
###################################################
############ Supply chain calculations ############
###################################################

#Function to assess the dependency in a vectorized form
#Giving an order too
def fn_assess_dep(Stype,Sisoref,Ssecref,Sisodep,Ssecdep,Svar='Output'):

    if Stype == 'Supply':
        Vmat = fn_assess_supplydep(Sisoref,Ssecref,Sisodep,Ssecdep,Svar)
        
    if Stype == 'Demand':
        Vmat = fn_assess_demanddep(Sisoref,Ssecref,Sisodep,Ssecdep,Svar)
        
    return Vmat

# Calculate direct/indirect supply  dependencies of Sisoref in a given industry towards Sisodep in another
def fn_assess_supplydep(Sisoref,Ssecref,Sisodep,Ssecdep,Svar = 'Output'): 

    #t = time.time() 

    Vfdbase = Dstructuralarrays['FD']
    Vgroups = Dstructuralarrays['Slicing_vecs']
    Vfdgroups=Dstructuralarrays['Slicing_vecs_FD']
    Vleontief=Dstructuralarrays['Leontief']
    Va=Dstructuralarrays['A']

    #t = fn_timer(t,'Vector initialization')

    Vmat = []

    ##############
    # Supply dep #
    ##############
        
    Vfdshock = fn_assemble_FDvec(Vfdbase,Vgroups,Vfdgroups, [Sisoref,Ssecref], ['Final demand'])        
    #t = fn_timer(t,'FD calibration')

    Vtotreqsshock = fn_calc_totreqs(Vfdshock,Vleontief)
    #t = fn_timer(t,'Totreqs calc')    

    Vinterreqsshock = fn_calc_intermediatereqs(Va,Vtotreqsshock,Svar)
    #t = fn_timer(t,'Interreqs calc')    
    
    Vy = []
    
    Vrows = []
    Vrows.append(Ssecdep) if Ssecdep!='*' else None
    Vrows.append(Sisodep) if Sisodep!='*' else None
        
    valdirect = fn_calcconditional_sum(Vinterreqsshock,Vgroups,Vgroups, Vrows,[Ssecref,Sisoref]) #Direct purchases of Sisoref from Sisodep
    Vy.append(valdirect)
    #t = fn_timer(t,'Conditional sum - Direct')    
    valtot = fn_calcconditional_sum(Vinterreqsshock,Vgroups,Vgroups, Vrows,[]) #Direct purchases of Sisoref from Sisodep#np.sum(Vinterreqsshock) #Total purchases of Sisoref
    
    Vy.append(valtot-valdirect)
    
    #t = fn_timer(t,'Conditional sum - Indirect')
    
    Vmat.append(Vy)
           
    return Vy

# Calculate direct/indirect demand  dependencies of Sisoref towards Sisodep
def fn_assess_demanddep(Sisoref,Ssecref,Sisodep,Ssecdep,Svar = 'Output'): 

    Vfdbase = Dstructuralarrays['FD']
    Vgroups = Dstructuralarrays['Slicing_vecs']
    Vfdgroups=Dstructuralarrays['Slicing_vecs_FD']
    Vleontief=Dstructuralarrays['Leontief']
    Va=Dstructuralarrays['A']

    ##############
    # Demand dep #
    ##############

    Visos = Dstructuralarrays['Slicing_vecs'][1]
    Visos = np.unique(Visos)

    Vfdshock = fn_assemble_FDvec(Vfdbase,Vgroups,Vfdgroups, Visos + [Ssecdep], [Sisodep,"Final demand"])
    
    Vmat = [['Sector','Direct id','Direct fd','Indirect id']]
    
    Vtotreqsshock = fn_calc_totreqs(Vfdshock,Vleontief)
    Vinterreqsshock = fn_calc_intermediatereqs(Va,Vtotreqsshock,Svar)
    Vfdshock = fn_convert_prodmat(Vfdshock,Svar)
    Vy = [Ssecref]
    valdirect = fn_calcconditional_sum(Vinterreqsshock,Vgroups,Vgroups, [Sisoref,Ssecref],[Sisodep,Ssecdep]) # Direct purchases of Sisoref from Sisodep
    Vy.append(valdirect)
    valfd = fn_calcconditional_sum([Vfdshock],[['xxx']],Vgroups, ['xxx'],[Ssecref,Sisoref]) # Need to add final demand
    Vy.append(valfd)
    valtot = fn_calcconditional_sum(Vinterreqsshock,Vgroups,Vgroups, [Sisoref,Ssecref],Visos)
    Vy.append(valtot-valdirect)
    Vmat.append(Vy)
           
    return Vmat

# Calculates activity of each sector/country at each stage of the production process
def fn_decompose_prodstages(Sisoref,Ssecref,Svar = 'Output',Scustomshock=None, nbstages=9):

    Vfdbase = Dstructuralarrays['FD']
    Vgroups = Dstructuralarrays['Slicing_vecs']
    Vfdgroups=Dstructuralarrays['Slicing_vecs_FD']
    Vleontief=Dstructuralarrays['Leontief']
    Va=Dstructuralarrays['A']

    #Visos = Dstructuralarrays['Slicing_vecs'][1]
    #Visos = np.unique(Visos)
    
    Vfdshock = fn_assemble_FDvec(Vfdbase,Vgroups,Vfdgroups, [Sisoref,Ssecref], ['Final demand'])
    
    if Scustomshock != None:
        factor = float(Scustomshock)/np.sum(Vfdshock)
        Vfdshock = np.array(Vfdshock) * factor
    
    Vtots = fn_calc_totreqs(Vfdshock,Vleontief)
    
    Vstages = [Vfdshock]
    Vstages.append(fn_calc_totreqs(Vfdshock,Va))
    
    for i in range(2,nbstages):
    
        Vmat = fn_calc_totreqs(Vstages[i-1],Va)
        Vstages.append(Vmat)
        
    Vstages.append(Vtots-np.sum(Vstages, axis=0))
    
    return [fn_convert_prodmat(Vstage,Svar) for Vstage in Vstages]

# Calculates average number of production stages for a country/sector to make output
def fn_calc_avprodsteps(Sisoref,Ssecref,Svar = 'Output'):

    Vmat = fn_decompose_prodstages(Sisoref,Ssecref)
    Vmat = fn_convert_prodmat(Vmat,Svar)
    
    nstages = len(Vmat)

    Vstages=[i+1 for i in range(nstages-1)]
    Vstages.append(nstages+3)

    Vmat2= np.dot(Vstages,Vmat)
    
    Davstage = np.sum(Vmat2)/np.sum(Vmat)
    
    return Davstage

def fn_calc_SCsupplyposition(Sisoref,Ssecref,Sisodep,Ssecdep,Svar = 'Output'):

    Vgroups = Dstructuralarrays['Slicing_vecs']

    Vmat = fn_decompose_prodstages(Sisoref,Ssecref,Svar) #Fetch a matrix of the form 1 vector per stage    
    nstages = len(Vmat)
    Vstages=[i+1 for i in range(nstages-2)]
    
    Vstages.append(nstages+4)

    Vres = []
    
    #Extract data for segment in question
    for Vsubmat in Vmat[1:]:
        
        res = fn_calcconditional_sum([Vsubmat],[['xxx']],Vgroups,['xxx'],[Sisodep,Ssecdep])
        Vres.append(res)
    
    Vmat2= np.dot(Vstages,Vres)
    
    return np.sum(Vmat2)/np.sum(Vres)

def fn_calc_SCdemandposition(Sisoref,Ssecref,Sisodep,Ssecdep):

    Vgroups = Dstructuralarrays['Slicing_vecs']

    Vmat = fn_decompose_prodstages(Sisodep,Ssecdep) #Fetch a matrix of the form 1 vector per stage    
    nstages = len(Vmat)
    Vstages=[i+1 for i in range(nstages-1)]
    Vstages.append(nstages+4)
   
    Vres = []
    
    #Extract data for segment in question
    for Vsubmat in Vmat:
        
        res = fn_calcconditional_sum([Vsubmat],[['xxx']],Vgroups,['xxx'],[Sisodep,Ssecdep])
        Vres.append(res)
    
    Vmat2= np.dot(Vstages,Vres)
    
    return np.sum(Vmat2)/np.sum(Vres)


###################################################
#################### Display ######################
###################################################

def fn_print_Vmat(Vmat,Sname):

    print(Sname)
    print(Vmat)

def fn_timer(t0,Ssteprompt):

    t1 = time.time()
    elapsed_time = t1 - t0
    print(Ssteprompt)
    print(f"Time elapsed: {elapsed_time:.2f} seconds")
    return t1

    
def fn_print_2dmat(Vmat):
    for row in Vmat:
        print("|", end=" ")
        for item in row:
            print("{:2}".format(item), end=" | ")
        print()
        
def draw_sankey_network(data, labels):

    n = len(labels)
    source_indices = np.repeat(np.arange(n), n)
    target_indices = np.tile(np.arange(n), n)
    values = list(itertools.chain(*data))#data.flatten()

    node_colors = ['rgba(31, 119, 180, 0.8)' for _ in range(n)]

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=labels,
            color=node_colors
        ),
        link=dict(
            source=source_indices,
            target=target_indices,
            value=values,
            color=[f'rgba(31, 119, 180, {x/max(values)})' for x in values],
            line=dict(width=[x/max(values)*10 for x in values], color='black'),
        ))])

    return fig

def plot_flow_network(matrix, labels):
    # Create a directed graph
    g = nx.DiGraph()

    # Add nodes to the graph
    for i, label in enumerate(labels):
        g.add_node(i, label=label)

    # Add edges to the graph
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            g.add_edge(i, j, weight=matrix[i][j])

    # Get edge positions and weights
    edge_x = []
    edge_y = []
    edge_weights = []

    for edge in g.edges():
        x0, y0 = np.array(g.nodes[edge[0]]['pos'])
        x1, y1 = np.array(g.nodes[edge[1]]['pos'])
        weight = g.edges[edge]['weight']
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)
        edge_weights.append(weight)

    # Create the edge trace
    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line=dict(width=1, color=edge_weights, colorscale='Blues', showscale=True),
        hoverinfo='none',
        mode='lines'
    )

    # Get node positions
    node_x = []
    node_y = []

    for node in g.nodes():
        x, y = np.array(g.nodes[node]['pos'])
        node_x.append(x)
        node_y.append(y)

    # Create the node trace
    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=False,
            colorscale='Blues',
            reversescale=True,
            color=[],
            size=10,
            line_width=2)
    )

    # Set the node text and colors
    node_trace.text = [g.nodes[node]['label'] for node in g.nodes()]
    node_trace.marker.color = [sum(matrix[i]) for i in range(matrix.shape[0])]

    # Create the figure
    fig = go.Figure(data=[edge_trace, node_trace])

    # Set the layout
    fig.update_layout(
        title='Trade Flow Network',
        title_x=0.5,
        title_font_size=24,
        showlegend=False,
        hovermode='closest',
        margin=dict(b=20, l=5, r=5, t=40),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
    )
    
    return fig

def create_flow_map(flows_matrix, country_codes):
    flows = []
    for i, source in enumerate(country_codes):
        for j, dest in enumerate(country_codes):
            if i != j and flows_matrix[i][j] > 0:
                flows.append(
                    go.Scattergeo(
                        lat=[source[1], dest[1], None],
                        lon=[source[2], dest[2], None],
                        mode='lines',
                        line=dict(width=flows_matrix[i][j]/100, color='red'),
                        opacity=0.6,
                        hoverinfo='none',
                        showlegend=False,
                    )
                )
    layout = go.Layout(
        geo=dict(
            projection_type='orthographic',
            showcoastlines=True,
            showland=True,
            showocean=True,
            oceancolor='rgb(229, 229, 255)',
            landcolor='rgb(229, 229, 229)',
            coastlinecolor='rgb(0, 0, 0)',
            countrywidth=0.5,
            countrycolor='rgb(255, 255, 255)'
        ),
        margin=dict(l=20, r=20, t=20, b=20),
        height=800,
        width=1000,
        title=dict(text='Flow Map')
    )
    fig = go.Figure(data=flows, layout=layout)
    return fig

def draw_lines_on_map(coordinates, flows, source_countries, target_countries, thickness_factor=0.01):
    # """
    # Draws lines on a map using plotly.graph_objs.
    
    # Parameters:
    # - coordinates: dictionary containing the latitudes and longitudes of each country
    # - flows: 2D matrix containing the flows between each country
    # - source_countries: list of source countries (in the order of the rows of 'flows')
    # - target_countries: list of target countries (in the order of the columns of 'flows')
    # - thickness_factor: factor to adjust the thickness of the lines (default=1)
    # """
    print(flows)

    lines = []
    for i in range(len(source_countries)):
        for j in range(len(target_countries)):
            if flows[i][j] > 0:

                source_lat=coordinates[source_countries[i]]['lat']
                source_lon = coordinates[source_countries[i]]['lon']
                target_lat=coordinates[target_countries[j]]['lat']
                target_lon = coordinates[target_countries[j]]['lon']

                line = go.Scattergeo(
                    locationmode = 'country names',
                    lon = [source_lon, target_lon],
                    lat = [source_lat, target_lat],
                    mode = 'lines',
                    line = dict(width = thickness_factor*flows[i][j]),
                    opacity = 0.7
                )
                lines.append(line)

    layout = go.Layout(
        geo = dict(
            scope='world',
            projection=dict(type='orthographic'),
            showland = True,
            landcolor = "rgb(250, 250, 250)",
            subunitcolor = "rgb(217, 217, 217)",
            countrycolor = "rgb(217, 217, 217)",
            countrywidth = 0.5,
            subunitwidth = 0.5
        ),
        margin=dict(l=0, r=0, t=0, b=0)
    )

    fig = go.Figure(data=lines, layout=layout)
    
    return fig
