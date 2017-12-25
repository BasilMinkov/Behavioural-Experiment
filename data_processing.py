"""This code is used to prepare data returned by expyriment package to be proceeded in R"""

import os
import expyriment
import csv

if __name__ == "__main__":
    counter = 1
    data_folder = os.getcwd() + os.sep + 'data'
    with open('output.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        listed_dir = os.listdir(data_folder)
        len_listed_data = len(listed_dir)
        print(listed_dir)
        print(len_listed_data)
        for subject in listed_dir:
            if subject[0:3] == "run":
                print(data_folder + os.sep + subject)
                subject_array = expyriment.misc.data_preprocessing.read_datafile(data_folder + os.sep + subject)
                new_array = [subject_array[0][i][:5] for i in range(len(subject_array[0]))]
                for i in new_array:
                    i[0] = str(counter)
                print(new_array)
                writer.writerows(new_array)
            counter += 1