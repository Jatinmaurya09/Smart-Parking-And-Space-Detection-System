# Smart Parking Space Detection and Availability Monitoring System

A computer-vision mini project that detects whether each parking slot in a
top-view image or video is **occupied** (red) or **free** (green) and shows
live counts on a dashboard.

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

## Run the Python version (images + video)

```bash
pip install -r requirements.txt
python slot_picker.py     # mark slots once, creates slots_*.json
python main.py            # results are saved in the output/ folder
