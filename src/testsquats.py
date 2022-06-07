from squats import SquatClass
from openpyxl.workbook import Workbook
import pandas as pd
import os

FOLDER_PATH = r'C:\\Users\\Therese Bolabola\\OneDrive\\Desktop\\ExerciseTracker\\test\\check'

gender_list = []
name_list = []
counter_list = []
correct_rep_list = []
st_list = []
rom_list = []
ave_depth_list = []


def exerciseRater(dir, gender_list, name_list, counter_list, correct_rep_list, st_list, rom_list, ave_depth_list):
    fileNames = os.listdir(dir)
    for fileName in fileNames:
        gender = fileName[0]
        filepath = os.path.abspath(os.path.join(dir, fileName))
        # create object or instance for squat Class
        instance = SquatClass(filepath, gender)
        # test if mediapipe still works
        instance.rateExercise()
        instance.summarizeResult()
        result = instance.getSummary()

        gender_list.append(gender)
        name_list.append(fileName[2:-4])

        for item in result:
            # total num of reps
            counter_list.append(item[0])
            # correct num of good reps
            correct_rep_list.append(item[1])
            # standardize test
            st_list.append(item[2])
            # range of motion
            rom_list.append(item[3])
            # ave angle depth
            ave_depth_list.append(item[4])


def main():
    exerciseRater(FOLDER_PATH, gender_list, name_list, counter_list,
                  correct_rep_list, st_list, rom_list, ave_depth_list)
    columns = ["Gender", "Student Name", "Total Num of Rep", "Correct Num of Rep", "Standardize Test",
               "Range of Motion", "Average Angle Depth"]

    df = pd.DataFrame(list(zip(gender_list, name_list, counter_list, correct_rep_list,
                      st_list, rom_list, ave_depth_list)), columns=columns)
    print(df)
    out_filename = 'lisondraqqqq-demo-summary.xlsx'
    out_path = 'C:\\Users\\Therese Bolabola\\OneDrive\\Desktop\\ExerciseTracker\\results\\'+out_filename
    df.to_excel(out_path, sheet_name="PE Section")


if __name__ == "__main__":
    main()
