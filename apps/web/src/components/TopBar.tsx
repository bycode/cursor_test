type Props = {
  ready: boolean;
};

export function TopBar({ ready }: Props) {
  return (
    <header className="topbar">
      <h1 className="topbar__title">报警二次校验</h1>
      <div className="topbar__status">
        <span
          className="topbar__status-dot"
          style={{ background: ready ? "var(--color-success)" : "var(--color-warning)" }}
        />
        {ready ? "服务就绪" : "连接中"}
      </div>
    </header>
  );
}
