import cv2
import mediapipe as mp
import random
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

GESTURES = {
    "rock": [0, 0, 0, 0, 0],
    "paper": [1, 1, 1, 1, 1],
    "scissors": [0, 1, 1, 0, 0],
}

def detect_gesture(hand_landmarks):
    finger_states = []
    tip_ids = [4, 8, 12, 16, 20]
    for i, tip_id in enumerate(tip_ids):
        if i == 0:
            finger_states.append(
                hand_landmarks.landmark[tip_id].x < hand_landmarks.landmark[tip_id - 1].x
            )
        else:
            finger_states.append(
                hand_landmarks.landmark[tip_id].y < hand_landmarks.landmark[tip_id - 2].y
            )
    for gesture, state in GESTURES.items():
        if finger_states == state:
            return gesture
    return "unknown"

def play_game():
    cap = cv2.VideoCapture(0)
    print("Starting Rock-Paper-Scissors game!")
    print("Show your gesture when prompted.")
    time.sleep(2)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb_frame)

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                user_move = detect_gesture(hand_landmarks)
                if user_move != "unknown":
                    computer_move = random.choice(list(GESTURES.keys()))
                    print(f"User: {user_move} | Computer: {computer_move}")

                    if user_move == computer_move:
                        result_text = "It's a Tie!"
                    elif (user_move == "rock" and computer_move == "scissors") or \
                         (user_move == "paper" and computer_move == "rock") or \
                         (user_move == "scissors" and computer_move == "paper"):
                        result_text = "You Win!"
                    else:
                        result_text = "You Lose!"

                    cv2.putText(frame, result_text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    print(result_text)
                    time.sleep(2)

        cv2.imshow("Rock-Paper-Scissors", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    play_game()
