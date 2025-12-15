import cv2
import face_recognition
import pickle
import os

# Importing student images
folderPath = 'Images'
pathList = os.listdir(folderPath)
print("Found images:", pathList)

encodeListKnown = []
studentIds = []

print("Encoding Started ...")

for path in pathList:
    try:
        # --- THE FIX: Use the library's native loader ---
        # This bypasses OpenCV and loads it exactly as dlib requires (RGB, 8-bit)
        img_path = os.path.join(folderPath, path)
        img = face_recognition.load_image_file(img_path)

        # Get the encodings
        encodings = face_recognition.face_encodings(img)

        if len(encodings) > 0:
            encodeListKnown.append(encodings[0])
            studentIds.append(os.path.splitext(path)[0])
            print(f"✅ Success: {path}")
        else:
            print(f"⚠️ Skipping {path}: No face detected. (Try a clearer photo)")

    except Exception as e:
        print(f"❌ Error with {path}: {e}")

# Only save if we actually succeeded
if len(encodeListKnown) == 0:
    print("CRITICAL: No valid encodings generated. File NOT saved.")
else:
    encodeListKnownWithIds = [encodeListKnown, studentIds]
    print("Encoding Complete")

    # Saving the file
    file = open("EncodeFile.p", 'wb')
    pickle.dump(encodeListKnownWithIds, file)
    file.close()
    print("File Saved as 'EncodeFile.p'")