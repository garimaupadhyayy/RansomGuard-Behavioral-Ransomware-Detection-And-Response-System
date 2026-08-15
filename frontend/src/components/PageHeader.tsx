interface PageHeaderProps {
  eyebrow: string;
  title: string;
  description?: string;
}

export default function PageHeader({ eyebrow, title, description }: PageHeaderProps) {
  return (
    <div style={{ marginBottom: "1.75rem" }}>
      <div
        style={{
          fontFamily: "var(--font-mono)",
          fontSize: "0.72rem",
          color: "var(--blue-400)",
          letterSpacing: "0.08em",
          textTransform: "uppercase",
          marginBottom: 6,
        }}
      >
        {eyebrow}
      </div>
      <h1 style={{ fontFamily: "var(--font-display)", fontSize: "1.7rem", fontWeight: 700, margin: 0, color: "var(--text-primary)" }}>
        {title}
      </h1>
      {description && (
        <p style={{ color: "var(--text-secondary)", marginTop: 6, fontSize: "0.92rem", maxWidth: 640 }}>{description}</p>
      )}
    </div>
  );
}
