import type { ReactNode } from "react";
import { TopBar } from "./TopBar";

type Props = {
  ready: boolean;
  aside: ReactNode;
  main: ReactNode;
};

export function Shell({ ready, aside, main }: Props) {
  return (
    <div className="shell">
      <TopBar ready={ready} />
      <div className="shell__body">
        <aside className="shell__aside">{aside}</aside>
        <main className="shell__main">{main}</main>
      </div>
    </div>
  );
}
