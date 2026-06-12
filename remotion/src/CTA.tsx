import { useCurrentFrame, interpolate, spring, useVideoConfig } from "remotion";

const lines = [
  { text: "FOLLOW",       big: true,  color: "#FFD700" },
  { text: "for more",     big: false, color: "#ffffff" },
  { text: "⚽ WORLD CUP", big: true,  color: "#ffffff" },
  { text: "content! 🔥",  big: true,  color: "#FFD700" },
];

export const CTA: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Pulsing scale on FOLLOW
  const pulse = interpolate(
    Math.sin((frame / fps) * Math.PI * 2),
    [-1, 1],
    [0.96, 1.04],
  );

  return (
    <div style={{
      width: "100%", height: "100%",
      background: "linear-gradient(160deg, #003300 0%, #001100 100%)",
      display: "flex", flexDirection: "column",
      alignItems: "center", justifyContent: "center",
      fontFamily: "'Arial Black', Impact, Arial, sans-serif",
      gap: 28,
      padding: "0 40px",
    }}>
      {lines.map(({ text, big, color }, i) => {
        const delay = i * 0.3 * fps;
        const progress = spring({ frame: frame - delay, fps, config: { damping: 14, stiffness: 130 } });
        const opacity = interpolate(frame - delay, [0, 8], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
        const y = interpolate(progress, [0, 1], [40, 0]);
        const extraScale = i === 0 ? pulse : 1;

        return (
          <div key={i} style={{
            opacity,
            transform: `translateY(${y}px) scale(${extraScale})`,
            fontSize: big ? 112 : 68,
            fontWeight: 900,
            color,
            textAlign: "center",
            textShadow: "0 4px 24px rgba(0,0,0,0.8)",
            lineHeight: 1.15,
          }}>
            {text}
          </div>
        );
      })}

      {/* animated underline */}
      <div style={{
        width: interpolate(frame, [60, 100], [0, 320], { extrapolateRight: "clamp" }),
        height: 8,
        background: "#FFD700",
        borderRadius: 4,
        marginTop: 24,
      }} />
    </div>
  );
};
