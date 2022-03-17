import cv2
import mediapipe as mp
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


def calculate_angle(a, b, c):
    a = np.array(a)  # First
    b = np.array(b)  # Mid
    c = np.array(c)  # End

    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - \
        np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)

    if angle > 180.0:
        angle = 360-angle

    return angle


def reduceResolution():
    cap.set(3, 480)
    cap.set(4, 360)


# VIDEO FEED
cap = cv2.VideoCapture('LowResExercises/narrow-pushups.mp4')

# EXERCISE: 0 = squat, 1 = pushup, 2 = situp
exercise = 0

# change resolution
# reduceResolution()

# Curl counter variables
counter = 0
stage = None

# Setup mediapipe instance
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()

        # Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # Make detection
        results = pose.process(image)

        # Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Extract landmarks
        # if squat
        if exercise == 0:
            try:
                landmarks = results.pose_landmarks.landmark

                # Get coordinates
                # A good squat requires a depth of around 90 degrees on the knees and a wide stance with the feet wider than shoulder width
                # Feet coordinates
                left_heel = [landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].y]
                right_heel = [landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value].x,
                              landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value].y]
                left_toe = [landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].y]
                right_toe = [landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].x,
                             landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].y]

                # Knee coordinates
                left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                              landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]

                # Hip Coordinates
                left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                             landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]

                # shoulder coordinates
                left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                 landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                                  landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]

                # Calculate angle
                squat_angle = calculate_angle(left_hip, left_knee, left_heel)
                foot_angle = calculate_angle(left_toe, left_heel, right_heel)

                # Visualize angle
                cv2.putText(image, str("{:.2f}".format(squat_angle)),
                            tuple(np.multiply(left_knee, [
                                  640, 480]).astype(int)),
                            cv2.FONT_HERSHEY_PLAIN, 0.5, (255,
                                                          255, 255), 2, cv2.LINE_AA
                            )

                # squat counter logic
                if squat_angle < 100:
                    stage = "down"
                if squat_angle > 170 and stage == 'down':
                    stage = "up"
                    counter += 1
                    print(counter)

            except:
                pass
        # if pushup
        if exercise == 1:
            try:
                landmarks = results.pose_landmarks.landmark

                # Get coordinates
                # A good pushup should aim to bend the elbows at or below a 90 degree angle. Since the basis is the elbow angle, both the wide and close grip pushup variations can be accounted for

                # hand coordinates
                left_hand = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                right_hand = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                              landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

                # elbow coordinates
                left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                              landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                               landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]

                # shoulder coordinates
                left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                 landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                                  landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]

                # hip coordinates
                left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                             landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                # Calculate angle
                elbow_angle = calculate_angle(
                    left_hand, left_elbow, left_shoulder)
                # Check Pushup Variation
                arm_angle = calculate_angle(
                    left_elbow, left_shoulder, left_hip)

                # Visualize elbow angle
                cv2.putText(image, str("{:.2f}".format(elbow_angle)),
                            tuple(np.multiply(left_elbow, [
                                  640, 480]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,
                                                            255, 255), 2, cv2.LINE_AA
                            )

                # Visualize arm angle
                # cv2.putText(image, str("{:.2f}".format(arm_angle)),
                #             tuple(np.multiply(left_shoulder,
                #                   [640, 480]).astype(int)),
                #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,
                #                                             255, 255), 2, cv2.LINE_AA
                #             )

                # pushup counter logic
                if elbow_angle < 90:
                    stage = "down"
                if elbow_angle > 150 and stage == 'down':
                    stage = "up"
                    counter += 1
                    print(counter)

            except:
                pass

        # Render curl counter
        # Setup status box
        cv2.rectangle(image, (0, 0), (225, 73), (245, 117, 16), -1)

        # Rep data
        cv2.putText(image, 'REPS', (15, 12),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(image, str(counter),
                    (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

        # Stage data
        cv2.putText(image, 'STAGE', (65, 12),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(image, stage,
                    (60, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

        # Render detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(
                                      color=(245, 117, 66), thickness=2, circle_radius=2),
                                  mp_drawing.DrawingSpec(
                                      color=(245, 66, 230), thickness=2, circle_radius=2)
                                  )

        cv2.imshow('Mediapipe Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
