import { useEffect, useState, type ChangeEvent } from 'react';
import { Button } from '@xvadur/ui';

export function useSelection(key: string, initial: string[], validIds: string[]) {
  const [selected, setSelected] = useState<string[]>(initial);
  const [ready, setReady] = useState(false);
  const [message, setMessage] = useState('Načítavam uložený výber…');
  useEffect(() => {
    try {
      const value = localStorage.getItem(key);
      if (value !== null) {
        const parsed: unknown = JSON.parse(value);
        if (Array.isArray(parsed)) setSelected(parsed.filter((id): id is string => typeof id === 'string' && validIds.includes(id)));
      }
      setMessage('Výber sa ukladá v tomto prehliadači. Na prenos použi Export JSON.');
    } catch { setMessage('Úložisko prehliadača nie je dostupné. Výber si exportuj do JSON.'); }
    setReady(true);
    function onStorage(event: StorageEvent) {
      if (event.key !== key) return;
      try {
        const parsed: unknown = JSON.parse(event.newValue || '[]');
        if (Array.isArray(parsed)) setSelected(parsed.filter((id): id is string => typeof id === 'string' && validIds.includes(id)));
      } catch { /* Keep the current selection if another tab writes invalid data. */ }
    }
    window.addEventListener('storage', onStorage);
    return () => window.removeEventListener('storage', onStorage);
  }, [key]); // The seed and valid IDs are static catalog data.
  function replace(ids: string[]) {
    if (ids.some(id => !validIds.includes(id))) {
      setMessage('Výber obsahuje neznáme položky. Doterajší výber zostal zachovaný.');
      return;
    }
    const next = [...new Set(ids)].filter(id => validIds.includes(id));
    setSelected(next);
    try { localStorage.setItem(key, JSON.stringify(next)); setMessage('Výber uložený v tomto prehliadači.'); }
    catch { setMessage('Výber sa nepodarilo uložiť. Exportuj ho do JSON.'); }
  }
  function toggle(id: string) { replace(selected.includes(id) ? selected.filter(item => item !== id) : [...selected, id]); }
  return { selected, ready, message, setMessage, replace, toggle };
}

export function SelectionTransfer({ kind, selected, onImport, onMessage }: {
  kind: 'fonty' | 'fotky'; selected: string[]; onImport: (ids: string[]) => void; onMessage: (message: string) => void;
}) {
  async function importFile(event: ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];
    if (!file) return;
    try {
      if (file.size > 1024 * 1024) throw new Error('Súbor je príliš veľký. Použi export výberu do JSON.');
      const data = JSON.parse(await file.text());
      if (data.kind && data.kind !== kind) throw new Error('Tento výber patrí do inej sekcie.');
      const ids = Array.isArray(data) ? data : data.selected ?? data.pairs?.map((item: { id: string }) => item.id) ?? data.images?.map((item: { id: string }) => item.id);
      if (!Array.isArray(ids) || !ids.every(id => typeof id === 'string')) throw new Error('Súbor neobsahuje platný výber.');
      onImport(ids);
    } catch (error) { onMessage(error instanceof Error ? error.message : 'Výber sa nepodarilo načítať.'); }
    event.target.value = '';
  }
  function exportFile() {
    const url = URL.createObjectURL(new Blob([JSON.stringify({ project: 'XVADUR Stack', kind, selected, exportedAt: new Date().toISOString() }, null, 2)], { type: 'application/json' }));
    const link = document.createElement('a'); link.href = url; link.download = `xvadur-${kind}-vyber.json`; link.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }
  return <div className="selection-transfer"><Button variant="secondary" onClick={exportFile}>Export JSON</Button><label className="file-import">Import výberu<input aria-label={`Import výberu: ${kind}`} type="file" accept="application/json,.json" onChange={importFile} /></label></div>;
}
