import cv2
import yaml
import time
import numpy as np

# Load YAML file
with open("./SPECIESMOSQ.yaml", "r") as f:
    data = yaml.safe_load(f)

print(data)

# Load the images from YAML file paths
aegypti_images = [cv2.imread(img['path'], cv2.IMREAD_GRAYSCALE) for img in data['species']['aegypti']['images']]
pipiens_images = [cv2.imread(img['path'], cv2.IMREAD_GRAYSCALE) for img in data['species']['pipiens']['images']]
albopictus_images = [cv2.imread(img['path'], cv2.IMREAD_GRAYSCALE) for img in data['species']['albopictus']['images']]
vexans_images = [cv2.imread(img['path'], cv2.IMREAD_GRAYSCALE) for img in data['species']['vexans']['images']]
niveus_images = [cv2.imread(img['path'], cv2.IMREAD_GRAYSCALE) for img in data['species']['niveus']['images']]
quinquefasciatus_images = [cv2.imread(img['path'], cv2.IMREAD_GRAYSCALE) for img in data['species']['quinquefasciatus']['images']]
vishnui_images = [cv2.imread(img['path'], cv2.IMREAD_GRAYSCALE) for img in data['species']['vishnui']['images']]
tritaeniorhynchus_images = [cv2.imread(img['path'], cv2.IMREAD_GRAYSCALE) for img in data['species']['tritaeniorhynchus']['images']]

# Check if images are loaded correctly
for i, img in enumerate(aegypti_images):
    if img is None:
        print(f"Failed to load Aedes Aegypti image {i+1}")
        exit()

for i, img in enumerate(pipiens_images):
    if img is None:
        print(f"Failed to load Culex Pipiens image {i+1}")
        exit()

for i, img in enumerate(albopictus_images):
    if img is None:
        print(f"Failed to load Aedes Albopictus image {i+1}")
        exit()

for i, img in enumerate(vexans_images):
    if img is None:
        print(f"Failed to load Aedes Vexans image {i+1}")
        exit()

for i, img in enumerate(niveus_images):
    if img is None:
        print(f"Failed to load Aedes Niveus image {i+1}")
        exit()

for i, img in enumerate(quinquefasciatus_images):
    if img is None:
        print(f"Failed to load Culex Quinquefasciatus image {i+1}")
        exit()

for i, img in enumerate(vishnui_images):
    if img is None:
        print(f"Failed to load Culex Vishnui image {i+1}")
        exit()

for i, img in enumerate(tritaeniorhynchus_images):
    if img is None:
        print(f"Failed to load Culex Tritaeniorhynchus image {i+1}")
        exit()

# Initialize ORB detector
orb = cv2.ORB_create()

# Compute ORB descriptors for the reference images
descriptors_aegypti = [orb.detectAndCompute(img, None)[1] for img in aegypti_images]
descriptors_pipiens = [orb.detectAndCompute(img, None)[1] for img in pipiens_images]
descriptors_albopictus = [orb.detectAndCompute(img, None)[1] for img in albopictus_images]
descriptors_vexans = [orb.detectAndCompute(img, None)[1] for img in vexans_images]
descriptors_niveus = [orb.detectAndCompute(img, None)[1] for img in niveus_images]
descriptors_quinquefasciatus = [orb.detectAndCompute(img, None)[1] for img in quinquefasciatus_images]
descriptors_vishnui = [orb.detectAndCompute(img, None)[1] for img in vishnui_images]
descriptors_tritaeniorhynchus = [orb.detectAndCompute(img, None)[1] for img in tritaeniorhynchus_images]

# Filter out empty descriptors
descriptors_aegypti = [des for des in descriptors_aegypti if des is not None and len(des) > 0]
descriptors_pipiens = [des for des in descriptors_pipiens if des is not None and len(des) > 0]
descriptors_albopictus = [des for des in descriptors_albopictus if des is not None and len(des) > 0]
descriptors_vexans = [des for des in descriptors_vexans if des is not None and len(des) > 0]
descriptors_niveus = [des for des in descriptors_niveus if des is not None and len(des) > 0]
descriptors_quinquefasciatus = [des for des in descriptors_quinquefasciatus if des is not None and len(des) > 0]
descriptors_vishnui = [des for des in descriptors_vishnui if des is not None and len(des) > 0]
descriptors_tritaeniorhynchus = [des for des in descriptors_tritaeniorhynchus if des is not None and len(des) > 0]

if not descriptors_aegypti:
    print("No descriptors found for Aedes Aegypti images")
    exit()
