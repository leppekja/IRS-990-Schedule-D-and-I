import requests
import read_990 as rd 
import pandas as pd 
import argparse


def get_data(index_csv, verbose=False, start=0, end=150):
    '''
    Read AWS index file and aggregate Schedule I
    and sponsoring organization forms.
    Input: AWS Index CSV
    Output: 2 dataframes, one with sponsoring org details,
            one with grantee data
    '''
    index = pd.read_csv(index_csv)
    # collect only 990s
    # initially RETURN_TYPE is stored as text; after converting to DataFrame,
    # it is considered a numpy int64, which may cause a warning if you convert
    # a selection of forms from the csv to a DataFrame and back to a CSV. 
    index = index.loc[index['RETURN_TYPE'] == '990'].OBJECT_ID.tolist()
    sponsors = pd.DataFrame()
    grants_made = pd.DataFrame()
    daf_object_ids = []
    for form in index[start:end]:
        link = "https://s3.amazonaws.com/irs-form-990/{}_public.xml".format(str(form))
        tree = rd.read_form(document=link, download=True)
        #confirm DAF
        if rd.confirm_daf_fund(tree):
            daf_object_ids.append(form)
            if verbose:
                print("DAF Confirmed. Getting data...")
                print(form)
            #get org headers
            sponsor = rd.get_form_headers(tree)
            #get schedule D
            daf_details = rd.get_schedule_d(tree)
            #combine headers and schedule D
            sponsor_details = pd.DataFrame([sponsor, daf_details])
            #get schedule I
            grantees = rd.get_schedule_i(tree)
            #clean schedule I
            grantees = rd.clean_daf_grantee_data(grantees, sponsor['NAME']) 
            #append dataframes with org info and grantees (I)
            sponsors = sponsors.append(sponsor_details)
            grants_made = grants_made.append(grantees)
        else:
            pass

    grants_made.to_csv("Grantees.csv")
    sponsors.to_csv("Sponsors.csv")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            description='Read an AWS IRS 990 Index and download data \
                        associated with a donor-advised fund')
    parser.add_argument('-file',type=str,
                    help='index file to use')
    parser.add_argument('-start',type=int, default=0,
                    help='object id index to start with')
    parser.add_argument('-end',type=int, default=150,
                    help='object id index to end with')
    parser.add_argument('--verbose', action="store_true",
                    help="whether to print progress")
    args = parser.parse_args()   
    get_data(args.file, args.verbose, args.start, args.end)