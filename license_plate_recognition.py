import cv2
import numpy as np
from paddleocr import PaddleOCR
from datetime import datetime

# Initialize PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang='en')


def process_video(video_path):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Error: Could not open video file {video_path}")
        return

    # Initialize video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (640, 480))
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = ocr.ocr(rgb_frame, cls=True)

        detected_text = ""
        if results:
            for line in results:
                if line:
                    for word_info in line:
                        if word_info and len(word_info) > 1:
                            text, box = word_info[1][0], word_info[0]
                            detected_text += text + " "
                            cv2.polylines(frame, [np.int32(box)], isClosed=True, color=(0, 255, 0), thickness=2)
                            cv2.putText(frame, text, (int(box[0][0]), int(box[0][1]) - 10),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cv2.putText(frame, current_time, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 255), 2)
        cv2.putText(frame, 'License Plate: ', (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2)
        cv2.putText(frame, detected_text.strip(), (10, 250), cv2.FONT_HERSHEY_SIMPLEX, 2.5, (0, 255, 0), 8)

        # Save frame to video
        out.write(cv2.resize(frame, (640, 480)))

        # Optional: Uncomment to display (if GUI works after fix)
        cv2.imshow('License Plate Recognition', cv2.resize(frame, (640, 480)))
        if cv2.waitKey(1) & 0xFF == ord('q'):
             break

    cap.release()
    out.release()  # Release video writer
    cv2.destroyAllWindows()


if __name__ == '__main__':
    process_video('test1.mp4')