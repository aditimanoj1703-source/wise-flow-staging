import { useCurrentFrame, interpolate, spring, staticFile, useVideoConfig, Img } from "remotion";
import { Player } from "./players";

export const PlayerCard: React.FC<{ player: Player; index: number }> = ({ player, index }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const { theme } = player;

  // Ken Burns zoom: 1.12 → 1.0 over the clip
  const zoomProgress = spring({ frame, fps, config: { damping: 30, stiffness: 60 }, durationInFrames });
  const scale = interpolate(zoomProgress, [0, 1], [1.14, 1.0]);

  // Caption slide-up
  const captionProgress = spring({ frame, fps, config: { damping: 18, stiffness: 140 } });
  const captionY = interpolate(captionProgress, [0, 1], [200, 0]);
  const captionOpacity = interpolate(frame, [0, 10], [0, 1], { extrapolateRight: "clamp" });

  return (
    <div style={{ width: "100%", height: "100%", overflow: "hidden", position: "relative", background: theme.c1 }}>

      {/* ── PLAYER PHOTO ── */}
      <div style={{ position: "absolute", inset: 0, transform: `scale(${scale})`, transformOrigin: "center top" }}>
        <Img
          src={staticFile(`${player.slug}.jpg`)}
          style={{
            width: "100%", height: "100%",
            objectFit: "cover",
            objectPosition: "center top",
          }}
        />
      </div>

      {/* ── GRADIENT OVERLAY ── */}
      <div style={{
        position: "absolute", inset: 0,
        background: `linear-gradient(
          to bottom,
          rgba(0,0,0,0.55) 0%,
          rgba(0,0,0,0) 30%,
          rgba(0,0,0,0) 50%,
          rgba(0,0,0,0.7) 72%,
          rgba(0,0,0,0.95) 100%
        )`,
      }} />

      {/* ── TOP BAR ── */}
      <div style={{
        position: "absolute", top: 0, left: 0, right: 0,
        background: `linear-gradient(to bottom, ${theme.c1}dd, transparent)`,
        padding: "60px 50px 40px",
        display: "flex", justifyContent: "space-between", alignItems: "center",
      }}>
        <span style={{ fontSize: 48, color: theme.accent, fontFamily: "'Arial Black', Arial, sans-serif", fontWeight: 900 }}>
          #{index + 1} / 9
        </span>
        <span style={{ fontSize: 56, color: "#fff", fontFamily: "'Arial Black', Arial, sans-serif", fontWeight: 900 }}>
          {player.country.toUpperCase()}
        </span>
      </div>

      {/* ── BOTTOM NAME PLATE ── */}
      <div style={{
        position: "absolute", left: 0, right: 0, bottom: 0,
        opacity: captionOpacity,
        transform: `translateY(${captionY}px)`,
        background: `rgba(0,0,0,0.88)`,
        borderTop: `14px solid ${theme.accent}`,
        padding: "44px 50px 60px",
      }}>
        {/* Player name */}
        <div style={{
          fontSize: 148,
          fontWeight: 900,
          fontFamily: "'Arial Black', Impact, Arial, sans-serif",
          color: "#ffffff",
          lineHeight: 1,
          textShadow: "0 4px 20px rgba(0,0,0,0.9)",
          letterSpacing: -1,
          // auto-scale for long names
          ...(player.name.length > 14 ? { fontSize: 110 } : {}),
          ...(player.name.length > 18 ? { fontSize: 90 } : {}),
        }}>
          {player.name.toUpperCase()}
        </div>

        {/* Country */}
        <div style={{
          fontSize: 108,
          fontWeight: 900,
          fontFamily: "'Arial Black', Impact, Arial, sans-serif",
          color: theme.accent,
          lineHeight: 1,
          marginTop: 20,
          textShadow: "0 3px 12px rgba(0,0,0,0.8)",
        }}>
          {player.flag} {player.country.toUpperCase()}
        </div>

        {/* Note */}
        {player.note && (
          <div style={{
            fontSize: 58,
            fontFamily: "Arial, sans-serif",
            color: "#dddddd",
            marginTop: 18,
            fontStyle: "italic",
          }}>
            {player.note}
          </div>
        )}
      </div>
    </div>
  );
};
