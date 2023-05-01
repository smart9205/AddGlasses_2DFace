# import cv2
# import numpy as np

# def watermarking(original, watermarked, alpha = 1, x=0, y=0):
#   # (B, G, R, A) = cv2.split(watermarked)
#   # B = cv2.bitwise_and(B, B, mask=A)
#   # G = cv2.bitwise_and(G, G, mask=A)
#   # R = cv2.bitwise_and(R, R, mask=A)
#   # watermarked = cv2.merge([B, G, R, A])

#   (originalHeight, originalWidth) = original.shape[:2]
#   original = np.dstack([original, np.ones((originalHeight,originalWidth), dtype="uint8") * 255])
#   (wH, wW) = watermarked.shape[:2]

#   #Blending
#   overlay = np.zeros((originalHeight, originalWidth, 4), dtype="uint8")
#   overlay[y:y + wH, x:x + wW] = watermarked
#   final = original.copy()
#   return cv2.addWeighted(overlay, alpha, final, 1.0, 0, final)

import cv2
import numpy as np

def transparentOverlay(src, overlay, x, y, scale=1):
    src = src.copy()
    overlay = cv2.resize(overlay, (0, 0), fx=scale, fy=scale)
    h, w, _ = overlay.shape  # Size of foreground
    rows, cols, _ = src.shape  # Size of background Image

    # loop over all pixels and apply the blending equation
    for i in range(h):
        for j in range(w):
            if y + i >= rows or x + j >= cols:
                continue
            alpha = float(overlay[i][j][3] / 255.0)  # read the alpha channel
            src[y + i][x + j] = alpha * overlay[i][j][:3] + (1 - alpha) * src[y + i][x + j]
    return src

def watermarking(original, watermarked, alpha = 1, x=0, y=0):
  overlay = transparentOverlay(original, watermarked, x, y)
  output = original.copy()
  cv2.addWeighted(overlay, 1, output, 1 - 1, 0, output)
  return output
