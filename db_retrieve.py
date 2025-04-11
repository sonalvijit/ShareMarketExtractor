from models import get_share_data
from argparse import ArgumentParser

def main():
     parser = ArgumentParser(description="Retrieve share data from the database.")
     parser.add_argument("-d", "--date", type=str, required=True, help="Date in the format dd-mm-yyyy")

     args = parser.parse_args()
     date = args.date
     a = get_share_data(date=date, epoch=False)
     for i in a[0]:
          res = f"{i}\t\t\t{a[0][i]["prices"][0]["share_value"]}\t\t\t{a[0][i]["prices"][0]["share_pts"]}\t\t\t{a[0][i]["prices"][0]["G_N_L"]}"
          print(res)

if __name__ == "__main__":
     main()