if not descriptors_pipiens:
    print("No descriptors found for Culex Pipiens images")
    exit()
if not descriptors_albopictus:
    print("No descriptors found for Aedes Albopictus images")
    exit()
if not descriptors_vexans:
    print("No descriptors found for Aedes Vexans images")
    exit()
if not descriptors_niveus:
    print("No descriptors found for Aedes Niveus images")
    exit()
if not descriptors_quinquefasciatus:
    print("No descriptors found for Culex Quinquefasciatus images")
    exit()
if not descriptors_vishnui:
    print("No descriptors found for Culex Vishnui images")
    exit()
if not descriptors_tritaeniorhynchus:
    print("No descriptors found for Culex Tritaeniorhynchus images")
    exit()

# Concatenate descriptors into single arrays
descriptors_aegypti = np.vstack(descriptors_aegypti)
descriptors_pipiens = np.vstack(descriptors_pipiens)
descriptors_albopictus = np.vstack(descriptors_albopictus)
descriptors_vexans = np.vstack(descriptors_vexans)
descriptors_niveus = np.vstack(descriptors_niveus)
descriptors_quinquefasciatus = np.vstack(descriptors_quinquefasciatus)
descriptors_vishnui = np.vstack(descriptors_vishnui)
descriptors_tritaeniorhynchus = np.vstack(descriptors_tritaeniorhynchus)

# Initialize global timer variable
last_display_time = time.time()

