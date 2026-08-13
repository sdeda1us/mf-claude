interface AvatarProps {
  name: string;
  src?: string | null;
  size?: number;
}

export default function Avatar({ name, src, size = 28 }: AvatarProps) {
  const initials = name
    .trim()
    .split(/\s+/)
    .slice(0, 2)
    .map((part) => part[0]?.toUpperCase())
    .join("");

  const style = { width: size, height: size, fontSize: size * 0.4 };

  if (src) {
    return <img className="avatar" style={style} src={src} alt={name} />;
  }
  return (
    <span className="avatar avatar-fallback" style={style}>
      {initials || "?"}
    </span>
  );
}
