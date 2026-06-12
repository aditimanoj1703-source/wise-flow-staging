export type Player = {
  name: string;
  country: string;
  flag: string;
  slug: string;
  dur: number; // seconds
  note?: string;
  theme: Theme;
};

export type Theme = {
  c1: string;
  c2: string;
  accent: string;
  text: string;
};

export const THEMES: Record<string, Theme> = {
  Argentina: { c1: "#74ACDF", c2: "#ffffff", accent: "#ffffff", text: "#ffffff" },
  Portugal:  { c1: "#006600", c2: "#CC0000", accent: "#FFD700", text: "#ffffff" },
  France:    { c1: "#002395", c2: "#ED2939", accent: "#ffffff", text: "#ffffff" },
  Brazil:    { c1: "#009C3B", c2: "#FFDF00", accent: "#FFDF00", text: "#ffffff" },
  Norway:    { c1: "#EF2B2D", c2: "#ffffff", accent: "#ffffff", text: "#ffffff" },
  England:   { c1: "#1a1a3e", c2: "#CF081F", accent: "#CF081F", text: "#ffffff" },
  Spain:     { c1: "#AA151B", c2: "#F1BF00", accent: "#F1BF00", text: "#ffffff" },
  Germany:   { c1: "#141414", c2: "#DD0000", accent: "#FFCE00", text: "#ffffff" },
};

export const PLAYERS: Player[] = [
  { name: "Lionel Messi",      country: "Argentina", flag: "🇦🇷", slug: "messi",      dur: 2,   theme: THEMES.Argentina },
  { name: "Cristiano Ronaldo", country: "Portugal",  flag: "🇵🇹", slug: "ronaldo",    dur: 2,   theme: THEMES.Portugal  },
  { name: "Kylian Mbappé",     country: "France",    flag: "🇫🇷", slug: "mbappe",     dur: 2,   theme: THEMES.France    },
  { name: "Neymar Jr",         country: "Brazil",    flag: "🇧🇷", slug: "neymar",     dur: 2,   note: "Back after 2 years!", theme: THEMES.Brazil },
  { name: "Erling Haaland",    country: "Norway",    flag: "🇳🇴", slug: "haaland",    dur: 2,   theme: THEMES.Norway    },
  { name: "Jude Bellingham",   country: "England",   flag: "🏴󠁧󠁢󠁥󠁮󠁧󠁿", slug: "bellingham", dur: 2,   theme: THEMES.England   },
  { name: "Vinicius Jr",       country: "Brazil",    flag: "🇧🇷", slug: "vinicius",   dur: 2,   theme: THEMES.Brazil    },
  { name: "Lamine Yamal",      country: "Spain",     flag: "🇪🇸", slug: "yamal",      dur: 1.5, theme: THEMES.Spain     },
  { name: "Jamal Musiala",     country: "Germany",   flag: "🇩🇪", slug: "musiala",    dur: 1.5, theme: THEMES.Germany   },
];

export const FPS = 30;
export const W   = 1080;
export const H   = 1920;

// Flash transition duration in frames
export const FLASH_FRAMES = 4;

// Compute start frame for each scene
export type SceneInfo = { type: "hook" | "player" | "twist" | "cta" | "flash"; startFrame: number; durationFrames: number; playerIndex?: number };

function buildTimeline(): SceneInfo[] {
  const scenes: SceneInfo[] = [];
  let cursor = 0;

  const push = (s: Omit<SceneInfo, "startFrame">) => {
    scenes.push({ ...s, startFrame: cursor });
    cursor += s.durationFrames;
  };

  push({ type: "hook",  durationFrames: 3 * FPS });
  push({ type: "flash", durationFrames: FLASH_FRAMES });

  PLAYERS.forEach((p, i) => {
    push({ type: "player", durationFrames: Math.round(p.dur * FPS), playerIndex: i });
    push({ type: "flash",  durationFrames: FLASH_FRAMES });
  });

  push({ type: "twist", durationFrames: Math.round(5.5 * FPS) });
  push({ type: "flash", durationFrames: FLASH_FRAMES });
  push({ type: "cta",   durationFrames: 4 * FPS });

  return scenes;
}

export const TIMELINE = buildTimeline();
export const TOTAL_FRAMES = TIMELINE[TIMELINE.length - 1].startFrame + TIMELINE[TIMELINE.length - 1].durationFrames;
