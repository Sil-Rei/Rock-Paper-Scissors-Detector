import HandTrackingGitHubEdition as htm
import cv2

cap = cv2.VideoCapture(0)


detector = htm.HandDetector()


def get_vector_distance(cords1, cords2):
    # Get vector
    cords1 = [cords1[1], cords1[2]]
    cords2 = [cords2[1], cords2[2]]
    cords_of_vector = [cords2[0] - cords1[0], cords2[1] - cords1[1]]
    vector_distance = (cords_of_vector[0] ** 2 + cords_of_vector[1] ** 2) ** 0.5

    return vector_distance

# Function to quickly debug with a example
def detectThumbsUp(img, cordsOfThumbTip, cordsOfIndexTip, cordsOfMiddleTip, draw=False):
    distance_thumb_to_index = get_vector_distance(cordsOfThumbTip, cordsOfIndexTip)
    distanceIndexToMiddle = get_vector_distance(cordsOfIndexTip, cordsOfMiddleTip)

    if draw:
        if distance_thumb_to_index > distanceIndexToMiddle * 3:
            cv2.line(img, [cordsOfThumbTip[1], cordsOfThumbTip[2]], [cordsOfIndexTip[1], cordsOfIndexTip[2]],
                     (0, 255, 0), 5)
        else:
            cv2.line(img, [cordsOfThumbTip[1], cordsOfThumbTip[2]], [cordsOfIndexTip[1], cordsOfIndexTip[2]],
                     (0, 0, 255), 5)

    # print(distance_thumb_to_index)
    return distance_thumb_to_index > distanceIndexToMiddle * 3


def detect_finger_bent(cord_tip, cord_dip, cord_pip, cord_mcp):
    # Compares the sum of the distances of each segment of a finger with the distance of the tip and the finger base

    sum_of_distance = get_vector_distance(cord_tip, cord_dip) + get_vector_distance(cord_dip, cord_pip) \
                    + get_vector_distance(cord_pip, cord_mcp)

    distance_end_to_end = get_vector_distance(cord_tip, cord_mcp)

    return sum_of_distance > distance_end_to_end * 1.5


def detect_whole_fingers_bent(lmList):
    index_finger = detect_finger_bent(lmList[8], lmList[7], lmList[6], lmList[5])
    middle_finger = detect_finger_bent(lmList[12], lmList[11], lmList[10], lmList[9])
    ring_finger = detect_finger_bent(lmList[16], lmList[15], lmList[14], lmList[13])
    pinky = detect_finger_bent(lmList[20], lmList[19], lmList[18], lmList[17])

    return index_finger, middle_finger, ring_finger, pinky


def detectRPS(lmList):
    index_finger, middle_finger, ring_finger, pinky = detect_whole_fingers_bent(lmList)

    if pinky and ring_finger and not index_finger and not middle_finger:
        print("Scissors")
    if pinky and ring_finger and middle_finger and index_finger:
        print("Rock")
    if not pinky and not ring_finger and not middle_finger and not index_finger:
        print("Paper")


while True:
    success, img = cap.read()
    img = detector.find_hands(img)
    landmark_list = detector.find_position(img, 0)

    if len(landmark_list) != 0:
        # print(detectThumbsUp(img, lmList[4], lmList[8], lmList[12], True))

        # print(detect_finger_bent(lmList[8], lmList[7], lmList[6], lmList[5]))

        # index_finger, middle_finger, ring_finger, pinky = detect_whole_fingers_bent(lmList)

        # print(f"index_finger: {index_finger}\nmiddle_finger: {middle_finger}\nring_finger: {ring_finger}\nPinky: {pinky}\n")

        detectRPS(landmark_list)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
