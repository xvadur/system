import { useEffect, useState, type ComponentPropsWithoutRef } from 'react';
import { classes } from './shared.js';

export type ThemeValue = 'light' | 'dark' | 'system';
export type ThemeControlProps = Omit<ComponentPropsWithoutRef<'div'>, 'defaultValue' | 'onChange'> & {
  defaultValue?: ThemeValue;
  storageKey?: string;
  onValueChange?: (value: ThemeValue) => void;
  label?: string;
};

function isTheme(value: unknown): value is ThemeValue {
  return value === 'light' || value === 'dark' || value === 'system';
}

const themeEvent = 'xvadur:theme-change';
type ThemeChange = { storageKey: string | undefined; value: ThemeValue };
// Only browser effects/events populate this map; server rendering never shares user state.
const activeThemes = new Map<string | undefined, ThemeValue>();

/** Controls sharing a storageKey stay synchronized. Persistence is opt-in. */
export function ThemeControl({ defaultValue = 'system', storageKey, onValueChange, label = 'Farebná téma', className, ...props }: ThemeControlProps) {
  const [value, setValue] = useState<ThemeValue>(defaultValue);
  const [ready, setReady] = useState(false);
  useEffect(() => {
    let initial = activeThemes.get(storageKey) ?? defaultValue;
    if (!activeThemes.has(storageKey) && storageKey) {
      try { const saved = localStorage.getItem(storageKey); if (isTheme(saved)) initial = saved; } catch { /* Storage may be blocked; the control still works. */ }
    }
    activeThemes.set(storageKey, initial);
    setValue(initial);
    setReady(true);
    const synchronize = (event: Event) => {
      const detail = (event as CustomEvent<ThemeChange>).detail;
      if (!detail || detail.storageKey !== storageKey || !isTheme(detail.value)) return;
      activeThemes.set(storageKey, detail.value);
      setValue(detail.value);
    };
    const synchronizeStorage = (event: StorageEvent) => {
      if (!storageKey || event.key !== storageKey) return;
      const next = isTheme(event.newValue) ? event.newValue : defaultValue;
      activeThemes.set(storageKey, next);
      setValue(next);
    };
    window.addEventListener(themeEvent, synchronize);
    window.addEventListener('storage', synchronizeStorage);
    return () => {
      window.removeEventListener(themeEvent, synchronize);
      window.removeEventListener('storage', synchronizeStorage);
    };
  }, [storageKey, defaultValue]);
  useEffect(() => {
    if (!ready) return;
    const media = window.matchMedia('(prefers-color-scheme: dark)');
    const apply = () => {
      const resolved = value === 'system' ? (media.matches ? 'dark' : 'light') : value;
      document.documentElement.dataset.theme = resolved;
    };
    apply();
    if (value === 'system') media.addEventListener('change', apply);
    return () => media.removeEventListener('change', apply);
  }, [value, ready]);
  const choose = (next: ThemeValue) => {
    activeThemes.set(storageKey, next);
    setValue(next);
    if (storageKey) { try { localStorage.setItem(storageKey, next); } catch { /* Optional persistence. */ } }
    window.dispatchEvent(new CustomEvent<ThemeChange>(themeEvent, { detail: { storageKey, value: next } }));
    onValueChange?.(next);
  };
  return <div {...props} role="group" aria-label={label} className={classes('xv-theme-control', className)}>
    {(['system', 'light', 'dark'] as const).map(theme => <button key={theme} type="button" className="xv-theme-control__choice" aria-pressed={value === theme} onClick={() => choose(theme)}>{theme === 'system' ? 'Systém' : theme === 'light' ? 'Svetlý' : 'Tmavý'}</button>)}
  </div>;
}
