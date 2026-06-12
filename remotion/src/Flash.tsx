import { useCurrentFrame, interpolate } from "remotion";

export const Flash: React.FC = () => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 2, 4], [1, 0.6, 0], { extrapolateRight: "clamp" });

  return (
    <div style={{
      width: "100%", height: "100%",
      background: "#ffffff",
      opacity,
    }} />
  );
};
