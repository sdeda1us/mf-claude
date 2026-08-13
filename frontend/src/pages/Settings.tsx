import { useState } from "react";
import Avatar from "../components/Avatar";
import { useAuth } from "../auth/AuthContext";
import { api, ApiError } from "../lib/api";

const AVATAR_SIZE = 256;

function resizeToSquareDataUrl(file: File): Promise<string> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onerror = () => reject(new Error("Couldn't read that file"));
    reader.onload = () => {
      const img = new Image();
      img.onerror = () => reject(new Error("That doesn't look like a valid image"));
      img.onload = () => {
        const canvas = document.createElement("canvas");
        canvas.width = AVATAR_SIZE;
        canvas.height = AVATAR_SIZE;
        const ctx = canvas.getContext("2d");
        if (!ctx) {
          reject(new Error("Couldn't process that image"));
          return;
        }
        // Cover-crop to a centered square before scaling down.
        const side = Math.min(img.width, img.height);
        const sx = (img.width - side) / 2;
        const sy = (img.height - side) / 2;
        ctx.drawImage(img, sx, sy, side, side, 0, 0, AVATAR_SIZE, AVATAR_SIZE);
        resolve(canvas.toDataURL("image/jpeg", 0.85));
      };
      img.src = reader.result as string;
    };
    reader.readAsDataURL(file);
  });
}

export default function Settings() {
  const { user, refresh } = useAuth();
  const [displayName, setDisplayName] = useState(user?.display_name ?? "");
  const [avatarPreview, setAvatarPreview] = useState<string | null>(user?.avatar_data_url ?? null);
  const [avatarChanged, setAvatarChanged] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [saved, setSaved] = useState(false);
  const [saving, setSaving] = useState(false);

  if (!user) return null;

  const onFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setError(null);
    try {
      const dataUrl = await resizeToSquareDataUrl(file);
      setAvatarPreview(dataUrl);
      setAvatarChanged(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Couldn't process that image");
    }
  };

  const removeAvatar = () => {
    setAvatarPreview(null);
    setAvatarChanged(true);
  };

  const save = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSaved(false);
    setSaving(true);
    try {
      await api.put("/users/me", {
        display_name: displayName,
        avatar_data_url: avatarChanged ? (avatarPreview ?? "") : undefined,
      });
      await refresh();
      setAvatarChanged(false);
      setSaved(true);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Failed to save");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="page">
      <h1>Settings</h1>

      <form onSubmit={save} className="stacked-form settings-form">
        <div className="avatar-editor">
          <Avatar name={displayName || user.display_name} src={avatarPreview} size={96} />
          <div className="avatar-editor-controls">
            <label className="file-input-label">
              Upload photo…
              <input type="file" accept="image/*" onChange={onFileChange} hidden />
            </label>
            {avatarPreview && (
              <button type="button" onClick={removeAvatar}>
                Remove
              </button>
            )}
          </div>
        </div>

        <label>
          Display name
          <input
            type="text"
            value={displayName}
            onChange={(e) => setDisplayName(e.target.value)}
            maxLength={100}
            required
          />
        </label>

        <label>
          Email
          <input type="email" value={user.email} disabled title="Contact the commissioner to change your login email" />
        </label>

        {error && <p className="error">{error}</p>}
        {saved && !error && <p className="saved-message">Saved.</p>}

        <button type="submit" className="btn-primary" disabled={saving}>
          {saving ? "Saving…" : "Save changes"}
        </button>
      </form>
    </div>
  );
}
