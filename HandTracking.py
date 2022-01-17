import cv2
import mediapipe as mp


class HandDetector:
    def __init__(self, mode=False, max_hand_number=2, detection_conf=0.5, track_conf=0.5):

        # Initialize MediaPipe settings
        self.mode = mode
        self.maxHandNum = max_hand_number
        self.detectionConf = detection_conf
        self.trackConf = track_conf

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(mode, max_hand_number, detection_conf, track_conf)
        self.mp_drawings = mp.solutions.drawing_utils

    def find_hands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        self.results = self.hands.process(imgRGB)

        # print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for hand_land_marks in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_drawings.draw_landmarks(img, hand_land_marks, self.mp_hands.HAND_CONNECTIONS)

        return img

    def find_position(self, img, hand_number=0):

        landmark_list = []

        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[hand_number]

            for id, landmark in enumerate(myHand.landmark):
                height, width, channels = img.shape
                cx, cy = int(landmark.x * width), int(landmark.y * height)

                #ID of finger part, see list of ID´s on mediapipe doc
                landmark_list.append([id, cx, cy])

        return landmark_list


def main():
    cap = cv2.VideoCapture(0)

    detector = HandDetector()

    while True:
        success, img = cap.read()
        img = detector.find_hands(img)
        landmark_list = detector.find_position(img, 0)

        if len(landmark_list) != 0:
            print(landmark_list[1])

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
