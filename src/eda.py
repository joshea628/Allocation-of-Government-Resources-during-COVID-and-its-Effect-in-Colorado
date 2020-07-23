import pandas as pd 
import matplotlib.pyplot as plt 
from clean_data import *

plt.style.use('fivethirtyeight')

#List all unique ethnicities
ethnicities = df_with_counties['RaceEthnicity'].unique()

#separate data into ethnicities
def split_ethnicities(ethnicities):
    '''
    Splits main dataframe into separate dataframes for each ethnicity included in data

    Returns: List of dataframes
    '''
    dataframes = [df_with_counties[df_with_counties['RaceEthnicity'] == name] for name in ethnicities]
    return dataframes
#unpack dataframes
white_df, hispanic_df, am_indian_alaska_df, asian_df, black_df, puerto_rican_df = split_ethnicities(ethnicities)
ethnicity_dfs = [white_df, hispanic_df, am_indian_alaska_df, asian_df, black_df, puerto_rican_df]


#average loan amount for each ethnicity
def avg_loan_by_ethnicity(ethnicities, ethnicity_dfs):
    '''
    Computes average loan amount for each dataframe in inputted list.

    Returns: Dictionary of averages for each ethnicity in the form of ethnicity:average
    '''
    avg_loan = {eth:round(df['LoanAmount'].mean(),2) for eth, df in zip(ethnicities, ethnicity_dfs)}
    return avg_loan
ethnicity_avg_loan = avg_loan_by_ethnicity(ethnicities, ethnicity_dfs)

#total loan amount for each ethnicity
def total_loan_by_ethnicity(ethnicities, ethnicity_dfs):
    '''
    Computes average loan amount for each dataframe in inputted list.

    Returns: Dictionary of averages for each ethnicity in the form of ethnicity:average
    '''
    total_loan = {eth:df['LoanAmount'].sum() for eth, df in zip(ethnicities, ethnicity_dfs)}
    return total_loan
ethnicity_total_loan = total_loan_by_ethnicity(ethnicities, ethnicity_dfs)

#colors for bar charts
chart_colors = ['#003f5c', '#58508d', '#bc5090', '#dd5182','#ff6361', '#ffa600']

#graph average loan amounts 
def graph_average_loan_ethnicity(ethnicity_avg_loan, chart_colors, save_loc):
    '''
    Graphs the Average Loan Amount by Ethnicity

    Returns: None
    '''
    fig, ax = plt.subplots(1, figsize=(12,4), dpi=700)
    keys = ethnicity_avg_loan.keys()
    averages = ethnicity_avg_loan.values()
    bar = ax.bar(keys, averages)
    for i in range(len(ethnicity_avg_loan)):
        bar[i].set_color(chart_colors[i])
    plt.xticks(rotation=45, fontsize=12, horizontalalignment='right')
    ax.set_xlabel('Ethnicity', fontsize= 16)
    ax.set_ylabel('Average Loan Amount in $', fontsize= 16)
    ax.set_title('Average Loan Amount by Ethnicity in Colorado', fontsize=18)
    plt.savefig(save_loc, bbox_inches='tight')

graph_average_loan_ethnicity(ethnicity_avg_loan, chart_colors, '../images/avg_loan_ethnicity.png')

#graph total loan for each ethnicity
def graph_total_loan_ethnicity(ethnicity_total_loan, chart_colors, save_loc):
    '''
    Graphs the total Loan Amount by Ethnicity

    Returns: None
    '''
    fig, ax = plt.subplots(1, figsize=(12,4), dpi=700)
    keys = ethnicity_total_loan.keys()
    totals = ethnicity_total_loan.values()
    bar = ax.bar(keys, totals)
    for i in range(len(ethnicity_total_loan)):
        bar[i].set_color(chart_colors[i])
    plt.xticks(rotation=45, fontsize=12, horizontalalignment='right')
    #ax.set_yscale('log') #not sure if the scaling is welcome here or not...
    ax.set_xlabel('Ethnicity', fontsize= 16)
    ax.set_ylabel('Total Loan Amount in $', fontsize= 16)
    ax.set_title('Total Loan Amount by Ethnicity in Colorado', fontsize=18)
    plt.savefig(save_loc, bbox_inches='tight')

graph_total_loan_ethnicity(ethnicity_total_loan, chart_colors, '../images/total_loan_ethnicity.png')

#top zip codes for each ethnicity
def top_zip(ethnicity_dfs, ethnicities):
    '''
    Counts the number of loans for each Ethnicity group, sorts by top 5.

    Returns: Dictionary where Keys are the Ethnicities and values are a dataframe of top 5
    zipcodes and the count of loans from each zip.
    '''
    top_dict = {}
    for eth, df in zip(ethnicities, ethnicity_dfs):
        count_zips = df.groupby(['Zip']).count()['LoanAmount']
        sort_zip = count_zips.sort_values(ascending=False).head(5)
        top_dict[eth]= sort_zip
    return top_dict

