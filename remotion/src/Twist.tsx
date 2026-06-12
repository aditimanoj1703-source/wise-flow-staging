import { useCurrentFrame, interpolate, spring, useVideoConfig } from "remotion";

const lines = [
  { text: "WAIT… 🤔",           big: true  },
  { text: "Did you know these 9 legends", big: false },
  { text: "all play in the",    big: false },
  { text: "WORLD CUP 2026?",    big: true  },
  { text: "Drop your score 👇",  big: false },
];

export const Twist: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <div style={{
      width: "100%", height: "100%",
      background: "linear-gradient(160deg, #1a0a2e 0%, #0a0a0a 100%)",
      display: "flex", flexDirection: "column",
      alignItems: "center", justifyContent: "center",
      fontFamily: "'Arial Black', Impact, Arial, sans-serif",
      gap: 32,
      padding: "0 40px",
    }}>
      {lines.map(({ text, big }, i) => {
        const delay = i * 0.4 * fps;
        const progress = spring({ frame: frame - delay, fps, config: { damping: 14, stiffness: 120 } });
        const opacity = interpolate(frame - delay, [0, 8], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
        const y = interpolate(progress, [0, 1], [50, 0]);

        return (
          <div key={i} style={{
            opacity,
            transform: `translateY(${y}px)`,
            fontSize: big ? 100 : 64,
            fontWeight: 900,
            color: big ? "#FFD700" : "#ffffff",
            textAlign: "center",
            textShadow: "0 4px 24px rgba(0,0,0,0.8)",
            letterSpacing: big ? 2 : 0,
            lineHeight: 1.2,
          }}>
            {text}
          </div>
        );
      })}
    </div>
  );
};
