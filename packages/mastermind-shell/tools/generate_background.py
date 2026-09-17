from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter


WIDTH = 1920
HEIGHT = 1280

OUTPUT = Path("packages/mastermind-shell/src/mastermind_shell/assets/background.png")


def smooth_noise(width: int, height: int, scale: int = 80) -> np.ndarray:
    """Generate smooth low-frequency noise."""
    small_w = max(2, width // scale)
    small_h = max(2, height // scale)

    noise = np.random.random((small_h, small_w)).astype(np.float32)

    image = Image.fromarray(
        np.uint8(noise * 255),
        mode="L",
    )

    image = image.resize(
        (width, height),
        Image.Resampling.BICUBIC,
    )

    image = image.filter(
        ImageFilter.GaussianBlur(scale * 0.5)
    )

    return np.asarray(image, dtype=np.float32) / 255.0


def generate_background() -> Image.Image:
    # ------------------------------------------------------------
    # Coordinates
    # ------------------------------------------------------------

    y, x = np.mgrid[0:HEIGHT, 0:WIDTH]

    nx = x / WIDTH
    ny = y / HEIGHT

    # ------------------------------------------------------------
    # Large organic deformation
    # ------------------------------------------------------------

    noise1 = smooth_noise(WIDTH, HEIGHT, 180)
    noise2 = smooth_noise(WIDTH, HEIGHT, 90)
    noise3 = smooth_noise(WIDTH, HEIGHT, 35)

    # Deform coordinates using noise
    dx = (
        np.sin(ny * 18.0 + noise1 * 5.0)
        * 0.035
        + (noise2 - 0.5) * 0.08
    )

    dy = (
        np.sin(nx * 14.0 + noise1 * 4.0)
        * 0.035
        + (noise2 - 0.5) * 0.08
    )

    warped_x = nx + dx
    warped_y = ny + dy

    # ------------------------------------------------------------
    # Balatro-style flowing bands
    # ------------------------------------------------------------

    wave1 = np.sin(
        warped_x * 16.0
        + np.sin(warped_y * 8.0) * 2.5
        + noise1 * 5.0
    )

    wave2 = np.sin(
        warped_y * 13.0
        + np.sin(warped_x * 7.0) * 2.0
        + noise2 * 4.0
    )

    wave3 = np.sin(
        (warped_x + warped_y) * 20.0
        + noise3 * 3.0
    )

    # Combine waves
    pattern = (
        wave1 * 0.50
        + wave2 * 0.35
        + wave3 * 0.15
    )

    # Normalize
    pattern = pattern * 0.5 + 0.5

    # Make the shapes more defined
    pattern = np.clip(
        (pattern - 0.25) / 0.5,
        0.0,
        1.0,
    )

    # ------------------------------------------------------------
    # Color palette
    # ------------------------------------------------------------

    dark = np.array([20, 30, 55], dtype=np.float32)

    mid = np.array([45, 70, 130], dtype=np.float32)

    light = np.array([90, 130, 210], dtype=np.float32)

    # First gradient
    t = pattern[..., None]

    color = dark * (1.0 - t) + mid * t

    # Add brighter areas
    highlight = np.clip(
        (pattern - 0.55) / 0.45,
        0.0,
        1.0,
    )[..., None]

    color = (
        color * (1.0 - highlight)
        + light * highlight
    )

    # ------------------------------------------------------------
    # Subtle radial lighting
    # ------------------------------------------------------------

    cx = nx - 0.5
    cy = ny - 0.5

    distance = np.sqrt(
        cx * cx + cy * cy
    )

    light_center = np.clip(
        1.0 - distance * 1.35,
        0.0,
        1.0,
    )

    color += light_center[..., None] * 12.0

    # ------------------------------------------------------------
    # Grain
    # ------------------------------------------------------------

    grain = (
        np.random.normal(
            0.0,
            3.0,
            (HEIGHT, WIDTH, 1),
        )
    )

    color += grain

    # ------------------------------------------------------------
    # Vignette
    # ------------------------------------------------------------

    vignette = np.clip(
        1.0 - distance * 0.55,
        0.65,
        1.0,
    )

    color *= vignette[..., None]

    # ------------------------------------------------------------
    # Final image
    # ------------------------------------------------------------

    color = np.clip(color, 0, 255).astype(np.uint8)

    return Image.fromarray(color, "RGB")


if __name__ == "__main__":
    print(f"Generating {WIDTH}x{HEIGHT} background...")

    image = generate_background()

    # Force un PNG RGB standard compatible SDL_image/Pygame
    image = image.convert("RGB")

    image.save(
        OUTPUT,
        format="PNG",
        optimize=False,
    )

    # Vérification
    test = Image.open(OUTPUT)
    print(f"Saved: {OUTPUT.resolve()}")
    print(f"Size: {test.size}")
    print(f"Mode: {test.mode}")
    print(f"Format: {test.format}")
