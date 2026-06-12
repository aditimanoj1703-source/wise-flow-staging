import { Composition, AbsoluteFill, Sequence } from "remotion";
import { PLAYERS, TIMELINE, TOTAL_FRAMES, FPS, W, H } from "./players";
import { Hook } from "./Hook";
import { PlayerCard } from "./PlayerCard";
import { Twist } from "./Twist";
import { CTA } from "./CTA";
import { Flash } from "./Flash";

const WorldCupShort: React.FC = () => {
  return (
    <AbsoluteFill style={{ background: "#000" }}>
      {TIMELINE.map((scene, i) => {
        let content: React.ReactNode;

        if (scene.type === "hook") {
          content = <Hook />;
        } else if (scene.type === "flash") {
          content = <Flash />;
        } else if (scene.type === "player" && scene.playerIndex !== undefined) {
          const player = PLAYERS[scene.playerIndex];
          content = <PlayerCard player={player} index={scene.playerIndex} />;
        } else if (scene.type === "twist") {
          content = <Twist />;
        } else if (scene.type === "cta") {
          content = <CTA />;
        } else {
          content = null;
        }

        return (
          <Sequence
            key={i}
            from={scene.startFrame}
            durationInFrames={scene.durationFrames}
          >
            <AbsoluteFill>{content}</AbsoluteFill>
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="WorldCupShort"
      component={WorldCupShort}
      durationInFrames={TOTAL_FRAMES}
      fps={FPS}
      width={W}
      height={H}
    />
  );
};
