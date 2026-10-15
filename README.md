# Smart Parking Space Detection and Availability Monitoring System

A computer-vision mini project that detects whether each parking slot in a
top-view image or video is **occupied** (red) or **free** (green) and shows
live counts on a dashboard.

### 🔗 Live Demo: [smart-parking-and-space-detection-s.vercel.app](https://smart-parking-and-space-detection-s.vercel.app/)

**Try it now** — upload a parking image, select the matching slots file, and click Detect.

---

The repository has two parts:

| Part | Files | Purpose |
|---|---|---|
| Python version | `main.py`, `slot_picker.py` | Full project: images + video, OpenCV windows, saved PNG/AVI output |
| Web demo | `app.py`, `templates/index.html` | Flask web app for Vercel deployment (images only) |

## How it works

1. Each slot is marked once as a rectangle `[x, y, w, h]` and stored in a JSON file.
2. For every slot the central region is cropped (20% margin removed from each side)
   to ignore painted lines and neighbouring cars.
3. The crop is converted to HSV and grayscale, and three values are computed:
   - **V**: median brightness
   - **S**: median saturation
   - **gray_std**: standard deviation of gray levels (texture)
4. The slot is **occupied** if any rule is true:
   - `V > 195` (white car)
   - `V < 100` (dark car)
   - `S > 55` (coloured car)
   - `gray_std > 45 and V < 180` (textured gray/silver car)
5. Otherwise it looks like plain concrete and is **free**.
6. A dashboard shows Total, Occupied, Available and
   `PARKING AVAILABLE` / `PARKING FULL`.

## Results

| Image | Total slots | Occupied | Free |
|---|---|---|---|
| Parking_slot1.png (drone view) | 32 | 3 | 29 |
| Parking_slot2.png (close view) | 14 | 8 | 6 |

## Project Structure

    smart-parking/
    ├── app.py                    # Flask web app (deployed on Vercel)
    ├── vercel.json               # Vercel configuration
    ├── requirements.txt          # Python dependencies
    ├── .gitignore
    ├── README.md
    ├── templates/
    │   └── index.html            # Web frontend (HTML + CSS + JS)
    ├── slots_1.json              # Marked slots for image 1
    ├── slots_2.json              # Marked slots for image 2
    ├── main.py                   # Python detection program (desktop)
    ├── slot_picker.py            # Slot marking tool (one-time setup)
    ├── test_video.py             # Video debugging helper
    ├── input/
    │   ├── Parking_slot1.png
    │   ├── Parking_slot2.png
    │   └── parking_video.mp4
    └── output/
        ├── result_1.png
        ├── result_2.png
        └── result_video.avi

## Run the Python version (images + video)

    pip install -r requirements.txt
    python slot_picker.py     # mark slots once, creates slots_*.json
    python main.py            # results are saved in the output/ folder

Put inputs in `input/` (`Parking_slot1.png`, `Parking_slot2.png`,
`parking_video.mp4`). Press `Q` or `Esc` to stop a video.

## Run the web demo locally

    pip install -r requirements.txt
    python app.py

Then visit `http://127.0.0.1:5000`. Upload an image, select the matching
slots JSON, and click **Detect**. The page shows the total, occupied and
available counts along with the annotated result image.

## Deploy on Vercel

1. Push this folder to a GitHub repository.
2. Go to vercel.com, click **Add New → Project**, and import the repository.
3. Framework preset: **Other**. Leave build and output settings empty.
   Click **Deploy**.
4. If the build fails due to the Python bundle size, add an environment
   variable `VERCEL_SUPPORT_LARGE_FUNCTIONS = 1` in the project settings
   and redeploy.

## Limitations

- Slots are marked manually and the camera must stay fixed.
- Thresholds are tuned on the sample images; other lighting may need re-tuning.
- Heavy shadows, stains or puddles can cause false "occupied" results.
- Only marked slots are analysed.
- Video processing works only in the Python version, not in the web demo.

## Future Scope

YOLO/CNN vehicle detection, automatic slot detection, temporal smoothing for
video, mobile app/API, number-plate recognition.