top_zips = top_zip(ethnicity_dfs, ethnicities)

#top zip code bar chart
def graph_top_zips(top_zips, chart_colors, saveloc):
    zips = pd.DataFrame(top_zips)
    zips.fillna(0, inplace=True)
    zips['total'] = zips['White'] + zips['American Indian or Alaska Native'] + zips['Asian'] + zips['Black or African American']+ zips['Puerto Rican'] + zips['Hispanic']
    zips = pd.DataFrame(zips).sort_values('total')    
    zips.drop('total', axis=1,inplace=True)

    ax = zips.plot(kind='barh', stacked=True, color=chart_colors)
    plt.yticks(fontsize = 12)
    ax.set_xlabel('Number of Loans')
    ax.set_title('Top 5 Zip Codes for Count of Loans')
    plt.savefig(saveloc, bbox_inches='tight')

graph_top_zips(top_zips, chart_colors, '../images/top_zip_loancount.png')

#top counties for each ethnicity
def top_county(ethnicity_dfs, ethnicities):
    '''
    Counts the number of loans for each Ethnicity group, sorts by top 5.

    Returns: Dictionary where Keys are the Ethnicities and values are a dataframe of top 5
    zipcodes and the count of loans from each zip.
    '''
    top_dict = {}
    for eth, df in zip(ethnicities, ethnicity_dfs):
        count_counties = df.groupby(['county']).count()['LoanAmount']
        sort_counties = count_counties.sort_values(ascending=False).head(5)
        top_dict[eth]= sort_counties
    return top_dict

top_county = top_county(ethnicity_dfs, ethnicities)

#top county bar chart
def graph_top_counties(top_county, chart_colors, saveloc):
    counties = pd.DataFrame(top_county)
    counties.fillna(0, inplace=True)
    counties['total'] = counties['White'] + counties['American Indian or Alaska Native'] + counties['Asian'] + \
        counties['Black or African American']+ counties['Puerto Rican'] + counties['Hispanic']
    counties = pd.DataFrame(counties).sort_values('total')    
    counties.drop('total', axis=1,inplace=True)

    ax = counties.plot(kind='barh', stacked=True, color=chart_colors)
    plt.yticks(fontsize = 12)
    ax.set_xlabel('Number of Loans')
    ax.set_title('Top 5 Counties for Loans')
    plt.savefig(saveloc, bbox_inches='tight')

graph_top_counties(top_county, chart_colors, '../images/top_county_loancount.png')

#top county total loan amount
def top_county_sum(ethnicity_dfs, ethnicities):
    '''
    Counts the number of loans for each Ethnicity group, sorts by top 5.

    Returns: Dictionary where Keys are the Ethnicities and values are a dataframe of top 5
    zipcodes and the count of loans from each zip.
    '''
    top_dict = {}
    for eth, df in zip(ethnicities, ethnicity_dfs):
        count_counties = df.groupby(['county']).sum()['LoanAmount']
        sort_counties = count_counties.sort_values(ascending=False).head(5)
        top_dict[eth]= sort_counties
    return top_dict

top_county_sum = top_county_sum(ethnicity_dfs, ethnicities)

#top county bar chart
graph_top_counties(top_county_sum, chart_colors, '../images/top_county_loansum.png')


#create list of population from demographics data
demographic_eth_cols = ['NH Whites','Hispanic','NH Am Indian/Native','NH Asian','NH Afr Am']
total_demographics = [sum(demographics_18[x]) for x in demographic_eth_cols]
other = sum(demographics_18['NH Two or more']) + sum(demographics_18['NH Native Hawaiian/other'])
total_demographics.append(other)

#demographics graph
def graph_demographics(total_demographics, ethnicities, saveloc):
    fig, ax = plt.subplots(1,figsize=(12,4))
    ethnicities_dem = ethnicities[:-1]
    ethnicities_dem=np.append(ethnicities_dem, 'Other')
    plt.bar(ethnicities_dem, total_demographics, color=chart_colors)
    plt.xticks(rotation=45, fontsize=12)
    ax.set_yscale('log')
    ax.set_xlabel('Ethnicity', fontsize=16)
    ax.set_ylabel('Millions of People', fontsize=16)
    ax.set_title('Distribution of Ethnicity in Colorado', fontsize=18)
    plt.savefig(saveloc, bbox_inches='tight')

graph_demographics(total_demographics, ethnicities, '../images/demographics.png')

#demographics for top 8 counties

#pull out top counties
top_counties_loans= ['Denver County', 'El Paso County', 'Jefferson County','Arapahoe County','Larimer County','Adams County','Douglas County','Weld County']
#create list of county rows
county_rows = [demographics_18[demographics_18['CTYNAME'] == x] for x in top_counties_loans]

