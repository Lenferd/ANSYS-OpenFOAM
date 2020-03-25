import pandas as pd
from argparse import ArgumentParser


def parse_file(args):
    df = pd.read_csv(args.input_file, sep='\t')
    head = df.head()
    if args.row_value not in head:
        print("{} not found!".format(args.row_value))
    if args.column_value not in head:
        print("{} not found!".format(args.column_value))
    if args.value not in head:
        print("{} not found!".format(args.value))
    table = pd.pivot_table(df, values=args.value, index=args.row_value,
                           columns=args.column_value)
    print(table)
    table.to_csv(args.output_file)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("input_file", type=str, help="File to read")

    parser.add_argument("-rv", "--row_value", type=str, help="Column, which will be used for rows in table",
                        required=True)
    parser.add_argument("-cv", "--column_value", type=str, help="Column, which will be used for column in table",
                        required=True)
    parser.add_argument("-v", "--value", type=str, help="Value, values of which will be inside table",
                        required=True)

    parser.add_argument("-o", "--output_file", type=str, help="Output file",
                        required=True)
    args = parser.parse_args()
    parse_file(args)
