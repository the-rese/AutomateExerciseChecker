from pushup import PushupClass
from openpyxl.workbook import Workbook
import pandas as pd

videoname = 'videos/narrow-pushups.mp4'

# create object or instance for Pushup Class
pushup_instance = PushupClass(videoname)
# test if mediapipe still works
pushup_instance.rateExercise()
pushup_instance.summarizeResult()
result = pushup_instance.getSummary()

for item in result:
    if item[0]:
        # total num of reps
        counter = item[0]
        # correct num of good reps
        correct_reps = item[1]
        # standardize test
        st = item[2]
        # range of motion
        rom = item[3]
        # ave angle depth
        ave_depth = item[4]
        print(item[4])

columns = ["Student Name", "Exercise", "Total Num of Rep", "Correct Num of Rep", "Standardize Test",
           "Range of Motion", "Average Angle Depth", "Additional Info"]

df = pd.DataFrame(
    list(zip([videoname], ["Push ups"], [counter], [correct_reps], [st], [rom], [ave_depth], ["None"])), columns=columns)
print(df)

filename = videoname[16:-4] + '.xlsx'
out_path = 'C:\\Users\\Therese Bolabola\\OneDrive\\Desktop\\ExerciseTracker\\summary\\'+filename

df.to_excel(out_path, sheet_name="PE Section")