#iterate through list of counties and pull out populations for each ethnicity
demographics_by_county =[]
for i in range(len(county_rows)):
    county_list = []
    for x in demographic_eth_cols:
        county_list.append(int(county_rows[i][x].values))
    
    other = county_rows[i]['NH Two or more'].values + county_rows[i]['NH Native Hawaiian/other'].values
    county_list.append(int(other))
    demographics_by_county.append(county_list)


#### issue?
#demographics by county
top_counties_loans= ['Denver County', 'El Paso County', 'Jefferson County','Arapahoe County','Larimer County','Adams County','Douglas County','Weld County']
county_rows = [demographics_18[demographics_18['CTYNAME'] == x] for x in top_counties_loans]

#iterate through list of counties and pull out populations for each ethnicity
demographics_county_ethnicity =[]
for eth in demographic_eth_cols:
    ethnicity_counts = []
    for i in range(len(county_rows)):
        ethnicity_counts.append(int(county_rows[i][eth].values))
    demographics_county_ethnicity.append(ethnicity_counts)

other_dem = []  
for i in range(len(county_rows)):
    other = county_rows[i]['NH Two or more'].values + county_rows[i]['NH Native Hawaiian/other'].values
    other_dem.append(int(other))
demographics_county_ethnicity.append(other_dem)
demographics_county_ethnicity


###BETTER THAN ABOVE
#demographics by county
top_counties_loans= ['Denver County', 'El Paso County', 'Jefferson County','Arapahoe County','Larimer County','Adams County','Douglas County','Weld County']
county_rows = [demographics_18[demographics_18['CTYNAME'] == x] for x in top_counties_loans]

#iterate through list of counties and pull out populations for each ethnicity
demographics_by_county =[]
for i in range(len(county_rows)):
    county_list = []
    for eth in demographic_eth_cols:
        county_list.append(int(county_rows[i][eth].values))
    
    other = county_rows[i]['NH Two or more'].values + county_rows[i]['NH Native Hawaiian/other'].values
    county_list.append(int(other))
    demographics_by_county.append(county_list)
demographics_by_county[::-1]

#top county bar chart
def graph_top_county_demographics(demographics_by_county, ethnicities, top_counties_loans, chart_colors, saveloc):
    ethnicities_dem = ethnicities[:-1]
    ethnicities_dem=np.append(ethnicities_dem, 'Other')
    #demographics_by_county=reversed(demographics_by_county)
    fig, ax = plt.subplots(1,figsize=(10,6))
    for x in range(len(demographics_by_county)):
        plt.barh(top_counties_loans[x], demographics_by_county[x], label=top_counties_loans[x], color=chart_colors)
        
    ax.set_xlabel('Number of People', fontsize=17)
    ax.set_title('Demographics of Top 8 Counties for Loans', fontsize=18)
    plt.legend(ethnicities_dem)
    plt.savefig(saveloc, bbox_inches='tight')

graph_top_county_demographics(demographics_by_county, ethnicities, top_counties_loans, chart_colors, '../images/top_county_loancount.png')


#scatter comparison of Jobs Retained to Loan Amount by ethnicity
ethnicity_dfs_job_comparison = [x.dropna(subset=['JobsRetained']) for x in ethnicity_dfs]

loan_by_ethnicity = [list(x['LoanAmount'].values) for x in ethnicity_dfs_job_comparison]
jobs_retained_by_ethnicity = [list(x['JobsRetained'].values) for x in ethnicity_dfs_job_comparison]

## avg amount of loan compared to jobs retained by ethnicity
avg_loan_by_ethnicity = [round(x['LoanAmount'].mean(),2) for x in ethnicity_dfs_job_comparison]
avg_jobs_retained_by_ethnicity = [round(x['JobsRetained'].mean(),3) for x in ethnicity_dfs_job_comparison]

def zip_lists(list1,list2):
    zipped = [(x,y) for x,y in zip(list1, list2)]
    return zipped
avg_jobs_loans = zip_lists(avg_jobs_retained_by_ethnicity, avg_loan_by_ethnicity)


def graph_job_loanamount(loan_by_ethnicity, jobs_retained_by_ethnicity, avg_jobs_loans, chart_colors, ethnicities, saveloc):
    fig, ax = plt.subplots(1, figsize=(10,6))

    for i in range(len(loan_by_ethnicity)):
        ax.scatter(loan_by_ethnicity[i], jobs_retained_by_ethnicity[i], color=chart_colors[i], label=ethnicities[i])


    ax.set_ylabel('Jobs Retained', fontsize=16)
    ax.set_xlabel('Amount of Loan in USD', fontsize=16)
    ax.set_title('Loan Amount vs Jobs Retained by Ethnicity')
    plt.ylim([0,125])
    plt.legend()    



if __name__ == '__main__':
   print('hi')
