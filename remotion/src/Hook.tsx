import { useCurrentFrame, interpolate, spring, useVideoConfig } from "remotion";

const lines = [
  { text: "WORLD CUP 2026 ⚽", big: true },
  { text: "Can you guess which country", big: false },
  { text: "these legends play for?", big: false },
  { text: "LET'S GO! 🔥", big: true },
];

export const Hook: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <div style={{
      width: "100%", height: "100%",
      background: "linear-gradient(160deg, #0a0a1e 0%, #0a0a0a 100%)",
      display: "flex", flexDirection: "column",
      alignItems: "center", justifyContent: "center",
      fontFamily: "'Arial Black', Impact, Arial, sans-serif",
      gap: 28,
    }}>
      {lines.map(({ text, big }, i) => {
        const delay = i * 0.35 * fps;
        const progress = spring({ frame: frame - delay, fps, config: { damping: 14, stiffness: 120 } });
        const opacity = interpolate(frame - delay, [0, 8], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
        const y = interpolate(progress, [0, 1], [40, 0]);

        return (
          <div key={i} style={{
            opacity,
            transform: `translateY(${y}px)`,
            fontSize: big ? 96 : 68,
            fontWeight: 900,
            color: big ? "#FFD700" : "#ffffff",
            textAlign: "center",
            textShadow: "0 4px 24px rgba(0,0,0,0.8)",
            letterSpacing: big ? 2 : 0,
            padding: "0 40px",
            lineHeight: 1.15,
          }}>
            {text}
          </div>
        );
      })}

      {/* animated underline */}
      <div style={{
        width: interpolate(frame, [60, 90], [0, 280], { extrapolateRight: "clamp" }),
        height: 6,
        background: "#FFD700",
        borderRadius: 3,
        marginTop: 16,
      }} />
    </div>
  );
};
