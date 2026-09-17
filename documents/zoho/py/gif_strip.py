from pathlib import Path
from PIL import Image, ImageSequence

gif_folder = Path(r"C:\Users\Scot Thomson\Desktop\New folder")
gif_name = "btax.gif"
gif_path = gif_folder / gif_name

frames = []

with Image.open(gif_path) as gif:
    for frame in ImageSequence.Iterator(gif):
        frames.append(frame.convert("RGBA"))

if not frames:
    raise RuntimeError("The GIF contains no readable frames.")

total_width = sum(frame.width for frame in frames)
maximum_height = max(frame.height for frame in frames)

print(f"Frames: {len(frames)}")
print(f"Output dimensions: {total_width} × {maximum_height}")

stitched_image = Image.new(
    "RGBA",
    (total_width, maximum_height),
    (0, 0, 0, 0),
)

current_x = 0

for frame in frames:
    stitched_image.paste(frame, (current_x, 0), frame)
    current_x += frame.width

save_path = gif_folder / f"stitched_{gif_path.stem}.png"
stitched_image.save(save_path, format="PNG", optimize=True)

print(save_path)
print("Stitched image saved successfully!")