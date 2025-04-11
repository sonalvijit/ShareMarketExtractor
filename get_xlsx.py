from xlsx import save
from argparse import ArgumentParser
from models import get_share_data

def main():
     parser = ArgumentParser(description="Save share data from the database.")
     parser.add_argument("-d", "--date", type=str, required=True, help="Date in the format dd-mm-yyyy")

     args = parser.parse_args()
     date = args.date
     a = get_share_data(date=date)
     save(data=a)

if __name__=="__main__":
     main()