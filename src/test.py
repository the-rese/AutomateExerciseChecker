from pushups import PushupClass
from squats import SquatClass
from openpyxl.workbook import Workbook
import pandas as pd
import os

FOLDER_PATH = r'C:\\Users\\Therese Bolabola\\OneDrive\\Desktop\\ExerciseTracker\\test\\squats'

name_list = []
counter_list = []
correct_rep_list = []
st_list = []
rom_list = []
ave_depth_list = []


def exerciseRater(dir, name_list, counter_list, correct_rep_list, st_list, rom_list, ave_depth_list):
    fileNames = os.listdir(dir)
    for fileName in fileNames:
        gender = fileName[0]
        # create object or instance for squat Class
        filepath = os.path.abspath(os.path.join(dir, fileName))
        # print(fileName)
        # print(filepath)
        squat_instance = SquatClass(filepath, gender)
        # test if mediapipe still works
        squat_instance.rateExercise()
        squat_instance.summarizeResult()
        result = squat_instance.getSummary()

        name_list.append(fileName)

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
    exerciseRater(FOLDER_PATH, name_list, counter_list,
                  correct_rep_list, st_list, rom_list, ave_depth_list)
    columns = ["Student Name", "Total Num of Rep", "Correct Num of Rep", "Standardize Test",
               "Range of Motion", "Average Angle Depth"]

    df = pd.DataFrame(list(zip(name_list, counter_list, correct_rep_list,
                      st_list, rom_list, ave_depth_list)), columns=columns)
    print(df)
    out_filename = 'squat-summary.xlsx'
    out_path = 'C:\\Users\\Therese Bolabola\\OneDrive\\Desktop\\ExerciseTracker\\results\\'+out_filename
    df.to_excel(out_path, sheet_name="PE Section")


if __name__ == "__main__":
    main()
