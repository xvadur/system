import { useState, type CSSProperties } from 'react';
import { Button, TextField } from '@xvadur/ui';
import pairs from '../data/font-pairs.json';
import favorites from '../data/font-favorites.json';
import { SelectionTransfer, useSelection } from './StudySelection';

const ids = pairs.map(pair => pair.id);
export default function FontStudy() {
  const selection = useSelection('xvadur-brandbook-fonts-v1', favorites, ids);
  const [filter, setFilter] = useState('favorites');
  const [sample, setSample] = useState('Výskum, nástroje a vlastné projekty.');
  const [size, setSize] = useState(80);
  const [detail, setDetail] = useState(false);
  const visible = pairs.filter(pair => filter === 'favorites' ? selection.selected.includes(pair.id) : filter === 'all' || pair.round === Number(filter));
  return <div className="brand-study">
    <div className="study-controls"><TextField label="Skúšobný nadpis" value={sample} onChange={event => setSample(event.target.value)} /><label className="range-control">Veľkosť názvu <strong>{size} px</strong><input aria-label="Veľkosť názvu" type="range" min="40" max="96" value={size} onChange={event => setSize(Number(event.target.value))} /></label><Button variant="secondary" aria-pressed={detail} onClick={() => setDetail(!detail)}>{detail ? 'Prehľad dvojíc' : 'Zobraziť detail'}</Button></div>
    <div className="study-filter-row"><div className="study-filters" role="group" aria-label="Kolá výberu fontov">{[{ id: 'favorites', label: 'Tvoji favoriti' }, { id: 'all', label: 'Všetkých 48' }, ...[1, 2, 3, 4].map(round => ({ id: String(round), label: `${round}. kolo` }))].map(item => <Button key={item.id} variant={filter === item.id ? 'primary' : 'secondary'} aria-pressed={filter === item.id} onClick={() => setFilter(item.id)}>{item.label}</Button>)}</div><p role="status">{visible.length} dvojíc · označených {selection.selected.length}</p></div>
    {visible.length ? <div className={`font-grid${detail ? ' font-grid-detail' : ''}`}>{visible.map(pair => {
      const chosen = selection.selected.includes(pair.id);
      const style = { '--pair-display': `"${pair.display}"`, '--pair-body': `"${pair.body}"`, '--pair-weight': pair.weight, '--pair-size': `${size}px`, '--pair-style': 'style' in pair ? pair.style : 'normal' } as CSSProperties;
      return <article className={`font-specimen${chosen ? ' is-selected' : ''}`} key={pair.id} id={`pair-${pair.id}`} style={style}>
        <header><h2>{pair.display} <span>+ {pair.secondary}</span></h2><span className="specimen-number">{pair.id}</span></header>
        <div className="specimen-word">XVADUR</div><h3>{sample || 'Výskum, nástroje a vlastné projekty.'}</h3>
        <p className="specimen-body">Zo zdravotníctva som si odniesol pozornosť k ľuďom. S AI dávam svojim otázkam ďalší tvar: texty, výskum, nástroje a vlastnú firmu.</p>
        {detail && <div className="specimen-detail"><p>{pair.label} {pair.note}</p><p>Čítanie · Projekty · Obchod · Spolupráca</p><p className="specimen-body">Ľščťžýáíéôäň · 0123456789 · {pair.display} / {pair.body}</p><a href={`https://fonts.google.com/specimen/${encodeURIComponent(pair.display).replaceAll('%20', '+')}`}>Zdroj písma ↗</a></div>}
        <footer><span>{pair.round}. kolo · nadpis {pair.weight} / text 400</span><Button disabled={!selection.ready} variant={chosen ? 'primary' : 'secondary'} aria-pressed={chosen} aria-label={`${chosen ? 'Zrušiť označenie' : 'Označiť'} dvojicu ${pair.id}`} onClick={() => selection.toggle(pair.id)}>{chosen ? 'Vo výbere' : 'Označiť dvojicu'}</Button></footer>
      </article>;
    })}</div> : <div className="study-empty"><h2>Zatiaľ bez favoritov.</h2><p>Otvor všetky dvojice a označ tie, s ktorými chceš pokračovať.</p><Button onClick={() => setFilter('all')}>Zobraziť všetky dvojice</Button></div>}
    <footer className="study-selection"><div><strong>{selection.selected.length} označených dvojíc</strong><p role="status">{selection.message}</p></div><SelectionTransfer kind="fonty" selected={selection.selected} onImport={selection.replace} onMessage={selection.setMessage} /></footer>
    <p className="study-note">Favoriti sú pracovný výber. Písma systému ešte nie sú definitívne určené. <a href="/brand/licenses/README.txt">Zdroje a licencie písiem</a>.</p>
  </div>;
}
