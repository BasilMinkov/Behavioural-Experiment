import os
import expyriment
import csv

if __name__ == "__main__":
    data_folder = os.getcwd() + os.sep + 'data'
    with open('output.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for subject in os.listdir(data_folder):
            subject_array = expyriment.misc.data_preprocessing.read_datafile(data_folder + os.sep + subject)
            writer.writerows(subject_array[0])