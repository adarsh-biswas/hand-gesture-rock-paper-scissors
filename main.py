import cv2
import mediapipe as mp
import random
import time

# Initialize MediaPipe Hand module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Define gestures
GESTURES = {
    "rock": [0, 0, 0, 0, 0],  # All fingers down
    "paper": [1, 1, 1, 1, 1],  # All fingers up
    "scissors": [0, 1, 1, 0, 0],  # Index and middle fingers up
}

def detect_gesture(hand_landmarks):
    finger_states = []
    tip_ids = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky
    for i, tip_id in enumerate(tip_ids):
        # Check if a finger is up
        if i == 0:  # Thumb
            finger_states.append(
                hand_landmarks.landmark[tip_id].x < hand_landmarks.landmark[tip_id - 1].x
            )
        else:  # Other fingers
            finger_states.append(
                hand_landmarks.landmark[tip_id].y < hand_landmarks.landmark[tip_id - 2].y
            )
    for gesture, state in GESTURES.items():
        if finger_states == state:
            return gesture
    return "unknown"

# Game logic
def play_game():
    cap = cv2.VideoCapture(0)
    print("Starting Rock-Paper-Scissors game!")
    print("Show your gesture when prompted.")
    time.sleep(2)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)  # Flip the frame horizontally
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb_frame)

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                user_move = detect_gesture(hand_landmarks)
                if user_move != "unknown":
                    # Get computer choice
                    computer_move = random.choice(list(GESTURES.keys()))
                    print(f"User: {user_move} | Computer: {computer_move}")

                    # Determine the winner
                    if user_move == computer_move:
                        result_text = "It's a Tie!"
                    elif (user_move == "rock" and computer_move == "scissors") or \
                         (user_move == "paper" and computer_move == "rock") or \
                         (user_move == "scissors" and computer_move == "paper"):
                        result_text = "You Win!"
                    else:
                        result_text = "You Lose!"

                    # Display result on the screen
                    cv2.putText(frame, result_text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    print(result_text)
                    time.sleep(2)

        cv2.imshow("Rock-Paper-Scissors", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if _name_ == "_main_":
    play_game()
