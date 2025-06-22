import numpy as np
import imageio
num_frames = 30  # 2 seconds at 30 FPS
height, width = 1080, 1920  # Full HD resolution

# Generate frames with random noise
frames_hd = [np.random.rand(height, width) for _ in range(num_frames)]

# Save as GIF
gif_hd_path = "noise.gif"
imageio.mimsave(gif_hd_path, (np.array(frames_hd) * 255).astype(np.uint8), duration=1/30, loop=0)
