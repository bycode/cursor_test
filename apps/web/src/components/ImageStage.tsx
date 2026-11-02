import { useEffect, useRef, useState } from "react";
import type { BBox, Detection } from "../api/types";

type Props = {
  imageUrl: string | null;
  alarmBoxes: BBox[];
  cabinBoxes: Detection[] | BBox[];
};

export function ImageStage({ imageUrl, alarmBoxes, cabinBoxes }: Props) {
  const imgRef = useRef<HTMLImageElement>(null);
  const [size, setSize] = useState({ w: 0, h: 0, natW: 1, natH: 1 });

  useEffect(() => {
    const img = imgRef.current;
    if (!img) return;
    const update = () => {
      setSize({
        w: img.clientWidth,
        h: img.clientHeight,
        natW: img.naturalWidth || 1,
        natH: img.naturalHeight || 1,
      });
    };
    update();
    img.addEventListener("load", update);
    window.addEventListener("resize", update);
    return () => {
      img.removeEventListener("load", update);
      window.removeEventListener("resize", update);
    };
  }, [imageUrl]);

  const sx = size.w / size.natW;
  const sy = size.h / size.natH;

  return (
    <div>
      <div className="image-stage">
        {imageUrl ? (
          <>
            <img ref={imgRef} className="image-stage__img" src={imageUrl} alt="校验原图" />
            <svg className="image-stage__overlay" viewBox={`0 0 ${size.w || 1} ${size.h || 1}`}>
              {cabinBoxes
                .filter((b) => b.x != null && b.y != null && b.w != null && b.h != null)
                .map((b, i) => (
                  <rect
                    key={`c-${i}`}
                    x={(b.x as number) * sx}
                    y={(b.y as number) * sy}
                    width={(b.w as number) * sx}
                    height={(b.h as number) * sy}
                    fill="var(--color-detect-box)"
                    fillOpacity={0.12}
                    stroke="var(--color-detect-box)"
                    strokeWidth={2}
                    strokeDasharray="6 4"
                  />
                ))}
              {alarmBoxes.map((b, i) => (
                <rect
                  key={`a-${i}`}
                  x={b.x * sx}
                  y={b.y * sy}
                  width={b.w * sx}
                  height={b.h * sy}
                  fill="none"
                  stroke="var(--color-alarm-box)"
                  strokeWidth={2}
                />
              ))}
            </svg>
          </>
        ) : (
          <span className="image-stage__empty">无图像</span>
        )}
      </div>
      <div className="image-stage__legend">
        <span>
          <i className="legend-key legend-key--alarm" />
          上游未戴帽框
        </span>
        <span>
          <i className="legend-key legend-key--detect" />
          驾驶室 cabin
        </span>
      </div>
    </div>
  );
}
