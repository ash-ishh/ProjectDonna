import argparse
import sentimental_analysis as sa

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("train_dir",help="provide training directory")
    args = parser.parse_args()
    train_dir = args.train_dir

    allDocuments , allLabels = sa.pre_process(train_dir)
    sa.train(allDocuments,allLabels)