# Function to capture image from camera and detect objects
def capture_and_detect():
    global last_display_time
    cap = cv2.VideoCapture(0)
    
    # FLANN parameters
    FLANN_INDEX_LSH = 6
    index_params = dict(algorithm=FLANN_INDEX_LSH, table_number=6, key_size=12, multi_probe_level=1)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)

    # Add descriptors to FLANN index
    flann.add([descriptors_aegypti])
    flann.add([descriptors_pipiens])
    flann.add([descriptors_albopictus])
    flann.add([descriptors_vexans])
    flann.add([descriptors_niveus])
    flann.add([descriptors_quinquefasciatus])
    flann.add([descriptors_vishnui])
    flann.add([descriptors_tritaeniorhynchus])
    flann.train()

    # List of descriptions for each species
    aegypti_descriptions = ["Danger: Dengue", "Danger: Chikungunya", "Danger: Yellow Fever", "Danger: Zika Virus"]
    pipiens_descriptions = ["Danger: West Nile Virus"]
    albopictus_descriptions = ["Danger: Chikungunya", "Danger: Dengue Fever", "Danger: Zika Virus"]
    vexans_descriptions = ["Danger: Dengue Fever", "Danger: Japanese encephalitis"]
    niveus_descriptions = ["Danger: Sylvatic Dengue"]
    quinquefasciatus_descriptions = ["Danger: West Nile Virus", "Danger: St. Louis Encephalitis"]
    vishnui_descriptions = ["Danger: Japanese Encephalitis"]
    tritaeniorhynchus_descriptions = ["Danger: Japanese Encephalitis"]

    aegypti_detected = False
    pipiens_detected = False
    albopictus_detected = False
    vexans_detected = False
    niveus_detected = False
    quinquefasciatus_detected = False
    vishnui_detected = False
    tritaeniorhynchus_detected = False

    aegypti_desc_index = 0
    pipiens_desc_index = 0
    albopictus_desc_index = 0
    vexans_desc_index = 0
    niveus_desc_index = 0
    quinquefasciatus_desc_index = 0
    vishnui_desc_index = 0
    tritaeniorhynchus_desc_index = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the frame to grayscale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect ORB keypoints and descriptors in the frame
        _, des_frame = orb.detectAndCompute(gray_frame, None)

        current_time = time.time()
        
        # Match the descriptors with the reference images
        matches_aegypti = flann.knnMatch(des_frame, descriptors_aegypti, k=2)
        matches_pipiens = flann.knnMatch(des_frame, descriptors_pipiens, k=2)
        matches_albopictus = flann.knnMatch(des_frame, descriptors_albopictus, k=2)
        matches_vexans = flann.knnMatch(des_frame, descriptors_vexans, k=2)
        matches_niveus = flann.knnMatch(des_frame, descriptors_niveus, k=2)
        matches_quinquefasciatus = flann.knnMatch(des_frame, descriptors_quinquefasciatus, k=2)
        matches_vishnui = flann.knnMatch(des_frame, descriptors_vishnui, k=2)
        matches_tritaeniorhynchus = flann.knnMatch(des_frame, descriptors_tritaeniorhynchus, k=2)

        # Apply ratio test for filtering good matches
        good_matches_aegypti = []
        for matches in matches_aegypti:
            if len(matches) >= 2:  # Check if there are at least two matches
                m, n = matches[0], matches[1]  # Get the best and second best matches
                if m.distance < 0.7 * n.distance:
                    good_matches_aegypti.append(m)
        
        good_matches_pipiens = []
        for matches in matches_pipiens:
            if len(matches) >= 2:  # Check if there are at least two matches
                m, n = matches[0], matches[1]  # Get the best and second best matches
                if m.distance < 0.7 * n.distance:
                    good_matches_pipiens.append(m)
        
        # Apply ratio test for filtering good matches
        good_matches_albopictus = []
        for matches in matches_albopictus:
            if len(matches) >= 2:  # Check if there are at least two matches
                m, n = matches[0], matches[1]  # Get the best and second best matches
                if m.distance < 0.7 * n.distance:
                    good_matches_albopictus.append(m)
        
        good_matches_niveus = []
        for matches in matches_niveus:
            if len(matches) >= 2:  # Check if there are at least two matches
                m, n = matches[0], matches[1]  # Get the best and second best matches
                if m.distance < 0.7 * n.distance:
                    good_matches_niveus.append(m)

        # Apply ratio test for filtering good matches
        good_matches_quinquefasciatus = []
        for matches in matches_quinquefasciatus:
            if len(matches) >= 2:  # Check if there are at least two matches
                m, n = matches[0], matches[1]  # Get the best and second best matches
                if m.distance < 0.7 * n.distance:
                    good_matches_quinquefasciatus.append(m)
        
        good_matches_tritaeniorhynchus = []
        for matches in matches_tritaeniorhynchus:
            if len(matches) >= 2:  # Check if there are at least two matches
                m, n = matches[0], matches[1]  # Get the best and second best matches
                if m.distance < 0.7 * n.distance:
                    good_matches_tritaeniorhynchus.append(m)

        # Apply ratio test for filtering good matches
        good_matches_vexans = []
        for matches in matches_vexans:
            if len(matches) >= 2:  # Check if there are at least two matches
                m, n = matches[0], matches[1]  # Get the best and second best matches
                if m.distance < 0.7 * n.distance:
                    good_matches_vexans.append(m)
        
        good_matches_vishnui = []
        for matches in matches_vishnui:
            if len(matches) >= 2:  # Check if there are at least two matches
                m, n = matches[0], matches[1]  # Get the best and second best matches
                if m.distance < 0.7 * n.distance:
                    good_matches_vishnui.append(m)

        # Set a threshold for the number of good matches
        good_matches_threshold = 10
        
        # Handle Aedes Aegypti detection
        if current_time - last_display_time >= 2:
            if len(good_matches_aegypti) > good_matches_threshold and not aegypti_detected:
                print(f"Detected: {data['species']['aegypti']['name']}")
                aegypti_detected = True
                aegypti_desc_index = 0
                last_display_time = current_time

        # Display Aedes Aegypti descriptions
        if aegypti_detected:
            if current_time - last_display_time >= 2:
                print(aegypti_descriptions[aegypti_desc_index])
                aegypti_desc_index += 1
                last_display_time = current_time
                if aegypti_desc_index >= len(aegypti_descriptions):
                    aegypti_detected = False
                    aegypti_desc_index = 0

        if current_time - last_display_time >= 2:
            if len(good_matches_pipiens) > good_matches_threshold and not pipiens_detected:
                print(f"Detected: {data['species']['aegypti']['name']}")
                pipiens_detected = True
                pipiens_desc_index = 0
                last_display_time = current_time

        # Display Aedes Aegypti descriptions
        if pipiens_detected:
            if current_time - last_display_time >= 2:
                print(pipiens_descriptions[pipiens_desc_index])
                pipiens_desc_index += 1
                last_display_time = current_time
                if pipiens_desc_index >= len(pipiens_descriptions):
                    pipiens_detected = False
                    pipiens_desc_index = 0

        # Handle Aedes Albopictus detection
        if current_time - last_display_time >= 2:
            if len(good_matches_albopictus) > good_matches_threshold and not albopictus_detected:
                print (f"Detected: {data['species']['albopictus']['name']}")
                albopictus_detected = True
                albopictus_desc_index = 0
                last_display_time = current_time

        # Display Aedes Albopictus descriptions
        if albopictus_detected:
            if current_time - last_display_time >= 2:
                print(albopictus_descriptions[albopictus_desc_index])
                albopictus_desc_index += 1
                last_display_time = current_time
                if albopictus_desc_index >= len(albopictus_descriptions):
                    albopictus_detected = False
                    albopictus_desc_index = 0

        # Handle Aedes Vexans detection
        if current_time - last_display_time >= 2:
            if len(good_matches_vexans) > good_matches_threshold and not vexans_detected:
                print(f"Detected: {data['species']['vexans']['name']}")
                vexans_detected = True
                vexans_desc_index = 0
                last_display_time = current_time

        # Display Aedes Vexans descriptions
        if vexans_detected:
            if current_time - last_display_time >= 2:
                print(vexans_descriptions[vexans_desc_index])
                vexans_desc_index += 1
                last_display_time = current_time
                if vexans_desc_index >= len(vexans_descriptions):
                    vexans_detected = False
                    vexans_desc_index = 0

        # Handle Aedes Niveus detection
        if current_time - last_display_time >= 2:
            if len(good_matches_niveus) > good_matches_threshold and not niveus_detected:
                print(f"Detected: {data['species']['niveus']['name']}")
                niveus_detected = True
                niveus_desc_index = 0
                last_display_time = current_time

        # Display Aedes Niveus descriptions
        if niveus_detected:
            if current_time - last_display_time >= 2:
                print(niveus_descriptions[niveus_desc_index])
                niveus_desc_index += 1
                last_display_time = current_time
                if niveus_desc_index >= len(niveus_descriptions):
                    niveus_detected = False
                    niveus_desc_index = 0

        # Handle Culex Quinquefasciatus detection
        if current_time - last_display_time >= 2:
            if len(good_matches_quinquefasciatus) > good_matches_threshold and not quinquefasciatus_detected:
                print(f"Detected: {data['species']['quinquefasciatus']['name']}")
                quinquefasciatus_detected = True
                quinquefasciatus_desc_index = 0
                last_display_time = current_time

        # Display Culex Quinquefasciatus descriptions
        if quinquefasciatus_detected:
            if current_time - last_display_time >= 2:
                print(quinquefasciatus_descriptions[quinquefasciatus_desc_index])
                quinquefasciatus_desc_index += 1
                last_display_time = current_time
                if quinquefasciatus_desc_index >= len(quinquefasciatus_descriptions):
                    quinquefasciatus_detected = False
                    quinquefasciatus_desc_index = 0

        # Handle Culex Vishnui detection
        if current_time - last_display_time >= 2:
            if len(good_matches_vishnui) > good_matches_threshold and not vishnui_detected:
                print(f"Detected: {data['species']['vishnui']['name']}")
                vishnui_detected = True
                vishnui_desc_index = 0
                last_display_time = current_time

        # Display Culex Vishnui descriptions
        if vishnui_detected:
            if current_time - last_display_time >= 2:
                print(vishnui_descriptions[vishnui_desc_index])
                vishnui_desc_index += 1
                last_display_time = current_time
                if vishnui_desc_index >= len(vishnui_descriptions):
                    vishnui_detected = False
                    vishnui_desc_index = 0

        # Handle Culex Tritaeniorhynchus detection
        if current_time - last_display_time >= 2:
            if len(good_matches_tritaeniorhynchus) > good_matches_threshold and not tritaeniorhynchus_detected:
                print(f" Detected: {data['species']['tritaeniorhynchus']['name']}")
                tritaeniorhynchus_detected = True
                tritaeniorhynchus_desc_index = 0
                last_display_time = current_time

        # Display Culex Tritaeniorhynchus descriptions
        if tritaeniorhynchus_detected:
            if current_time - last_display_time >= 2:
                print(tritaeniorhynchus_descriptions[tritaeniorhynchus_desc_index])
                tritaeniorhynchus_desc_index += 1
                last_display_time = current_time
                if tritaeniorhynchus_desc_index >= len(tritaeniorhynchus_descriptions):
                    tritaeniorhynchus_detected = False
                    tritaeniorhynchus_desc_index = 0

        # If no detection, print message
        if not (aegypti_detected or albopictus_detected or vexans_detected or niveus_detected or
                quinquefasciatus_detected or vishnui_detected or tritaeniorhynchus_detected):
            if current_time - last_display_time >= 10:
                print("No detection")
                last_display_time = current_time

        cv2.imshow('Mosquito Detector', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Run the capture and detect function
capture_and_detect()