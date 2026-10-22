import { useState } from 'react';
import { Button, Dialog, TextField } from '@xvadur/ui';
import images from '../data/photos.json';
import favorites from '../data/photo-favorites.json';
import { SelectionTransfer, useSelection } from './StudySelection';

const ids = images.map(image => image.id);
export default function PhotoGallery() {
  const selection = useSelection('xvadur-brandbook-photos-v1', favorites, ids);
  const [search, setSearch] = useState('');
  const [format, setFormat] = useState('all');
  const [onlySelected, setOnlySelected] = useState(false);
  const [active, setActive] = useState<string | null>(null);
  const visible = images.filter(image => {
    const ratio = image.width / image.height;
    const orientation = ratio > 1.05 ? 'landscape' : ratio < .95 ? 'portrait' : 'square';
    return (format === 'all' || format === orientation) && (!onlySelected || selection.selected.includes(image.id)) && (!search.trim() || image.filename.toLocaleLowerCase('sk').includes(search.trim().toLocaleLowerCase('sk')) || Number(image.number) === Number(search));
  });
  const image = images.find(item => item.id === active);
  const position = visible.findIndex(item => item.id === active);
  return <div className="brand-study">
    <div className="study-controls photo-controls"><TextField label="Nájsť obrázok" type="search" value={search} onChange={event => setSearch(event.target.value)} placeholder="Číslo alebo názov súboru" /><label className="select-control">Formát<select value={format} onChange={event => setFormat(event.target.value)}><option value="all">Všetky formáty</option><option value="portrait">Na výšku</option><option value="landscape">Na šírku</option><option value="square">Štvorcové</option></select></label><Button variant={onlySelected ? 'primary' : 'secondary'} aria-pressed={onlySelected} onClick={() => setOnlySelected(!onlySelected)}>{onlySelected ? 'Všetky obrázky' : 'Iba označené'}</Button></div>
    <p className="study-results" role="status">{visible.length} z {images.length} obrázkov · zobrazené sú celé fotografie bez orezu</p>
    {visible.length ? <div className="photo-grid">{visible.map((item, index) => <article className={`photo-specimen${selection.selected.includes(item.id) ? ' is-selected' : ''}`} key={item.id}>
      <button type="button" className="photo-preview" aria-label={`Zväčšiť obrázok ${item.number}`} onClick={() => setActive(item.id)}><img src={item.thumbnail} width={item.width} height={item.height} alt={`Obrázok ${item.number} — ${item.filename}`} loading={index < 8 ? 'eager' : 'lazy'} decoding="async" /></button>
      <footer><div><strong>{item.number}</strong><span className="photo-name" title={item.filename}>{item.filename}</span><span>{item.width} × {item.height} px</span></div><Button disabled={!selection.ready} variant={selection.selected.includes(item.id) ? 'primary' : 'secondary'} aria-label={`${selection.selected.includes(item.id) ? 'Zrušiť označenie' : 'Označiť'} obrázok ${item.number}`} aria-pressed={selection.selected.includes(item.id)} onClick={() => selection.toggle(item.id)}>{selection.selected.includes(item.id) ? 'Označené' : 'Označiť'}</Button></footer>
    </article>)}</div> : <div className="study-empty"><h2>Žiadny obrázok pre tento filter.</h2><Button onClick={() => { setSearch(''); setFormat('all'); setOnlySelected(false); }}>Zobraziť všetky obrázky</Button></div>}
    <footer className="study-selection"><div><strong>{selection.selected.length} označených obrázkov</strong><p role="status">{selection.message}</p></div><SelectionTransfer kind="fotky" selected={selection.selected} onImport={selection.replace} onMessage={selection.setMessage} /></footer>
    <p className="study-note">Brand book obsahuje optimalizované náhľady. Originály zostávajú v xvadur_fotky. Výber nemení ani nemaže fotografie.</p>
    <Dialog open={!!image} onOpenChange={open => { if (!open) setActive(null); }} title={image ? `Obrázok ${image.number}` : 'Detail obrázka'} description={image?.filename}>
      {image && <div className="photo-detail"><img src={image.thumbnail} alt={`Obrázok ${image.number} — ${image.filename}`} width={image.width} height={image.height} /><p>{image.width} × {image.height} px · optimalizovaný náhľad</p><div className="detail-actions"><Button variant="secondary" disabled={position <= 0} onClick={() => setActive(visible[position - 1].id)}>Predchádzajúci</Button><Button aria-pressed={selection.selected.includes(image.id)} onClick={() => selection.toggle(image.id)}>{selection.selected.includes(image.id) ? 'Zrušiť označenie' : 'Označiť obrázok'}</Button><Button variant="secondary" disabled={position < 0 || position >= visible.length - 1} onClick={() => setActive(visible[position + 1].id)}>Nasledujúci</Button></div></div>}
    </Dialog>
  </div>;
}
